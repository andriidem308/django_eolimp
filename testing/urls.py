from django.shortcuts import redirect
from django.urls import include, path
from django.views.generic.base import RedirectView

from .views import testing, students, teachers
urlpatterns = [
    path('', testing.home, name='home'),

    path('students/', include(([
        path('', lambda request: redirect('my_account', permanent=True)),
        # path('', RedirectView.as_view(url='accounts/my_account'), name='my_account_'),
        path('tasks/', students.TaskListView.as_view(), name='task_list'),
        path('taken/', students.TakenTaskListView.as_view(), name='taken_task_list'),
        path('tasks/<int:pk>/', students.take_task, name='take_task'),
        path('materials/', students.MaterialListView.as_view(), name='material_list'),
        # path('materials/<int:pk>/', students.take_task, name='material_show')
    ], 'testing'), namespace='students')),

    path('teachers/', include(([
        path('', lambda request: redirect('my_account', permanent=True)),
        path('tasks/', teachers.TasksListView.as_view(), name='task_change_list'),
        path('tasks/add/', teachers.task_add, name='task_add'),
        path('tasks/<int:pk>/', teachers.TaskUpdateView.as_view(), name='task_change'),
        path('materials/', teachers.MaterialsListView.as_view(), name='material_change_list'),
        path('materials/add/', teachers.material_add, name='material_add'),
        path('materials/<int:pk>/', teachers.MaterialUpdateView.as_view(), name='material_change'),
        path('students/', teachers.StudentsListView.as_view(), name='students_list')
        # path('task/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='task_delete'),
    ], 'testing'), namespace='teachers')),

]

