import hashlib
import random

import bcrypt as bcrypt
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from authapp.models import ShopUser
from django import forms

import datetime


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'birthday', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_birthday(self):
        data = self.cleaned_data['birthday']
        if datetime.date.today().year - data.year < 18:
            raise forms.ValidationError("Вы слишком молоды!")

        return data

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)

        user.is_active = False
        # user.activation_key = bcrypt.hashpw(str(random.random()).encode('utf8'), bcrypt.gensalt())
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        print(user.activation_key)

        return user


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'email', 'birthday', 'avatar', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_birthday(self):
        data = self.cleaned_data['birthday']
        if datetime.date.today().year - data.year < 18:
            raise forms.ValidationError("Вы слишком молоды!")

        return data


class ShopUserProfileForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('first_name', 'last_name', 'avatar', 'username', 'email', 'birthday')

    def __init__(self, *args, **kwargs):
        super(ShopUserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def clean_birthday(self):
        data = self.cleaned_data['birthday']
        if datetime.date.today().year - data.year < 18:
            raise forms.ValidationError("Вы слишком молоды!")

        return data
