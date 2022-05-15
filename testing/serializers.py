from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class TeacherSerializer(serializers.Serializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'


class CreateTeacherSerializer(serializers.Serializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class StudentSerializer(serializers.Serializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = '__all__'


class CreateStudentSerializer(serializers.Serializer):
    class Meta:
        model = Student
        fields = '__all__'


class GroupSerializer(serializers.Serializer):
    teacher_id = TeacherSerializer()

    class Meta:
        model = Group
        fields = '__all__'

class CreateGroupSerializer(serializers.Serializer):
    class Meta:
        model = Group
        fields = '__all__'


class ProblemSerializer(serializers.Serializer):
    teacher_id = TeacherSerializer()
    groups = GroupSerializer()

    class Meta:
        model = Problem
        fields = '__all__'

class CreateProblemSerializer(serializers.Serializer):
    class Meta:
        model = Problem
        fields = '__all__'


class SolutionSerializer(serializers.Serializer):
    problem_id = ProblemSerializer()
    student_id = StudentSerializer()

    class Meta:
        model = Solution
        fields = ['student_id', 'problem_id', 'date_solved']



class LectureSerializer(serializers.Serializer):
    teacher_id = TeacherSerializer()

    class Meta:
        model = Lecture
        fields = '__all__'


class CreateLectureSerializer(serializers.Serializer):
    class Meta:
        model = Lecture
        fields = '__all__'


class AttachmentSerializer(serializers.Serializer):
    lecture_id = LectureSerializer()

    class Meta:
        model = Attachment
        fields = '__all__'


class CreateAttachmentSerializer(serializers.Serializer):
    class Meta:
        model = Attachment
        fields = '__all__'
