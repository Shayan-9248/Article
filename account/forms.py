from django import forms
from .models import *
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from datetime import timezone


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