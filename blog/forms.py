from django import forms
from .models import Blog, Blogcomment, BlogCommentReply


class create_blogpost_form(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class comment_form(forms.ModelForm):
    class Meta:
        model = Blogcomment
        fields = '__all__'

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 40%; height: 60px'})
        }

class commentreply_form(forms.ModelForm):
    class Meta:
        model = BlogCommentReply
        fields = '__all__'

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 40%; height: 60px'})
        }