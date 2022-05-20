from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from testing.decorators import teacher_required
from testing.forms import TeacherSignUpForm, CreateProblemForm, LectureCreateForm
from testing.models import Problem, User, Lecture, Student, Solution, Group, Teacher


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
        return redirect('teachers:problem_change_list')


@method_decorator([login_required, teacher_required], name='dispatch')
class ProblemsListView(ListView):
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
    teacher = Teacher.objects.get(user=request.user)

    if request.method == 'POST':
        form = CreateProblemForm(teacher, request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user, commit=False)
            return HttpResponseRedirect('../')
    else:
        form = CreateProblemForm(teacher)
    return render(request, 'teachers/problem_add_form.html', {'form': form})


@method_decorator([login_required, teacher_required], name='dispatch')
class ProblemUpdateView(UpdateView):
    model = Problem
    fields = (
        'group', 'title', 'description', 'problem_value', 'max_execution_time',
        'deadline', 'input_data', 'output_data'
    )
    context_object_name = 'problem'
    template_name = 'teachers/problem_change_form.html'

    def get_queryset(self):
        return Problem.objects.all()

    def get_success_url(self):
        return reverse('teachers:problem_change', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['problem'] = Problem.objects.get(pk=self.kwargs['pk'])
        return context


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
    teacher = Teacher.objects.get(user=request.user)

    if request.method == 'POST':
        form = LectureCreateForm(teacher, request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user, commit=False)
            return HttpResponseRedirect('../')
    else:
        form = LectureCreateForm(teacher)
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
        return reverse('teachers:lecture_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, teacher_required], name='dispatch')
class GroupsListView(ListView):
    model = Group
    ordering = ('group_name', )
    context_object_name = 'groups'
    template_name = 'teachers/groups_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = Group.objects.filter(teacher__user_id=user.pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = Student.objects.all()
        data = {student: {} for student in students}

        for i, student in enumerate(students):
            solutions = Solution.objects.filter(student=student.pk)
            data[student]['total_solutions_score'] = sum([solution.score for solution in solutions])
            data[student]['total_problems_points'] = sum([solution.problem.problem_value for solution in solutions])
            data[student]['first_name'] = student.user.first_name
            data[student]['last_name'] = student.user.last_name

        context['data'] = data
        return context


@method_decorator([login_required, teacher_required], name='dispatch')
class StudentsListView(ListView):
    model = Student
    ordering = ('last_name', 'first_name')
    context_object_name = 'students'
    template_name = 'teachers/students_list.html'

    def get_queryset(self):
        return Student.objects.filter(group=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = self.get_queryset()
        data = {student: {} for student in students}

        for i, student in enumerate(students):
            solutions = Solution.objects.filter(student=student.pk)
            data[student]['total_solutions_score'] = sum([solution.score for solution in solutions])
            data[student]['total_problems_points'] = sum([solution.problem.problem_value for solution in solutions])
            data[student]['first_name'] = student.user.first_name
            data[student]['last_name'] = student.user.last_name

        context['data'] = data
        context['group_title'] = Group.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('teachers:group', kwargs={'pk': self.object.pk})


@method_decorator([login_required, teacher_required], name='dispatch')
class StudentSolutionsListView(ListView):
    context_object_name = 'students'
    template_name = 'teachers/solution_list.html'

    def get_queryset(self, **kwargs):
        problem = Problem.objects.get(pk=self.kwargs['pk'])
        group = Group.objects.get(pk=problem.group.id)
        students = Student.objects.filter(group=group)
        return students

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        problem = Problem.objects.get(pk=self.kwargs['pk'])
        context['problem'] = problem

        students = self.get_queryset(**kwargs)

        data = {student: {} for student in students}

        for i, student in enumerate(students):
            solution = Solution.objects.filter(student=student).filter(problem=problem)

            if solution:
                data[student]['grade'] = f'{solution[0].score} / {problem.problem_value}'
                data[student]['solution'] = f'<a href="../../../solutions/{solution[0].pk}">Подивитись розв\'язок</a>'
            else:
                data[student]['grade'] = f'Немає оцінки'
                data[student]['solution'] = 'Немає розв\'язку'

        context['data'] = data

        return context

    def get_success_url(self):
        return reverse('teachers:group', kwargs={'pk': self.object.pk})

@login_required
@teacher_required
def view_solution(request, pk):
    solution = Solution.objects.get(pk=pk)
    context = {
        'solution': solution,
        'problem': Problem.objects.get(pk=solution.problem.id),
        'student': Student.objects.get(pk=solution.student.id),
        'code': solution.solution_code.replace('\r\n', '<br>').replace('    ', '&emsp;')
    }

    return render(request, 'teachers/view_solution.html', context=context)
