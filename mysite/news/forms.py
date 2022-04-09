from django import forms
from news.models import Category, News
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.urls import reverse
from captcha.fields import CaptchaField

class ContactForm(forms.Form):

    subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    captcha = CaptchaField()

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def get_absolute_url(self):
        return reverse('register')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# class NewsForm(forms.Form):  # не связана с моделью
#     title = forms.CharField(max_length=128, label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     content = forms.CharField(label='Текст', required=False, widget=forms.Textarea(
#         attrs={'class': 'form-control', 'rows': 5}))
#     is_published = forms.BooleanField(label='Опубликовано', initial=True, widget=forms.CheckboxInput(attrs={
#         'class': 'form-check-input'
#     }))
#     category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория',
#                                       empty_label='Выберите категорию',
#                                       widget=forms.Select(attrs={'class': 'form-control'
#                                                                  }))  # fk

class NewsForm(forms.ModelForm):  # связана
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория',
                                      empty_label='Выберите категорию')  # для настройки

    class Meta:
        model = News
        # fields = '__all__'
        fields = ['title', 'content', 'is_published', 'category', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title
