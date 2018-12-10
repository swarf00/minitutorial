from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from user.forms import UserRegistrationForm, LoginForm


class UserRegistrationView(CreateView):
    model = get_user_model()
    form_class = UserRegistrationForm
    success_url = '/article/'


class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'user/login_form.html'
