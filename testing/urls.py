from django.shortcuts import redirect
from django.urls import include, path

from .views import testing, students, teachers
urlpatterns = [
    path('', testing.home, name='home'),

    path('students/', include(([
        path('', lambda request: redirect('my_account', permanent=True)),
        path('tasks/', students.TaskListView.as_view(), name='task_list'),
        path('taken/', students.SolutionListView.as_view(), name='taken_task_list'),
        path('tasks/<int:pk>/', students.take_task, name='take_task'),
        path('materials/', students.LectureListView.as_view(), name='material_list'),
    ], 'testing'), namespace='students')),

    path('teachers/', include(([
        path('', lambda request: redirect('my_account', permanent=True)),
        path('tasks/', teachers.TasksListView.as_view(), name='task_change_list'),
        path('tasks/add/', teachers.problem_add, name='task_add'),
        path('tasks/<int:pk>/', teachers.TaskUpdateView.as_view(), name='task_change'),
        path('materials/', teachers.LectureListView.as_view(), name='material_change_list'),
        path('materials/add/', teachers.lecture_add, name='material_add'),
        path('materials/<int:pk>/', teachers.LectureUpdateView.as_view(), name='material_change'),
        path('groups/', teachers.GroupsListView.as_view(), name='groups_list'),
        path('groups/<int:pk>/', teachers.StudentsListView.as_view(), name='group'),
        # path('students/', teachers.StudentsListView.as_view(), name='students_list')
    ], 'testing'), namespace='teachers')),

]

