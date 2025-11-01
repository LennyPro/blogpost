from django import forms
from blog.models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

    author = forms.IntegerField(widget=forms.HiddenInput(), required=False)


class EmailForm(forms.Form):
    sender = forms.CharField(max_length=50)
    email_from = forms.EmailField()
    email_to = forms.EmailField()


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'status',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Name of the Poem'}),
            'body': forms.Textarea(attrs={'rows': 10, 'cols': 100}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'status']
