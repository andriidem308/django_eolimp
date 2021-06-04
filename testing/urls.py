from django.urls import include, path

from .views import testing, students, teachers

urlpatterns = [
    path('', testing.home, name='home'),

    path('students/', include(([
        path('', students.TaskListView.as_view(), name='task_list'),
        path('taken/', students.TakenTaskListView.as_view(), name='taken_task_list'),
        path('task/<int:pk>/', students.take_task, name='take_task')
    ], 'testing'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.TasksListView.as_view(), name='task_change_list'),
        path('task/add/', teachers.TaskCreateView.as_view(), name='task_add'),
        path('task/<int:pk>/', teachers.TaskUpdateView.as_view(), name='task_change'),
        # path('task/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='task_delete'),
    ], 'testing'), namespace='teachers')),

]