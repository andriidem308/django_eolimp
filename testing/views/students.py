from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView

from testing.decorators import student_required
from testing.forms import StudentSignUpForm, CreateSolutionForm
from testing.models import Problem, User, Solution, Lecture
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
        student = self.request.user.student
        taken_tasks = student.tasks.values_list('pk', flat=True)
        queryset = Problem.objects.exclude(pk__in=taken_tasks)
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class SolutionListView(ListView):
    model = Solution
    context_object_name = 'solutions'
    template_name = 'students/solution_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_tasks \
            .select_related('task').order_by('task__title')
        return queryset


@login_required
@student_required
def take_task(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    student = request.user.student

    if request.method == 'POST':
        form = CreateSolutionForm(data=request.POST)

        if form.is_valid():

            with transaction.atomic():
                student_solution = form.save(commit=False)
                student_solution.student = student
                student_solution.task = problem
                use_files = student_solution.use_files
                student_solution.save()

                input_file = student_solution.task.input_file.path
                output_file = student_solution.task.output_file.path

                if use_files:
                    try:
                        score = inp_out_file(student_solution.text, input_file, output_file)
                    except AssertionError:
                        messages.warning(request, 'Файл використовує стандартні потоки введення/виведення!')
                        return render(request, 'students/solution_form.html', {
                            'task': problem,
                            'form': form,
                        })

                else:
                    score = inp_out_cmd(student_solution.text, input_file, output_file)

                student_solution = Solution.objects.filter(student_id=student.pk)
                if student_solution.exists():
                    student_solution.update(score=score)
                else:
                    Solution.objects.create(problem_id=problem.pk, student_id=student.pk, task=problem, score=score)

                if score >= 75.0:
                    messages.success(request, 'Чудово! Ви пройшли %d відсотків тестів.' % score)
                else:
                    messages.warning(request, 'На жаль ви пройшли лише %d відсотків тестів.' % score)

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
