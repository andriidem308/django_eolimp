from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user._teacher = True

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return self.user.get_full_name()


class Group(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=255)

    class Meta:
        ordering = ['group_name']

    def __str__(self):
        return self.group_name


class Problem(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    problem_value = models.FloatField()
    max_execution_time = models.FloatField()  # ms

    deadline = models.DateTimeField()
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)

    input_data = models.FileField(upload_to='files_uploaded/test_files/', null=True)
    output_data = models.FileField(upload_to='files_uploaded/test_files/', null=True)

    class Meta:
        ordering = ['date_created']


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user._student = True
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return self.user.get_full_name()

    def get_group(self):
        return self.group

    def get_group_name(self):
        return self.group.group_name


class Solution(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    solution_code = models.TextField()
    score = models.FloatField()
    date_solved = models.DateTimeField(auto_now=True)
    checked = models.BooleanField(default=False, null=True)

    class Meta:
        ordering = ['date_solved']

    def get_owner(self):
        return self.student

    def get_owner_name(self):
        return self.student.user.get_full_name()


class Lecture(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)
    attachment = models.FileField(upload_to='files_uploaded/lectures_files', blank=True, null=True)

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return self.title
