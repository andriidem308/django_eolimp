from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.serializers import TeacherSerializer, ProblemSerializer, LectureSerializer, SolutionSerializer, \
    StudentSerializer
from testing.models import Teacher, Solution, Student, Problem, Lecture


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.select_related('user')
    serializer_class = TeacherSerializer

    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        return super(TeacherViewSet, self).retrieve(request)

    def list(self, request, *args, **kwargs):
        return super(TeacherViewSet, self).list(request)

    def update(self, request, *args, **kwargs):
        return super(TeacherViewSet, self).update(request)

    def partial_update(self, request, *args, **kwargs):
        return super(TeacherViewSet, self).partial_update(request)

    def destroy(self, request, *args, **kwargs):
        return super(TeacherViewSet, self).destroy(request)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('user').select_related('group')
    serializer_class = StudentSerializer

    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        return super(StudentViewSet, self).retrieve(request)

    def list(self, request, *args, **kwargs):
        return super(StudentViewSet, self).list(request)

    def update(self, request, *args, **kwargs):
        return super(StudentViewSet, self).update(request)

    def partial_update(self, request, *args, **kwargs):
        return super(StudentViewSet, self).partial_update(request)

    def destroy(self, request, *args, **kwargs):
        return super(StudentViewSet, self).destroy(request)


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.select_related('teacher').select_related('group')
    serializer_class = ProblemSerializer

    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        return super(ProblemViewSet, self).retrieve(request)

    def list(self, request, *args, **kwargs):
        return super(ProblemViewSet, self).list(request)

    def update(self, request, *args, **kwargs):
        return super(ProblemViewSet, self).update(request)

    def partial_update(self, request, *args, **kwargs):
        return super(ProblemViewSet, self).partial_update(request)

    def destroy(self, request, *args, **kwargs):
        return super(ProblemViewSet, self).destroy(request)


class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.select_related('teacher').select_related('group')
    serializer_class = LectureSerializer

    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        return super(LectureViewSet, self).retrieve(request)

    def list(self, request, *args, **kwargs):
        return super(LectureViewSet, self).list(request)

    def update(self, request, *args, **kwargs):
        return super(LectureViewSet, self).update(request)

    def partial_update(self, request, *args, **kwargs):
        return super(LectureViewSet, self).partial_update(request)

    def destroy(self, request, *args, **kwargs):
        return super(LectureViewSet, self).destroy(request)


class SolutionsViewSet(viewsets.ModelViewSet):
    queryset = Solution.objects.select_related('student').select_related('problem')
    serializer_class = SolutionSerializer

    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        return super(SolutionsViewSet, self).retrieve(request)

    def list(self, request, *args, **kwargs):
        return super(SolutionsViewSet, self).list(request)

    def update(self, request, *args, **kwargs):
        return super(SolutionsViewSet, self).update(request)

    def partial_update(self, request, *args, **kwargs):
        return super(SolutionsViewSet, self).partial_update(request)

    def destroy(self, request, *args, **kwargs):
        return super(SolutionsViewSet, self).destroy(request)
