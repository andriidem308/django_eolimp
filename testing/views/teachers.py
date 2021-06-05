from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import teacher_required, log_highlight
from ..forms import TeacherSignUpForm, TaskCreateForm
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


# @method_decorator([login_required, teacher_required], name='dispatch')
# class TaskCreateView(CreateView):
#     model = Task
#
#     fields = ('title', 'condition', 'input_file', 'output_file')
#     template_name = 'teachers/task_add_form.html'
#
#     def form_valid(self, form):
#         task = form.save(commit=False)
#         task.owner = self.request.user
#
#         # input_file = self.request.FILES['input_file']
#         # output_file = self.request.FILES['output_file']
#         #
#         # with open(f'input_file_{task.id}.txt', 'wb+') as destination:
#         #     for chunk in input_file.chunks():
#         #         destination.write(chunk)
#         #     log_highlight('FILE INPUT SAVED')
#         #
#         # with open(f'output_file_{task.id}.txt', 'wb+') as destination:
#         #     for chunk in output_file.chunks():
#         #         destination.write(chunk)
#         #     log_highlight('FILE OUTPUT SAVED')
#
#         task.save()
#         messages.success(self.request, 'Завдання було створено!.')
#         return redirect('teachers:task_change_list')


@login_required
@teacher_required
def task_add(request):
    if request.method == 'POST':
        form = TaskCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../../')
    else:
        form = TaskCreateForm()
        log_highlight('NOT LOADED!')
    return render(request, 'teachers/task_add_form.html', {'form': form})


@method_decorator([login_required, teacher_required], name='dispatch')
class TaskUpdateView(UpdateView):
    model = Task
    fields = ('title', 'condition', 'input_file', 'output_file')
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

