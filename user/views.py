from django.contrib.auth import get_user_model
from django.views.generic import CreateView

from user.forms import UserRegistrationForm


class UserRegistrationView(CreateView):
    model = get_user_model()
    form_class = UserRegistrationForm
    success_url = '/article/'

    # fields = ('email', 'name', 'password')
