from django.urls import include, path

from .api_views import *


urlpatterns = [
    path('teachers/<int:pk>', TeacherRetrieveView.as_view()),
    path('teachers/update/<int:pk>', TeacherUpdateView.as_view()),
    path('teachers/all/', TeacherListView.as_view()),
    path('teachers/new', TeacherCreateView.as_view()),

    path('students/<int:pk>', StudentRetrieveView.as_view()),
    path('students/update/<int:pk>', StudentUpdateView.as_view()),
    path('students/all/', StudentListView.as_view()),
    path('students/new', StudentCreateView.as_view()),

    path('groups/<int:pk>', GroupRetrieveView.as_view()),
    path('groups/update/<int:pk>', GroupUpdateView.as_view()),
    path('groups/all/', GroupListView.as_view()),
    path('groups/new', GroupCreateView.as_view()),

    path('problems/<int:pk>', ProblemRetrieveView.as_view()),
    path('problems/update/<int:pk>', ProblemUpdateView.as_view()),
    path('problems/all/', ProblemListView.as_view()),
    path('problems/new', ProblemCreateView.as_view()),

    path('solutions/<int:pk>', SolutionRetrieveView.as_view()),
    path('solutions/update/<int:pk>', SolutionUpdateView.as_view()),
    path('solutions/all/', SolutionListView.as_view()),

    path('lectures/<int:pk>', LectureRetrieveView.as_view()),
    path('lectures/update/<int:pk>', LectureUpdateView.as_view()),
    path('lectures/all/', LectureListView.as_view()),
    path('lectures/new', LectureCreateView.as_view()),

    # path('attachments/<int:pk>', AttachmentRetrieveView.as_view()),
    # path('attachments/update/<int:pk>', AttachmentUpdateView.as_view()),
    # path('attachments/all/', AttachmentListView.as_view()),
    # path('attachments/new', AttachmentCreateView.as_view()),
]

