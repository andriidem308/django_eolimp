# from eolimp_app.models import User
#
#
# def create_students_models(students_info):
#     for student in students_info:
#         username, email, password, first_name, last_name = student.strip().split(', ')
#         user = User.objects.create_user(username=username, email=email, password=password)
#         user.is_active = False
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()
#
#
# def create_teachers_models(teachers_info):
#     for teacher in teachers_info:
#         pass
#
#
# def create_problems_models(problems_info):
#     for problem in problems_info:
#         pass
#
#
# def create_lectures_models(lectures_info):
#     for lecture in lectures_info:
#         pass
