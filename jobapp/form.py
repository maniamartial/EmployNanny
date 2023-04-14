from django import forms
from .models import jobModel


class jobPostingForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model= jobModel
        fields='__all__'
        
        exclude=('employer', 'date_posted')
