from django.shortcuts import redirect
from django.urls import include, path

from .views import testing, students, teachers
from .views.students import verify_email

urlpatterns = [
    path('', testing.home, name='home'),
    path('create_teachers/', testing.create_teachers, name='create_teachers_bot'),
    path('create_groups/', testing.create_groups, name='create_groups_bot'),
    path('create_students/', testing.create_students, name='create_students_bot'),
    path('create_problems/', testing.create_problems, name='create_problems_bot'),
    path('create_lectures/', testing.create_lectures, name='create_lectures_bot'),

    path('students/', include(([
                                   path('', lambda request: redirect('my_account', permanent=True)),
                                   path('verify-email/', verify_email, name='verify_email'),
                                   path('problems/', students.ProblemListView.as_view(), name='problem_list'),
                                   path('problems/<int:pk>/', students.take_problem, name='take_problem'),
                                   path('solutions/', students.SolutionListView.as_view(), name='solution_list'),
                                   path('lectures/', students.LectureListView.as_view(), name='lecture_list'),
                                   path('lectures/<int:pk>/', students.lecture_view, name='lecture_view'),
                                   path('lectures/<int:pk>/download_attachment/', students.attachment_download,
                                        name='attachment_download'),
                                   path('tests/', lambda request: redirect('my_account', permanent=True), name='test_list'),
                                   # path('tests/<int:pk>/', teachers.TestUpdateView.as_view(), name='test_solve'),
                               ], 'testing'), namespace='students')),

    path('teachers/', include(([

        path('', lambda request: redirect('my_account', permanent=True)),
        path('verify-email/', verify_email, name='verify_email'),
        path('problems/', teachers.ProblemsListView.as_view(), name='problem_change_list'),
        path('problems/add/', teachers.problem_add, name='problem_add'),
        path('problems/<int:pk>/', teachers.ProblemUpdateView.as_view(), name='problem_change'),
        path('lectures/', teachers.LectureListView.as_view(), name='lecture_change_list'),
        path('lectures/add/', teachers.lecture_add, name='lecture_add'),
        path('lectures/<int:pk>/', teachers.LectureUpdateView.as_view(), name='lecture_change'),
        path('groups/', teachers.GroupsListView.as_view(), name='groups_list'),
        path('groups/add/', teachers.group_add, name='group_add'),
        path('groups/<int:pk>/', teachers.StudentsListView.as_view(), name='group'),
        path('problems/<int:pk>/solutions/', teachers.StudentSolutionsListView.as_view(), name='solution_list'),
        path('solutions/<int:pk>/', teachers.SolutionUpdateView.as_view(), name='solution_change'),
        path('solutions/<int:pk>/download/', teachers.solution_download, name='solution_download'),
        path('tests/', teachers.TestsListView.as_view(), name='test_change_list'),
        # path('tests/add', lambda request: redirect('my_account', permanent=True), name='test_add'),
    ], 'testing'), namespace='teachers')),


]
