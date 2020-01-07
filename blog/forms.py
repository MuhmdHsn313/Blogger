from django import forms
from .models import Command, Post


class NewCommand(forms.ModelForm):
    class Meta:
        model = Command
        fields = ('title', 'body')


class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
