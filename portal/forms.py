from django import forms
from .models import Subscriber
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from .models import Post
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['category']


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'author',
        ]
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                "Описание не должно быть идентичным названию."
            )

        return cleaned_data
    
    def clean_name(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы."
            )
        return title

class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user

