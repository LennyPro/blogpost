from django import forms
from blog.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class EmailForm(forms.Form):
    name = forms.CharField(max_length=50)  # reformats to <input type='text'>
    email_from = forms.EmailField()  # reformats to <input type='email'>
    email_to = forms.EmailField()  # reformats to <input type='email'>
