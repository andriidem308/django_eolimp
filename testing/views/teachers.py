from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from testing.decorators import teacher_required
from testing.forms import TeacherSignUpForm, CreateProblemForm, LectureCreateForm
from testing.models import Problem, User, Lecture, Student, Solution, Group


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
    model = Problem
    ordering = ('title', )
    context_object_name = 'problems'
    template_name = 'teachers/problem_change_list.html'

    def get_queryset(self):
        queryset = Problem.objects.all()
        return queryset


@login_required
@teacher_required
def problem_add(request):
    if request.method == 'POST':
        form = CreateProblemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user, commit=False)
            return HttpResponseRedirect('../../')
    else:
        form = CreateProblemForm()
    return render(request, 'teachers/problem_add_form.html', {'form': form})


@method_decorator([login_required, teacher_required], name='dispatch')
class TaskUpdateView(UpdateView):
    model = Problem
    fields = ('groups', 'title', 'description', 'problem_value', 'deadline', 'input_data', 'output_data')
    context_object_name = 'problem'
    template_name = 'teachers/problem_change_form.html'

    def get_queryset(self):
        return Problem.objects.all()

    def get_success_url(self):
        return reverse('teachers:task_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, teacher_required], name='dispatch')
class LectureListView(ListView):
    model = Lecture
    ordering = ('date', )
    context_object_name = 'lectures'
    template_name = 'teachers/lecture_change_list.html'

    def get_queryset(self):
        queryset = Lecture.objects.all()
        return queryset


@login_required
@teacher_required
def lecture_add(request):
    if request.method == 'POST':
        form = LectureCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user, commit=False)
            return HttpResponseRedirect('../../')
    else:
        form = LectureCreateForm()
    return render(request, 'teachers/lecture_add_form.html', {'form': form})


@method_decorator([login_required, teacher_required], name='dispatch')
class LectureUpdateView(UpdateView):
    model = Lecture
    fields = ('title', 'description')
    context_object_name = 'lectures'
    template_name = 'teachers/lecture_change_form.html'

    def get_queryset(self):
        return Lecture.objects.all()

    def get_success_url(self):
        return reverse('teachers:material_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, teacher_required], name='dispatch')
class GroupsListView(ListView):
    model = Group
    ordering = ('group_name', )
    context_object_name = 'groups'
    template_name = 'teachers/groups_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = Group.objects.filter(teacher_id__user_id=user.pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = Student.objects.all()
        data = {student: {} for student in students}

        for i, student in enumerate(students):
            solutions = Solution.objects.filter(student_id=student.pk)
            data[student]['total_solutions_score'] = sum([solution.score for solution in solutions])
            data[student]['total_problems_points'] = sum([solution.problem_id.problem_value for solution in solutions])
            data[student]['first_name'] = student.user.first_name
            data[student]['last_name'] = student.user.last_name

        context['data'] = data
        return context


@method_decorator([login_required, teacher_required], name='dispatch')
class StudentsListView(ListView):
    model = Student
    ordering = ('first_name', )
    context_object_name = 'students'
    template_name = 'teachers/students_list.html'

    def get_queryset(self):
        return Student.objects.filter(group=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = self.get_queryset()
        data = {student: {} for student in students}

        for i, student in enumerate(students):
            solutions = Solution.objects.filter(student_id=student.pk)
            data[student]['total_solutions_score'] = sum([solution.score for solution in solutions])
            data[student]['total_problems_points'] = sum([solution.problem_id.problem_value for solution in solutions])
            data[student]['first_name'] = student.user.first_name
            data[student]['last_name'] = student.user.last_name

        context['data'] = data
        context['group_title'] = Group.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('teachers:group', kwargs={'pk': self.object.pk})



