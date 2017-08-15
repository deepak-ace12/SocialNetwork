from django import forms
from home.models import Post


class HomeForm(forms.ModelForm):
    post = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': "What's going on?",
            'rows': 3,
            'style': 'resize:none;',

        }
    ))

    class Meta:
        model = Post
        fields = ('post',)