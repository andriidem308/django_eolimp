from django.conf import settings
from django.db import models
from django.forms import TextInput


User = settings.AUTH_USER_MODEL


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user._teacher = True

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return self.user.get_full_name()


class Group(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=255)

    class Meta:
        ordering = ['group_name']

    def __str__(self):
        return self.group_name


class Problem(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group)
    title = models.CharField(max_length=255)
    description = models.TextField()

    problem_value = models.FloatField()
    # max_execution_time = models.FloatField()

    deadline = models.DateTimeField()
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)

    need_to_check = models.BooleanField(null=True)

    class Meta:
        ordering = ['date_created']


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user._student = True
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return self.user.get_full_name()

    def get_group(self):
        return self.group_id

    def get_group_name(self):
        return self.group_id.group_name


class Solution(models.Model):
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    solution_code = models.TextField()
    score = models.FloatField()
    date_solved = models.DateTimeField(auto_now=True)
    checked = models.BooleanField(default=False, null=True)

    class Meta:
        ordering = ['date_solved']

    def get_owner(self):
        return self.student_id

    def get_owner_name(self):
        return self.student_id.user.get_full_name()


class Lecture(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return self.title


class Attachment(models.Model):
    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    attachment_file = models.FileField(null=True)

    class Meta:
        ordering = ['pk']


class ProblemTest(models.Model):
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_data = models.FileField(null=True)
    output_data = models.FileField(null=True)

    class Meta:
        ordering = ['pk']
