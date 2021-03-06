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


class CreateGroupForm(forms.ModelForm):
    group_name = forms.CharField(max_length=255, widget=forms.TextInput())

    def __init__(self, teacher, *args, **kwargs):
        super(CreateGroupForm, self).__init__(*args, **kwargs)
        self.fields['group_name'].label = 'Назва групи'

    class Meta:
        model = Group
        fields = ['group_name']

    def save(self, **kwargs):
        user = kwargs.pop('user')
        instance = super(CreateGroupForm, self).save(**kwargs)
        instance.teacher = Teacher.objects.get(user=user)
        instance.save()
        return instance


class CreateProblemForm(forms.ModelForm):
    title = forms.CharField(max_length=255, widget=forms.TextInput())
    description = forms.Textarea()
    problem_value = forms.FloatField(widget=forms.NumberInput(attrs={'min': 0}))
    max_execution_time = forms.FloatField(widget=forms.NumberInput(attrs={'min': 0, 'step': 100}))
    deadline = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:00:00'],
        widget=BootstrapDateTimePickerInput(attrs={'autocomplete': 'off'})
    )
    input_data = forms.FileField()
    output_data = forms.FileField()

    def __init__(self, teacher, *args, **kwargs):
        super(CreateProblemForm, self).__init__(*args, **kwargs)
        self.fields['group'] = forms.ModelChoiceField(queryset=Group.objects.filter(teacher=teacher))
        self.fields['group'].label = ''
        self.fields['group'].empty_label = 'Оберіть групу'
        self.fields['title'].label = 'Назва задачі'
        self.fields['description'].label = 'Умова задачі'
        self.fields['problem_value'].label = 'Бал за задачу'
        self.fields['max_execution_time'].label = 'Максимальний час (у мс)'
        self.fields['deadline'].label = 'Дедлайн'
        self.fields['input_data'].label = 'Вхідні тести'
        self.fields['output_data'].label = 'Вихідні тести'

    class Meta:
        model = Problem
        fields = ['group', 'title', 'description', 'problem_value', 'max_execution_time', 'deadline', 'input_data', 'output_data']

    def save(self, **kwargs):
        user = kwargs.pop('user')
        instance = super(CreateProblemForm, self).save(**kwargs)
        instance.teacher = Teacher.objects.get(user=user)
        instance.save()
        return instance


class LectureCreateForm(forms.ModelForm):
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    description = forms.Textarea()
    attachment = forms.FileField(required=False)

    def __init__(self, teacher, *args, **kwargs):
        super(LectureCreateForm, self).__init__(*args, **kwargs)
        self.fields['group'] = forms.ModelChoiceField(queryset=Group.objects.filter(teacher=teacher))
        self.fields['group'].empty_label = 'Оберіть групу'
        self.fields['group'].label = ''
        self.fields['title'].label = 'Тема лекції'
        self.fields['description'].label = 'Вміст лекції'

    class Meta:
        model = Lecture
        fields = ['group', 'title', 'description', 'attachment']

    def save(self, **kwargs):
        user = kwargs.pop('user')
        instance = super(LectureCreateForm, self).save(**kwargs)
        instance.teacher = Teacher.objects.get(user=user)
        instance.save()
        return instance

