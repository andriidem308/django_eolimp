from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.core.mail import send_mail
from django.db import transaction
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView


from django_eolimp.settings import EMAIL_HOST_USER
from testing.decorators import student_required
from testing.forms import StudentSignUpForm, CreateSolutionForm, EmailConfirmationForm
from testing.models import Problem, User, Solution, Lecture, Student, EmailConfirmation
from testing.services.code_solver import test_student_solution
from testing.services.verification import generate_passcode, send_verification_passcode


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'accounts/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        passcode = send_verification_passcode(user.email)
        EmailConfirmation.objects.create(user=user, passcode=passcode)
        login(self.request, user)
        return redirect('students:verify_email')


@login_required
def verify_email(request):
    email_confirmation = EmailConfirmation.objects.get(user=request.user)

    if email_confirmation.is_confirmed:
        return redirect('students:problem_list')

    if request.method == 'POST':
        form = EmailConfirmationForm(request.POST)
        if form.is_valid():
            passcode = form.cleaned_data['passcode']

            if email_confirmation.passcode == passcode:
                email_confirmation.is_confirmed = True
                email_confirmation.save()
                return redirect('students:problem_list')

    else:
        form = EmailConfirmationForm()

    return render(request, 'students/verify_email.html', {'form': form})


@method_decorator([login_required, student_required], name='dispatch')
class ProblemListView(ListView):
    model = Problem
    ordering = ('title',)
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

                test_file = Problem.objects.get(id=student_solution.problem.id).test_file

                solution_code = student_solution.solution_code
                max_execution_time = student_solution.problem.max_execution_time

                test_score_percentage = test_student_solution(
                    code=solution_code,
                    exec_time=max_execution_time,
                    test_filename=test_file,
                )

                score = round(test_score_percentage * problem.problem_value, 1)

                if timezone.now() > problem.deadline:
                    score = round(score / 2, 1)

                previous_solution = Solution.objects.filter(student=student).filter(problem=problem)
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
    ordering = ('date',)
    context_object_name = 'lectures'
    template_name = 'students/lecture_list.html'

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)
        queryset = Lecture.objects.filter(group=student.group)
        return queryset


@login_required
@student_required
def lecture_view(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk)
    return render(request, 'students/lecture_view.html', context={'lecture': lecture})


@login_required
@student_required
def attachment_download(request, pk):
    lecture = Lecture.objects.get(pk=pk)
    attachment_path = lecture.attachment.path
    filename = attachment_path.split('/')[-1]

    file_response = open(attachment_path, 'rb')

    return FileResponse(file_response, filename=filename)
