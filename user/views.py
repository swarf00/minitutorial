from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, FormView
from django.views.generic.base import TemplateView

from user.forms import UserRegistrationForm, LoginForm, VerificationEmailForm
from user.mixins import VerifyEmailMixin


class UserRegistrationView(VerifyEmailMixin, CreateView):
    model = get_user_model()
    form_class = UserRegistrationForm
    success_url = '/user/login/'
    verify_url = '/user/verify/'
    template_name = 'user/registration_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance:
            self.send_verification_email(form.instance)
        return response


class UserVerificationView(TemplateView):
    model = get_user_model()
    redirect_url = '/user/login/'
    token_generator = default_token_generator

    def get(self, request, *args, **kwargs):
        if self.is_valid_token(**kwargs):
            messages.info(request, '인증이 완료되었습니다.')
        else:
            messages.error(request, '인증이 실패되었습니다.', extra_tags='danger')
        return HttpResponseRedirect(self.redirect_url)

    def is_valid_token(self, **kwargs):
        pk = kwargs.get('pk')
        token = kwargs.get('token')
        user = self.model.objects.get(pk=pk)
        is_valid = self.token_generator.check_token(user, token)
        if is_valid:
            user.is_active = True
            user.save()
        return is_valid


class ResendVerifyEmailView(VerifyEmailMixin, FormView):
    model = get_user_model()
    form_class = VerificationEmailForm
    success_url = '/user/login/'
    template_name = 'user/resend_verify_form.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = self.model.objects.get(email=email)
        except self.model.DoesNotExist:
            messages.error(self.request, '알 수 없는 사용자 입니다.')
        else:
            self.send_verification_email(user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'user/login_form.html'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)