from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from django_eolimp.settings import SECRET_KEY_TEACHER
from testing.models import Student, Teacher, Group, Solution, Lecture, Problem

from testing.widget import BootstrapDateTimePickerInput


User = get_user_model()


class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"}),
                                 max_length=32, label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}),
                                max_length=32, label='')

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Пошта'}),
                             max_length=64, label='')
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логін'}),
                               max_length=32, label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
                                label='')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Підтвердження паролю'}), label='')

    secret_key = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Код доступу'}), label='')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email') + UserCreationForm.Meta.fields + ('secret_key', )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user._teacher = True
        user.save()
        teacher = Teacher.objects.create(user=user)
        return user

    def clean(self):
        super().clean()
        secret_key = self.cleaned_data.get('secret_key')
        if secret_key:
            if secret_key != SECRET_KEY_TEACHER:
                raise forms.ValidationError(
                    'You must be a teacher to sign up as a teacher!',
                    code='password_mismatch',
                )


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"}),
                                 max_length=32, label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}),
                                max_length=32, label='')
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логін'}),
                                max_length=32, label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Пошта'}),
                             max_length=64, label='')

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Підтвердження паролю'}), label='')

    group = forms.ModelChoiceField(queryset=Group.objects.all(), label="Група")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email') + UserCreationForm.Meta.fields + ('group', )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user._student = True
        user.save()
        student = Student.objects.create(user=user, group=self.cleaned_data['group'])
        return user


class CreateSolutionForm(forms.ModelForm):
    solution_code = forms.CharField(widget=forms.Textarea(), label='')

    class Meta:
        model = Solution
        fields = ['solution_code']


class CreateProblemForm(forms.ModelForm):
    # groups = forms.ModelChoiceField(queryset=Group.objects.filter(teacher=))
    title = forms.CharField(max_length=255)
    description = forms.Textarea()
    problem_value = forms.FloatField()
    deadline = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:00:00'],
        widget=BootstrapDateTimePickerInput()
    )
    input_data = forms.FileField()
    output_data = forms.FileField()

    def __init__(self, teacher, *args, **kwargs):
        super(CreateProblemForm, self).__init__(*args, **kwargs)
        self.fields['group'] = forms.ModelChoiceField(queryset=Group.objects.filter(teacher=teacher))

    class Meta:
        model = Problem
        fields = ['group', 'title', 'description', 'problem_value', 'deadline', 'input_data', 'output_data']

    def save(self, **kwargs):
        user = kwargs.pop('user')
        print('self:', self)
        instance = super(CreateProblemForm, self).save(**kwargs)
        instance.teacher = Teacher.objects.get(user=user)
        print(instance)
        instance.save()
        return instance


class LectureCreateForm(forms.ModelForm):
    title = forms.CharField(max_length=255)
    description = forms.Textarea()

    def __init__(self, teacher, *args, **kwargs):
        super(LectureCreateForm, self).__init__(*args, **kwargs)
        self.fields['group'] = forms.ModelChoiceField(queryset=Group.objects.filter(teacher=teacher))


    class Meta:
        model = Lecture
        fields = ['group', 'title', 'description']

    def save(self, **kwargs):
        user = kwargs.pop('user')
        instance = super(LectureCreateForm, self).save(**kwargs)
        instance.teacher = Teacher.objects.get(user=user)
        instance.save()
        return instance

