from django.shortcuts import redirect
from django.urls import include, path

from .views import testing, students, teachers

urlpatterns = [
    path('', testing.home, name='home'),

    path('students/', include(([
        path('', lambda request: redirect('my_account', permanent=True)),
        path('problems/', students.TaskListView.as_view(), name='problem_list'),
        path('problems/<int:pk>/', students.take_problem, name='take_problem'),
        path('solutions/', students.SolutionListView.as_view(), name='solution_list'),
        path('lectures/', students.LectureListView.as_view(), name='lecture_list'),
        path('lectures/<int:pk>/', students.lecture_view, name='lecture_view'),
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
        path('solutions/<int:pk>/', teachers.solution_view, name='solution_view'),
        path('solutions/<int:pk>/check/', teachers.solution_check, name='solution_check'),
        path('solutions/<int:pk>/download/', teachers.solution_download, name='solution_download'),
        path('tests/add/',teachers.add_form,name='add_form')
        # path('students/', teachers.StudentsListView.as_view(), name='students_list')
    ], 'testing'), namespace='teachers')),

]

