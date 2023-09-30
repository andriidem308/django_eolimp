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
    group_name = models.CharField(max_length=255, unique=True)

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

    test_file = models.FileField(upload_to='files_uploaded/test_files/', null=True)

    class Meta:
        ordering = ['-date_updated']


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
        ordering = ['-date_updated']

    def __str__(self):
        return self.title


class EmailConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    passcode = models.CharField(max_length=6)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Test(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Answers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_1_text = models.CharField(max_length=255)
    answer_2_text = models.CharField(max_length=255)
    answer_3_text = models.CharField(max_length=255)
    answer_4_text = models.CharField(max_length=255)
    answer_1_correct = models.BooleanField(default=False, blank=True)
    answer_2_correct = models.BooleanField(default=False, blank=True)
    answer_3_correct = models.BooleanField(default=False, blank=True)
    answer_4_correct = models.BooleanField(default=False, blank=True)

