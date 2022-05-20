from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
# from rest_framework.views import APIView

from .serializers import *


class TeacherRetrieveView(generics.RetrieveAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherUpdateView(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = CreateTeacherSerializer


class TeacherCreateView(generics.CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = CreateTeacherSerializer


class TeacherListView(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class StudentRetrieveView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentUpdateView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = CreateStudentSerializer


class StudentCreateView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = CreateStudentSerializer


class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class GroupRetrieveView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupUpdateView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = CreateGroupSerializer


class GroupCreateView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = CreateGroupSerializer


class GroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProblemRetrieveView(generics.RetrieveAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class ProblemUpdateView(generics.ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class ProblemCreateView(generics.CreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = CreateProblemSerializer


class ProblemListView(generics.ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class SolutionRetrieveView(generics.RetrieveAPIView):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer


class SolutionUpdateView(generics.ListAPIView):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer


class SolutionListView(generics.ListAPIView):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer


class LectureRetrieveView(generics.RetrieveAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer


class LectureUpdateView(generics.ListAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer


class LectureCreateView(generics.CreateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = CreateLectureSerializer


class LectureListView(generics.ListAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer


# class AttachmentRetrieveView(generics.RetrieveAPIView):
#     queryset = Attachment.objects.all()
#     serializer_class = AttachmentSerializer
#
#
# class AttachmentUpdateView(generics.ListAPIView):
#     queryset = Attachment.objects.all()
#     serializer_class = AttachmentSerializer
#
#
# class AttachmentCreateView(generics.CreateAPIView):
#     queryset = Attachment.objects.all()
#     serializer_class = CreateAttachmentSerializer
#
#
# class AttachmentListView(generics.ListAPIView):
#     queryset = Attachment.objects.all()
#     serializer_class = AttachmentSerializer

# Create your views here.
