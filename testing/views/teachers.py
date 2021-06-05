from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from ..decorators import teacher_required
from ..forms import TeacherSignUpForm, TaskCreateForm, MaterialCreateForm
from ..models import Task, User, Material, Student, TakenTask


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
    return render(request, 'teachers/task_add_form.html', {'form': form})


@method_decorator([login_required, teacher_required], name='dispatch')
class TaskUpdateView(UpdateView):
    model = Task
    fields = ('title', 'condition', 'input_file', 'output_file')
    context_object_name = 'task'
    template_name = 'teachers/task_change_form.html'

    def get_queryset(self):
        return Task.objects.all()

    def get_success_url(self):
        return reverse('teachers:task_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, teacher_required], name='dispatch')
class MaterialsListView(ListView):
    model = Material
    ordering = ('date', )
    context_object_name = 'materials'
    template_name = 'teachers/material_change_list.html'

    def get_queryset(self):
        queryset = Material.objects.all()
        return queryset


@login_required
@teacher_required
def material_add(request):
    if request.method == 'POST':
        form = MaterialCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../../')
    else:
        form = MaterialCreateForm()
    return render(request, 'teachers/material_add_form.html', {'form': form})


@method_decorator([login_required, teacher_required], name='dispatch')
class MaterialUpdateView(UpdateView):
    model = Material
    fields = ('title', 'description', 'attachment',)
    context_object_name = 'material'
    template_name = 'teachers/material_change_form.html'

    def get_queryset(self):
        return Material.objects.all()

    def get_success_url(self):
        return reverse('teachers:material_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, teacher_required], name='dispatch')
class StudentsListView(ListView):
    model = Student
    ordering = ('first_name', )
    context_object_name = 'students'
    template_name = 'teachers/students_list.html'

    def get_queryset(self):
        return Student.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = Student.objects.all()
        data = {}
        n = Task.objects.all().count()
        for i, st in enumerate(students):
            taken_tasks = TakenTask.objects.filter(student_id=st)
            if n == 0:
                s = 0
            else:
                s = round(sum([tt.score for tt in taken_tasks]) / n, 2)
            st.user.score = s
            data[st.user.username] = st.user

        context['data'] = data
        return context




