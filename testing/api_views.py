from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from api.serializers import *


class TeacherRetrieveView(generics.RetrieveAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    authentication_classes = (TokenAuthentication,)


class TeacherUpdateView(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = CreateTeacherSerializer
    authentication_classes = (TokenAuthentication,)


class TeacherCreateView(generics.CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = CreateTeacherSerializer
    authentication_classes = (TokenAuthentication,)


class TeacherListView(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    authentication_classes = (TokenAuthentication,)


class StudentRetrieveView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = (TokenAuthentication,)


class StudentUpdateView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = CreateStudentSerializer
    authentication_classes = (TokenAuthentication,)


class StudentCreateView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = CreateStudentSerializer
    authentication_classes = (TokenAuthentication,)


class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = (TokenAuthentication,)


class GroupRetrieveView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = (TokenAuthentication,)


class GroupUpdateView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = CreateGroupSerializer
    authentication_classes = (TokenAuthentication,)


class GroupCreateView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = CreateGroupSerializer
    authentication_classes = (TokenAuthentication,)


class GroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = (TokenAuthentication,)


class ProblemRetrieveView(generics.RetrieveAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    authentication_classes = (TokenAuthentication,)


class ProblemUpdateView(generics.ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    authentication_classes = (TokenAuthentication,)


class ProblemCreateView(generics.CreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = CreateProblemSerializer
    authentication_classes = (TokenAuthentication,)


class ProblemListView(generics.ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    authentication_classes = (TokenAuthentication,)


class SolutionRetrieveView(generics.RetrieveAPIView):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    authentication_classes = (TokenAuthentication,)


class SolutionUpdateView(generics.ListAPIView):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    authentication_classes = (TokenAuthentication,)


class SolutionListView(generics.ListAPIView):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    authentication_classes = (TokenAuthentication,)


class LectureRetrieveView(generics.RetrieveAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    authentication_classes = (TokenAuthentication,)


class LectureUpdateView(generics.ListAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    authentication_classes = (TokenAuthentication,)


class LectureCreateView(generics.CreateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = CreateLectureSerializer
    authentication_classes = (TokenAuthentication,)


class LectureListView(generics.ListAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    authentication_classes = (TokenAuthentication,)

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
