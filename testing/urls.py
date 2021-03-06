from django.shortcuts import redirect
from django.urls import include, path

from .views import testing, students, teachers

urlpatterns = [
    path('', testing.home, name='home'),

    path('students/', include(([
        path('', lambda request: redirect('my_account', permanent=True)),
        path('problems/', students.ProblemListView.as_view(), name='problem_list'),
        path('problems/<int:pk>/', students.take_problem, name='take_problem'),
        path('solutions/', students.SolutionListView.as_view(), name='solution_list'),
        path('lectures/', students.LectureListView.as_view(), name='lecture_list'),
        path('lectures/<int:pk>/', students.lecture_view, name='lecture_view'),
        path('lectures/<int:pk>/download_attachment/', students.attachment_download, name='attachment_download'),
    ], 'testing'), namespace='students')),

    path('teachers/', include(([
        path('', lambda request: redirect('my_account', permanent=True)),
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
    ], 'testing'), namespace='teachers')),

]

