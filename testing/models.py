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

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return self.title


class Attachment(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    attachment_file = models.FileField(null=True)

    class Meta:
        ordering = ['pk']


class ProblemTest(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_data = models.FileField(null=True)
    output_data = models.FileField(null=True)

    class Meta:
        ordering = ['pk']


class Choices(models.Model):
    choice = models.CharField(max_length=5000)
    is_answer = models.BooleanField(default=False)


class Questions(models.Model):
    question = models.CharField(max_length= 10000)
    question_type = models.CharField(max_length=20)
    required = models.BooleanField(default= False)
    answer_key = models.CharField(max_length = 5000, blank = True)
    score = models.IntegerField(blank = True, default=0)
    feedback = models.CharField(max_length = 5000, null = True)
    choices = models.ManyToManyField(Choices, related_name = "choices")


class Form(models.Model):
    code = models.CharField(max_length=30)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=10000, blank = True)
    creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "creator")
    background_color = models.CharField(max_length=20, default = "#d9efed")
    text_color = models.CharField(max_length=20, default="#272124")
    collect_email = models.BooleanField(default=False)
    authenticated_responder = models.BooleanField(default = False)
    edit_after_submit = models.BooleanField(default=False)
    confirmation_message = models.CharField(max_length = 10000, default = "Your response has been recorded.")
    is_quiz = models.BooleanField(default=False)
    allow_view_score = models.BooleanField(default= True)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    questions = models.ManyToManyField(Questions, related_name = "questions")
