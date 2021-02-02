from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate, login , logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy, reverse
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib import messages
from settings.models import Setting
from django.views import View
from my_blog import settings
from six import text_type
from core.models import *
from .mixins import *
from .models import *
from .forms import *
import requests


class Login(View):
    template_name = 'account/login.html'
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = self.form_class
        setting = Setting.objects.all()[0]
        return render(request, self.template_name, {'form': form, 'setting': setting})

    def post(self, request):
        form = self.form_class(request.POST)
        setting = Setting.objects.all()[0]
        next = request.GET.get('next')
        if form.is_valid():
            data = form.cleaned_data
            remember = form.cleaned_data['remember']
            user = authenticate(request, email=data['email'], password=data['password'])
            response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': response
            }
            info = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            auth = info.json()
            if auth['success']:
                if user is not None:
                    login(request, user)
                    if next:
                        return redirect(next)
                    if not remember:
                        request.session.set_expiry(0)
                    else:
                        request.session.set_expiry(68400)
                    return redirect('/')
                else:
                    form.add_error('email', 'user not found')
            else:
                messages.error(request, 'invalid recaptcha', 'danger')
        return render(request, self.template_name, {'form': form, 'setting': setting})


class Logout(LoginRequiredMixin, View):
    login_url = 'account:login'

    def get(self, request):
        logout(request)
        messages.success(request, 'logged out successfully', 'success')
        return redirect('/')


class Home(LoginRequiredMixin, ListView):
    template_name = 'account/account.html'
    login_url = 'account:login'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        elif self.request.user.is_admin:
            return Article.objects.filter(status='Published')
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(AuthorsAccessMixin, LoginRequiredMixin, FieldsMixin, FormValidMixin, CreateView):
    login_url = 'account:login'
    success_url = reverse_lazy('account:account')
    model = Article
    template_name = 'account/article-create-update.html'


class ArticleUpdate(AuthorAccessMixin, LoginRequiredMixin, FieldsMixin, FormValidMixin, UpdateView):
    login_url = 'account:login'
    success_url = reverse_lazy('account:account')
    model = Article
    template_name = 'account/article-create-update.html'


class DeleteArticle(LoginRequiredMixin, SuperUserMixin,  DeleteView):
    login_url = 'account:login'
    template_name = 'account/article_delete.html'
    model = Article
    success_url = reverse_lazy('account:account')


class UserProfile(LoginRequiredMixin, UpdateView):
    template_name = 'account/user_profile.html'
    login_url = 'account:login'
    model = User
    success_url = reverse_lazy('account:profile')
    form_class = ProfileForm

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class ChangePassword(LoginRequiredMixin, View):
    template_name = 'account/change_password.html'
    login_url = 'account:login'

    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        url = request.META.get('HTTP_REFERER')
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'your password changed successfully')
            return redirect(url)
        return render(request, self.template_name, {'form': form})


class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))

token_generator = EmailToken()


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('account/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send(fail_silently=False)
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'account/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


# class ResetPassword(auth_views.PasswordResetView):
#     template_name = 'forget_password/reset.html'
#     success_url = reverse_lazy('')
#     email_template_name = 'forget_password/link.html'


# class DonePassword(auth_views.PasswordResetDoneView):
#     pass
    