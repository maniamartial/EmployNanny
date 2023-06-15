from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from .models import Rating
from .models import DirectContract
from django import forms
from .models import jobModel, ContractModel


class jobPostingForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        salary = cleaned_data.get('salary')

        if salary and int(salary) < 10000:
            raise ValidationError("Salary cannot be less than 10,000.")

        return cleaned_data

    class Meta:
        model = jobModel
        fields = '__all__'

        exclude = ('employer', 'date_posted')
        widgets = {
            'job_description': forms.Textarea(attrs={'placeholder': 'Include all the tasks, number of children (if available), etc.'})
        }


class JobForm(jobPostingForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        # Disable editing of category field
        self.fields['category'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk and self.user != self.instance.employer:
            raise forms.ValidationError(
                "Only the creator can edit/delete this job.")
        return cleaned_data


'''class ContractForm(forms.ModelForm):
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = ContractModel
        #fields = ["end_date", "status"]'''
CATEGORIES = (
    ('Full-time Nanny', 'full-time nanny'),
    ('Part-time Nanny', 'parttime nanny'),
    ('Live-in Nanny', 'live-in nanny'),
    ('Live-out Nanny', 'Live-out Nanny'),
    ('Night Nanny', 'night nanny')
)


class JobSearchForm(forms.Form):
    category_query = forms.ChoiceField(choices=CATEGORIES)
    min_salary = forms.IntegerField(widget=forms.NumberInput(
        attrs={'type': 'number', 'class': 'form-control', 'placeholder': 'Min Salary'}), required=False)


# direct contract form


class DirectContractForm(forms.ModelForm):
    class Meta:
        model = DirectContract
        fields = ['job_category', 'city', 'salary', 'start_date',
                  'end_date', 'job_description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }


#Ratings and comments


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('stars', 'comment')

    stars = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'id': 'star-rating'}),
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Media:
        css = {
            'all': ('css/star-rating.css',)
        }
        js = ('js/star-rating.js',)

    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your comment'
        })
    )
