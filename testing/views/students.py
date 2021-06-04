from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from ..decorators import student_required
from ..forms import StudentSignUpForm, TakeTaskForm
from ..models import Task, Student, User, TakenTask


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
    model = Task
    ordering = ('title', )
    context_object_name = 'tasks'
    template_name = 'students/task_list.html'

    def get_queryset(self):
        # student = self.request.user.student
        # taken_tasks = student.tasks.values_list('pk', flat=True)
        queryset = Task.objects.all()
        # queryset = Task.objects.all() # exclude(pk__in=taken_tasks)
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class TakenTaskListView(ListView):
    model = TakenTask
    context_object_name = 'taken_tasks'
    template_name = 'students/taken_task_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_tasks \
            .select_related('task').order_by('task__title')
        return queryset


@login_required
@student_required
def take_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    student = request.user.student

    if student.tasks.filter(pk=pk).exists():
        return render(request, 'students/taken_task_list.html')

    if request.method == 'POST':
        form = TakeTaskForm()
        if form.is_valid():

            with transaction.atomic():
                student_solution = form.save(commit=False)
                student_solution.student = student
                student_solution.save()

                passed_tests, total_tests = 20, 24
                # passed_tests = 0
                score = round((passed_tests / total_tests) * 100.0, 2)
                TakenTask.objects.create(student=student, task=task, score=score)

                if score > 75.0:
                    messages.success(request, 'Чудово! Ви пройшли %d відсотків тестів.' % score)
                else:
                    messages.warning(request, 'На жаль ви пройшли лише %d відсотків тестів.' % score)

                return redirect('students:task_list')
    else:
        form = TakeTaskForm()

    return render(request, 'students/take_task_form.html', {
        'task': task,
        'form': form,
    })
