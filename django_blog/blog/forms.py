# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from .models import Comment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

from .models import Post, Tag

class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Separate tags with commas")

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
        # Handle tags
        tags_str = self.cleaned_data.get('tags', '')
        tag_names = [name.strip() for name in tags_str.split(',') if name.strip()]
        tag_objs = []
        for name in tag_names:
            tag_obj, created = Tag.objects.get_or_create(name=name)
            tag_objs.append(tag_obj)
        post.tags.set(tag_objs)
        return post
