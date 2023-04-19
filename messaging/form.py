from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'subject', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5}),
        }
