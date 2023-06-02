import os

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from testing.decorators import teacher_required
from testing.forms import TeacherSignUpForm, CreateProblemForm, CreateGroupForm, LectureCreateForm, UpdateProblemForm, \
    UpdateLectureForm, SolutionViewForm, TestCreateForm, QuestionFormSet, AnswersFormSet
from testing.models import Problem, User, Lecture, Student, Solution, Group, Teacher, Test
from testing.services.notifications import lecture_added_notify, problem_added_notify


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


@login_required
@teacher_required
def group_add(request):
    teacher = Teacher.objects.get(user=request.user)

    if request.method == 'POST':
        form = CreateGroupForm(teacher, request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user, commit=False)
            return HttpResponseRedirect('../')
    else:
        form = CreateGroupForm(teacher)
    return render(request, 'teachers/group_add_form.html', {'form': form})


@method_decorator([login_required, teacher_required], name='dispatch')
class ProblemsListView(ListView):
    model = Problem
    context_object_name = 'problems'
    template_name = 'teachers/problem_change_list.html'

    def get_queryset(self):
        teacher = Teacher.objects.get(user=self.request.user)
        problems = Problem.objects.filter(teacher=teacher)
        return problems


@login_required
@teacher_required
def problem_add(request):
    teacher = Teacher.objects.get(user=request.user)

    if request.method == 'POST':
        form = CreateProblemForm(teacher, request.POST, request.FILES)
        if form.is_valid():
            problem = form.save(user=request.user, commit=False)
            problem.save()
            problem_added_notify(problem)
            return HttpResponseRedirect('../')
    else:
        form = CreateProblemForm(teacher)
    return render(request, 'teachers/problem_add_form.html', {'form': form})


@method_decorator([login_required, teacher_required], name='dispatch')
class ProblemUpdateView(UpdateView):
    model = Problem
    form_class = UpdateProblemForm
    context_object_name = 'problem'
    template_name = 'teachers/problem_change_form.html'
    success_url = reverse_lazy('teachers:problem_change_list')

    def get_queryset(self):
        return Problem.objects.all()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        teacher = Teacher.objects.get(user=self.request.user)
        kwargs['teacher'] = teacher
        return kwargs

    def get_success_url(self):
        return reverse_lazy('teachers:problem_change_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['problem'] = Problem.objects.get(pk=self.kwargs['pk'])
        return context


@method_decorator([login_required, teacher_required], name='dispatch')
class LectureListView(ListView):
    model = Lecture
    context_object_name = 'lectures'
    template_name = 'teachers/lecture_change_list.html'

    def get_queryset(self):
        teacher = Teacher.objects.get(user=self.request.user)
        lectures = Lecture.objects.filter(teacher=teacher)
        return lectures


@login_required
@teacher_required
def lecture_add(request):
    teacher = Teacher.objects.get(user=request.user)

    if request.method == 'POST':
        form = LectureCreateForm(teacher, request.POST, request.FILES)
        if form.is_valid():
            lecture = form.save(user=request.user, commit=False)
            lecture.save()

            lecture_added_notify(lecture)

            return HttpResponseRedirect('../')
    else:
        form = LectureCreateForm(teacher)
    return render(request, 'teachers/lecture_add_form.html', {'form': form})


@method_decorator([login_required, teacher_required], name='dispatch')
class LectureUpdateView(UpdateView):
    model = Lecture
    form_class = UpdateLectureForm
    context_object_name = 'lecture'
    template_name = 'teachers/lecture_change_form.html'
    success_url = reverse_lazy('teachers:lecture_change_list')

    def get_queryset(self):
        return Lecture.objects.all()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        teacher = Teacher.objects.get(user=self.request.user)
        kwargs['teacher'] = teacher
        return kwargs

    def get_success_url(self):
        return reverse_lazy('teachers:lecture_change_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lecture'] = Lecture.objects.get(pk=self.kwargs['pk'])
        return context


@method_decorator([login_required, teacher_required], name='dispatch')
class GroupsListView(ListView):
    model = Group
    ordering = ('group_name',)
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
        return students.order_by('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        problem = Problem.objects.get(pk=self.kwargs['pk'])
        context['problem'] = problem

        solutions = Solution.objects.filter(problem=problem).order_by('checked', 'date_solved')
        students = [solution.student for solution in solutions]

        for student in self.get_queryset(**kwargs):
            if student not in students:
                students.append(student)

        data = {student: {} for student in students}

        for i, student in enumerate(students):
            solution = Solution.objects.filter(student=student).filter(problem=problem)

            if solution:
                data[student]['grade'] = f'{solution[0].score} / {problem.problem_value}'
                data[student]['solution'] = f'<u><a href="../../../solutions/{solution[0].pk}">Check solution</a></u>'
                data[student]['checked'] = f'{"Yes" if solution[0].checked else "No"}'
            else:
                data[student]['grade'] = f'No solution'
                data[student]['solution'] = 'No solution'
                data[student]['checked'] = 'No solution'

        context['data'] = data

        return context

    def get_success_url(self):
        return reverse('teachers:group', kwargs={'pk': self.object.pk})


@method_decorator([login_required, teacher_required], name='dispatch')
class SolutionUpdateView(UpdateView):
    model = Solution
    # fields = ('score',)
    form_class = SolutionViewForm
    context_object_name = 'solution'
    template_name = 'teachers/solution_change_form.html'

    def get_queryset(self):
        return Solution.objects.all()

    def get_success_url(self):
        problem = self.object.problem
        return reverse('teachers:solution_list', kwargs={'pk': problem.id})

    def get_context_data(self, **kwargs):
        context = super(SolutionUpdateView, self).get_context_data(**kwargs)
        solution = Solution.objects.get(pk=self.object.pk)
        context['code'] = solution.solution_code.replace('\r\n', '<br>').replace('    ', '&emsp;')
        return context

    def form_valid(self, form):
        problem = self.object.problem
        self.object.checked = True
        if form.cleaned_data.get('score') > problem.problem_value:
            solution = form.save(commit=False)
            solution.score = problem.problem_value
            solution.save()
        return super().form_valid(form)


@login_required
@teacher_required
def solution_download(request, pk):
    solution = Solution.objects.get(pk=pk)

    filename = '_'.join([
        solution.student.user.first_name.replace(' ', '_'),
        solution.student.user.last_name.replace(' ', '_'),
        'problem',
        str(solution.problem.id),
    ]) + '.py'

    open(filename, 'w').write(solution.solution_code)
    file_response = open(filename, 'rb')
    os.remove(filename)

    return FileResponse(file_response)


@method_decorator([login_required, teacher_required], name='dispatch')
class TestsListView(ListView):
    model = Test
    context_object_name = 'tests'
    template_name = 'teachers/test_list.html'

    def get_queryset(self):
        teacher = Teacher.objects.get(user=self.request.user)
        tests = Test.objects.filter(teacher=teacher)
        return tests


@login_required
@teacher_required
def test_add(request):
    teacher = Teacher.objects.get(user=request.user)

    if request.method == 'POST':
        test_form = TestCreateForm(teacher, request.POST)
        question_formset = QuestionFormSet(request.POST, prefix='questions')
        # answer_formset = AnswersFormSet(request.POST)
        answer_formset = AnswersFormSet(request.POST, initial=[{'question': question for question in question_formset}], prefix='answers')

        if test_form.is_valid() and question_formset.is_valid() and answer_formset.is_valid():
            test = test_form.save(user=request.user, commit=False)
            test.save()

            questions = question_formset.save(commit=False)
            answers = answer_formset.save(commit=False)

            for question, answers_group in zip(questions, answers):
                question.test = test
                question.save()

                answers_group.question = question
                answers_group.save()

                # answers = answer_formset.save(commit=False)
                # for answer in answers:
                #     answer.question = question
                #     answer.save()

            return redirect('teachers:test_change_list')
        else:
            return redirect('teachers:test_add')
    else:
        test_form = TestCreateForm(teacher)
        question_formset = QuestionFormSet(prefix='questions')
        answer_formset = AnswersFormSet(initial=[{'question': question for question in question_formset}], prefix='answers')

    context = {
        'test_form': test_form,
        # 'question_answer_formset': zip(question_formset, answer_formset),
        'question_formset': question_formset,
        'answer_formset': answer_formset,
    }

    return render(request, 'teachers/test_add.html', context)


@method_decorator([login_required, teacher_required], name='dispatch')
class TestUpdateView(UpdateView):
    model = Test
    fields = ('group', 'title')
    context_object_name = 'test'
    template_name = 'teachers/test_change_form.html'

    def get_queryset(self):
        user = self.request.user
        teacher = Teacher.objects.get(user=user)
        return Test.objects.filter(teacher=teacher)

    def get_success_url(self):
        return reverse('teachers:test_change', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = Test.objects.get(pk=self.kwargs['pk'])
        return context
