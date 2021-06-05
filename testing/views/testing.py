from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth import logout as _logout
from django.contrib.auth.decorators import login_required
from ..models import User


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class AccountView(TemplateView):
    model = User
    context_object_name = 'user'
    template_name = 'registration/my_account.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('home')
        else:
            return redirect('home')
    return render(request, 'home.html')


@login_required
def my_account(request):
    user = request.user
    return render(request, 'registration/my_account.html', context={'user': user})

def signup(request):
    return render(request, 'registration/signup.html')


def signup_form(request):
    return render(request, 'registration/signup_form.html')