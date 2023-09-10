"""django_eolimp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from testing.views import testing, students, teachers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('testing.urls')),

    path('api/', include('api.urls')),

    # Accounts urls
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/my_account/', testing.AccountView.as_view(), name='my_account'),
    path('login/', testing.LoginView.as_view(), name='login'),
    path('accounts/signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/teacher/', teachers.TeacherSignUpView.as_view(), name='teacher_signup'),

    path('password_change/', testing.PasswordChangeView.as_view(), name='password_change'),

    path('__debug__/', include(debug_toolbar.urls))
]
