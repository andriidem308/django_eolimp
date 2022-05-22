from django.conf import settings
settings.configure('AUTH_USER_MODEL', 'accounts.User')

User = settings.AUTH_USER_MODEL

from testing.models import Student, Group



def create_students_models(students_info, group_id):
    for student in students_info:
        username, email, password, first_name, last_name = student.strip().split(', ')
        user = User.objects.create(username=username, email=email, password=password)
        user._student = True
        user.save()
        group = Group.objects.get(pk=group_id)
        student = Student.objects.create(user=user, group=group)


def create_teachers_models(teachers_info):
    for teacher in teachers_info:
        pass


def create_problems_models(problems_info):
    for problem in problems_info:
        pass


def create_lectures_models(lectures_info):
    for lecture in lectures_info:
        pass
