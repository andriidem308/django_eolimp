import solution as solution
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView

from testing.decorators import student_required
from testing.forms import StudentSignUpForm, CreateSolutionForm
from testing.models import Problem, User, Solution, Lecture, Student
from testing.services.code_solver import inp_out_cmd, inp_out_file


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
        return redirect('students:task_list')


@method_decorator([login_required, student_required], name='dispatch')
class TaskListView(ListView):
    model = Problem
    ordering = ('title', )
    context_object_name = 'tasks'
    template_name = 'students/problem_list.html'

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)
        taken_tasks = Solution.objects.filter(student_id=student)
        problem_id_list = [taken_task.problem_id.id for taken_task in taken_tasks]
        queryset = Problem.objects.filter(groups__id=student.group_id).exclude(pk__in=problem_id_list)
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class SolutionListView(ListView):
    model = Solution
    context_object_name = 'solutions'
    template_name = 'students/solution_list.html'

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)
        queryset = Solution.objects.filter(student_id=student)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = Student.objects.get(user=self.request.user)
        solutions = Solution.objects.filter(student_id=student)

        context['points_sum'] = sum([sol.score for sol in solutions])
        context['points_total'] = sum([sol.problem_id.problem_value for sol in solutions])

        return context

@login_required
@student_required
def take_task(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    student = Student.objects.get(user=request.user)

    if request.method == 'POST':
        form = CreateSolutionForm(data=request.POST)

        if form.is_valid():
            with transaction.atomic():
                student_solution = form.save(commit=False)
                student_solution.student_id = student
                student_solution.problem_id = problem

                input_file = Problem.objects.get(id=student_solution.problem_id.id).input_data
                output_file = Problem.objects.get(id=student_solution.problem_id.id).output_data

                test_score_percentage = inp_out_cmd(student_solution.solution_code, input_file, output_file)

                score = round(test_score_percentage * problem.problem_value, 1)

                previous_solution = Solution.objects.filter(student_id=student)
                if previous_solution:
                    if score > previous_solution[0].score:
                        student_solution.score = score
                        student_solution.save()
                else:
                    student_solution.score = score
                    student_solution.save()

                return redirect('students:task_list')
    else:
        form = CreateSolutionForm()

    return render(request, 'students/solution_form.html', {
        'task': problem,
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
