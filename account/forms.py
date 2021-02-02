from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm
from datetime import timezone
from django import forms
from .models import *


message = {
    'invalid': 'please enter a valid email',
    'required': 'this field is required',
    'max_length': 'character for this field is too long'
}


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password(self):
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.EmailField(error_messages=message, widget=forms.TextInput(attrs={
        'class': 'form-control', 'style': 'width: 30% !important', 'placeholder': 'email'
    }))
    password = forms.CharField(error_messages={'required': 'this field is required'}, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'style': 'width: 30% !important', 'placeholder': 'password'
    }))
    remember = forms.CharField(label='remember me', required=False, widget=forms.CheckboxInput)


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')

        super().__init__(*args, **kwargs)
        
        if not user.is_superuser:
            self.fields['is_author'].disabled = True
            self.fields['special_user'].disabled = True

    class Meta:
        model = User
        fields = ('username', 'email', 'is_author', 'special_user')


class SignupForm(UserCreationForm):
    username = forms.CharField(error_messages=message, widget=forms.TextInput(attrs={
        'class': 'form-control', 'style': 'width: 30% !important', 'placeholder': 'Username'
    }))
    email = forms.EmailField(error_messages=message, widget=forms.TextInput(attrs={
        'class': 'form-control', 'style': 'width: 30% !important', 'placeholder': 'Email'
    }))
    password1 = forms.CharField(error_messages={'required': 'this field is required'}, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'style': 'width: 30% !important', 'placeholder': 'Password'
    }))
    password2 = forms.CharField(error_messages={'required': 'this field is required'}, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'style': 'width: 30% !important', 'placeholder': 'Confirm Password'
    }))

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError('This Username is already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('This Email is already exists')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Passwords must be match!')
        return password2

    class Meta:
        model = User
        fields = ('username', 'email')


    