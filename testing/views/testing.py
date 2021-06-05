from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from ..models import User


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


@method_decorator([login_required], name='dispatch')
class AccountView(TemplateView):
    model = User
    context_object_name = 'user'
    template_name = 'registration/my_account.html'


def home(request):
    if request.user.is_authenticated:
        return redirect('my_account')
    return render(request, 'home.html')
