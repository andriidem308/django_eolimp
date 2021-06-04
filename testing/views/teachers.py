from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import teacher_required
from ..forms import TeacherSignUpForm
from ..models import Task, User


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teachers:task_change_list')


@method_decorator([login_required, teacher_required], name='dispatch')
class TasksListView(ListView):
    model = Task
    ordering = ('title', )
    context_object_name = 'tasks'
    template_name = 'teachers/task_change_list.html'

    def get_queryset(self):
        queryset = Task.objects.all()
        return queryset


@method_decorator([login_required, teacher_required], name='dispatch')
class TaskCreateView(CreateView):
    model = Task

    # input_text = ''
    # output_text = ''
    fields = ('title', 'condition')
    template_name = 'teachers/task_add_form.html'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.owner = self.request.user
        task.save()
        messages.success(self.request, 'Завдання було створено!.')
        return redirect('teachers:task_change', task.pk)


@method_decorator([login_required, teacher_required], name='dispatch')
class TaskUpdateView(UpdateView):
    model = Task
    fields = ('title', 'condition', )
    context_object_name = 'task'
    template_name = 'teachers/task_change_form.html'

    def get_queryset(self):
        """
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        """
        return Task.objects.all()

    def get_success_url(self):
        return reverse('teachers:task_change', kwargs={'pk': self.object.pk})

