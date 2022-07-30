from django import forms
from .models import Comment, Post



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class PostForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Post
 
        # specify fields to be used
        fields = [
            "title",
            'image',
            "content"]