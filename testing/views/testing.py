import json
import os
import random

import yaml
from crispy_forms.helper import FormHelper
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from faker import Faker

from django.utils import timezone
from datetime import timedelta

from testing.models import User, Teacher, Student, Group, Problem, Lecture
from testing.services.logging_service import log_user

User = get_user_model()


class SignUpView(TemplateView):
    template_name = 'registration/signup_form.html'


@method_decorator([login_required], name='dispatch')
class AccountView(TemplateView):
    model = User
    context_object_name = 'user'
    template_name = 'registration/my_account.html'

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.is_teacher:
                context['teacher'] = Teacher.objects.get(user=user)
            elif user.is_student:
                context['student'] = Student.objects.get(user=user)
        return context


def home(request):
    if request.user.is_authenticated:
        return redirect('my_account')
    return render(request, 'home.html')


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)
        self.fields['username'].label = 'a cool label'
        self.fields['password'].label = 'another cool label'


class UserLoginView(LoginView):
    model = User
    form_class = CustomAuthenticationForm
    template_name = 'login.html'


def create_teachers(request):
    response_log = []

    config = yaml.safe_load(open('bot_config.yml').read())
    fake = Faker()

    number_of_teachers = config.get('number_of_teachers', 0)

    for _ in range(number_of_teachers):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        password = fake.password()

        user = User.objects.create_teacher_user(email, password, first_name, last_name)

        teacher = Teacher.objects.create(user=user)
        teacher.save()

        log_user(teacher, password)

        response_log.append(f'Created teacher: {teacher}')

    return JsonResponse(response_log, safe=False)


def create_groups(request):
    response_log = []

    config = yaml.safe_load(open('bot_config.yml').read())
    group_names = config.get('group_names', [])

    teachers = Teacher.objects.all()

    for group_name in group_names:
        for year in range(1, 5):
            teacher = random.choice(teachers)
            group_name_full = f'{group_name}-{year}'
            if not Group.objects.filter(group_name=group_name_full).exists():
                group = Group.objects.create(
                    teacher=teacher,
                    group_name=group_name_full
                )
                response_log.append(f'Created group: {group} with teacher {teacher}')

    return JsonResponse(response_log, safe=False)


def create_students(request):
    response_log = []

    config = yaml.safe_load(open('bot_config.yml').read())
    fake = Faker()

    max_students_per_group = config.get('max_students_per_group', 0)

    groups = Group.objects.all()

    for group in groups:
        current_amount_of_students = len(Student.objects.filter(group=group) or [])
        if current_amount_of_students < max_students_per_group:
            students_amount_to_add = random.randint(1, max_students_per_group - current_amount_of_students)
            for _ in range(students_amount_to_add):
                first_name = fake.first_name()
                last_name = fake.last_name()
                email = fake.email()
                password = fake.password()

                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_student_user(email, password, first_name, last_name)
                    student = Student.objects.create(user=user, group=group)
                    student.save()

                    log_user(student, password)

                    response_log.append(f'Created student: {student} in group {group}')

    return JsonResponse(response_log, safe=False)


def create_problems(request):
    response_log = []

    problems_data = json.load(open('problems_generator.json'))

    if not os.path.exists('files_uploaded'):
        os.mkdir('files_uploaded')

    if not os.path.exists('files_uploaded/test_files'):
        os.mkdir('files_uploaded/test_files')

    teachers = Teacher.objects.all()
    for teacher in teachers:
        groups = Group.objects.filter(teacher=teacher)
        for group in groups:
            for problem_data in problems_data:
                title = problem_data.get('title')
                condition = problem_data.get('condition')
                problem_value = random.randint(1, 10)
                max_exec_time = random.randrange(500, 5000, 500)
                time_now = timezone.now()
                random_days = timedelta(days=random.randint(0, 30))
                random_date = (time_now + random_days).replace(hour=0, minute=0, second=0, microsecond=0)

                test_filename = f'files_uploaded/test_files/{title}_{group}_{teacher}.json'

                with open(test_filename, 'w') as tmp_test_file:
                    tmp_test_file.write(json.dumps(problem_data.get('tests')))

                if not Problem.objects.filter(test_file=test_filename).exists():
                    Problem.objects.create(
                        teacher=teacher,
                        group=group,
                        title=title,
                        description=condition,
                        problem_value=problem_value,
                        max_execution_time=max_exec_time,
                        deadline=random_date,
                        date_created=time_now,
                        date_updated=time_now,
                        test_file=test_filename
                    )

                    response_log.append(f'Created problem: {title} in group {group} by teacher {teacher}')

    return JsonResponse(response_log, safe=False)


def create_lectures(request):
    response_log = []

    lectures_data = json.load(open('lectures_generator.json'))

    if not os.path.exists('files_uploaded'):
        os.mkdir('files_uploaded')

    if not os.path.exists('files_uploaded/attachments_files'):
        os.mkdir('files_uploaded/attachments_files')

    teachers = Teacher.objects.all()
    for teacher in teachers:
        groups = Group.objects.filter(teacher=teacher)
        for group in groups:
            for lecture_data in lectures_data:
                title = lecture_data.get('title')
                content = lecture_data.get('content')
                attachment = lecture_data.get("attachment")

                if not Lecture.objects.filter(
                        attachment=attachment).filter(title=title).filter(description=content).exists():
                    lecture = Lecture.objects.create(
                        teacher=teacher,
                        group=group,
                        title=title,
                        description=content,
                    )
                    if attachment:
                        lecture.attachment = f'files_uploaded/attachments_files/{attachment}'
                    lecture.save()

                    response_log.append(f'Created lecture: {title} in group {group} by teacher {teacher}')

    return JsonResponse(response_log, safe=False)
