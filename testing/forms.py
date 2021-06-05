from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from .models import Student, User, Task, Solution, TakenTask


class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"}),
                                 max_length=32, label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}),
                                max_length=32, label='')

    # username = forms.CharField(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логін'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Пошта'}),
                             max_length=64, label='')

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логін'}), label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
                                label='')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Підтвердження паролю'}), label='')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email',) + UserCreationForm.Meta.fields

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"}),
                                 max_length=32, label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}),
                                max_length=32, label='')

    # username = forms.CharField(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логін'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Пошта'}),
                             max_length=64, label='')

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логін'}), label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Підтвердження паролю'}), label='')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email',) + UserCreationForm.Meta.fields

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        return user


class TakeTaskForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(), label='')

    class Meta:
        model = Solution
        fields = ['text']


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'condition', 'input_file', 'output_file']


