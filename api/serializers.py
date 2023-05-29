from rest_framework import serializers
from testing.models import *
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'


class CreateTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()

    class Meta:
        model = Group
        fields = '__all__'


class CreateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    group = GroupSerializer()

    class Meta:
        model = Student
        fields = '__all__'


class CreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class ProblemSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    group = GroupSerializer()

    class Meta:
        model = Problem
        fields = '__all__'


class CreateProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'


class SolutionSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer()
    student = StudentSerializer()

    class Meta:
        model = Solution
        fields = '__all__'


class LectureSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    group = GroupSerializer()

    class Meta:
        model = Lecture
        fields = '__all__'


class CreateLectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'
