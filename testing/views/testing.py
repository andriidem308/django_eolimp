from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, User, UsernameField
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


from testing.models import User


class SignUpView(TemplateView):
    template_name = 'registration/signup_form.html'


@method_decorator([login_required], name='dispatch')
class AccountView(TemplateView):
    model = User
    context_object_name = 'user'
    template_name = 'registration/my_account.html'


def home(request):
    if request.user.is_authenticated:
        return redirect('my_account')
    return render(request, 'home.html')


class UserLoginView(LoginView):
    model = User
    form_class = AuthenticationForm
    template_name = 'registration/login.html'

