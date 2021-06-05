from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.html import escape, mark_safe
# Create your models here.


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Task(models.Model):
    title = models.CharField('Назва:', max_length=30)
    condition = models.TextField('Умова')
    input_file = models.FileField('Вхідні дані', upload_to='files_uploaded/test_files')
    output_file = models.FileField('Вихідні дані', upload_to='files_uploaded/test_files')


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    tasks = models.ManyToManyField(Task, through='TakenTask')

    # def get_unsolved_tasks(self, all_tasks):
    #     taken_tasks = self.taken_tasks
    #     unsolved_tasks = all_tasks.exclude(pk__in=taken_tasks).order_by('title')
    #     return unsolved_tasks

    def __str__(self):
        return self.user.username


class TakenTask(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='taken_tasks')
    score = models.FloatField(default=0)


class Solution(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='task_solutions')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='solutions')
    text = models.TextField(default='')


class Material(models.Model):
    title = models.CharField('Тема', max_length=30)
    description = models.TextField('Короткий опис')
    attachment = models.FileField('Додаток', upload_to='files_uploaded/material_files/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

