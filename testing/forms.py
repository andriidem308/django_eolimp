import logging

from django import forms
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, User, UsernameField
from django.db import transaction
from django.forms.models import formset_factory, inlineformset_factory

from django_eolimp.settings import SECRET_KEY_TEACHER
from testing.models import Student, Teacher, Group, Solution, Lecture, Problem, Test, Question, Answers
from testing.widget import BootstrapDateTimePickerInput

User = get_user_model()


class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Name"}),
                                 max_length=32, label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname'}),
                                max_length=32, label='')

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
                             max_length=64, label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                                label='')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'}), label='')

    secret_key = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Access code'}), label='')

    class Meta(UserCreationForm.Meta):
        model = User
        print("FIELDS:::::::::")
        print(UserCreationForm.Meta.fields)
        fields = ('first_name', 'last_name', 'email', 'secret_key',)

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
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Name"}),
                                 max_length=32, label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname'}),
                                max_length=32, label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
                             max_length=64, label='')

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                                label='')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'}), label='')

    group = forms.ModelChoiceField(queryset=Group.objects.all(), label='', empty_label='Select Group')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'group',)

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
        for field in self.fields.values():
            field.label = ''

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
    test_file = forms.FileField()

    def __init__(self, teacher, *args, **kwargs):
        super(CreateProblemForm, self).__init__(*args, **kwargs)
        # fields = ['group', 'title', 'description', 'problem_value', 'max_execution_time', 'deadline', 'input_data', 'output_data']
        self.fields['group'] = forms.ModelChoiceField(queryset=Group.objects.filter(teacher=teacher))
        for field in self.fields.values():
            field.label = ''

    class Meta:
        model = Problem
        fields = ['group', 'title', 'description', 'problem_value', 'max_execution_time', 'deadline', 'test_file']

    def save(self, **kwargs):
        user = kwargs.pop('user')
        instance = super(CreateProblemForm, self).save(**kwargs)
        instance.teacher = Teacher.objects.get(user=user)
        instance.save()
        return instance


class UpdateProblemForm(forms.ModelForm):
    def __init__(self, teacher, *args, **kwargs):
        super(UpdateProblemForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''

    class Meta:
        model = Problem
        fields = ['group', 'title', 'description', 'problem_value', 'max_execution_time', 'deadline', 'test_file']


class UpdateLectureForm(forms.ModelForm):
    def __init__(self, teacher, *args, **kwargs):
        super(UpdateLectureForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''

    class Meta:
        model = Lecture
        fields = ['group', 'title', 'description', 'attachment']


class LectureCreateForm(forms.ModelForm):
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    description = forms.Textarea()
    attachment = forms.FileField(required=False)

    def __init__(self, teacher, *args, **kwargs):
        super(LectureCreateForm, self).__init__(*args, **kwargs)
        self.fields['group'] = forms.ModelChoiceField(queryset=Group.objects.filter(teacher=teacher))
        for field in self.fields.values():
            field.label = ''

    class Meta:
        model = Lecture
        fields = ['group', 'title', 'description', 'attachment']

    def save(self, **kwargs):
        user = kwargs.pop('user')
        instance = super(LectureCreateForm, self).save(**kwargs)
        instance.teacher = Teacher.objects.get(user=user)
        instance.save()
        return instance


class SolutionViewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SolutionViewForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''

    class Meta:
        model = Solution
        fields = ['score']


class TestCreateForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['group', 'title']

    def __init__(self, teacher, *args, **kwargs):
        super(TestCreateForm, self).__init__(*args, **kwargs)
        self.fields['group'] = forms.ModelChoiceField(queryset=Group.objects.filter(teacher=teacher))
        for field in self.fields.values():
            field.label = ''

    def save(self, **kwargs):
        user = kwargs.pop('user')
        instance = super(TestCreateForm, self).save(**kwargs)
        instance.teacher = Teacher.objects.get(user=user)
        instance.save()
        return instance


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = {'text': forms.TextInput(attrs={'size': 80})}

    def __init__(self, *args, **kwargs):
        super(QuestionCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''


class AnswersCreateForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = ['question', 'answer_1_text', 'answer_2_text', 'answer_3_text', 'answer_4_text', 'answer_1_correct', 'answer_2_correct', 'answer_3_correct', 'answer_4_correct', ]

    def __init__(self, question, *args, **kwargs):
        super(AnswersCreateForm, self).__init__(*args, **kwargs)
        self.fields['question'] = question
        for field in self.fields.values():
            field.label = ''


QuestionFormSet = inlineformset_factory(Test, Question, form=QuestionCreateForm, extra=1, can_delete=True)
AnswersFormSet = inlineformset_factory(Question, Answers, form=AnswersCreateForm, extra=4, can_delete=False)
