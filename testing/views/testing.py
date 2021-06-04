from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth import logout as _logout


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('home')
        else:
            return redirect('home')
    return render(request, 'home.html')


def login(request):
    return render(request, 'registration/login.html')


def logout(request):
    _logout(request)
    return home


def signup(request):
    return render(request, 'registration/signup.html')


def signup_form(request):
    return render(request, 'registration/signup_form.html')