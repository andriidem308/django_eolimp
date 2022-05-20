from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView

from testing.decorators import student_required
from testing.forms import StudentSignUpForm, CreateSolutionForm
from testing.models import Problem, User, Solution, Lecture, Student
from testing.services.code_solver import test_student_solution


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:problem_list')


@method_decorator([login_required, student_required], name='dispatch')
class TaskListView(ListView):
    model = Problem
    ordering = ('title', )
    context_object_name = 'problems'
    template_name = 'students/problem_list.html'

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)
        solutions = Solution.objects.filter(student=student)
        problem_list = [solution.problem.id for solution in solutions]
        queryset = Problem.objects.filter(group=student.group).exclude(pk__in=problem_list)
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class SolutionListView(ListView):
    model = Solution
    context_object_name = 'solutions'
    template_name = 'students/solution_list.html'

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)
        queryset = Solution.objects.filter(student=student)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = Student.objects.get(user=self.request.user)
        solutions = Solution.objects.filter(student=student)

        context['points_sum'] = sum([sol.score for sol in solutions])
        context['points_total'] = sum([sol.problem.problem_value for sol in solutions])

        return context

@login_required
@student_required
def take_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    student = Student.objects.get(user=request.user)

    if request.method == 'POST':
        form = CreateSolutionForm(data=request.POST)

        if form.is_valid():
            with transaction.atomic():
                student_solution = form.save(commit=False)
                student_solution.student = student
                student_solution.problem = problem

                input_file = Problem.objects.get(id=student_solution.problem.id).input_data
                output_file = Problem.objects.get(id=student_solution.problem.id).output_data

                solution_code = student_solution.solution_code
                max_execution_time = student_solution.problem.max_execution_time

                test_score_percentage = test_student_solution(
                    code=solution_code,
                    exec_time=max_execution_time,
                    file_in=input_file,
                    file_out=output_file
                )

                score = round(test_score_percentage * problem.problem_value, 1)

                print(timezone.now() > problem.deadline)
                if timezone.now() > problem.deadline:
                    print(score)
                    score = round(score / 2, 1)
                    print(score)

                previous_solution = Solution.objects.filter(student=student).filter(problem=problem)
                print(previous_solution)
                if previous_solution:
                    if score > previous_solution[0].score:
                        previous_solution.delete()
                        student_solution.score = score
                        student_solution.save()
                else:
                    student_solution.score = score
                    student_solution.save()

                return redirect('students:problem_list')
    else:
        form = CreateSolutionForm()

    return render(request, 'students/solution_form.html', {
        'problem': problem,
        'form': form,
    })


@method_decorator([login_required, student_required], name='dispatch')
class LectureListView(ListView):
    model = Lecture
    ordering = ('date', )
    context_object_name = 'lectures'
    template_name = 'students/lecture_list.html'

    def get_queryset(self):
        queryset = Lecture.objects.all()
        return queryset
