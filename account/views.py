from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.mixins import LoginRequiredMixin
from my_blog import settings
from django.views import View
from django.contrib import messages
from settings.models import Setting
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


class Account(View):
    template_name = 'account/account.html'

    def get(self, request):
        return render(request, self.template_name)