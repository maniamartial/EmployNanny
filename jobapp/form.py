from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django import forms

from .models import Rating
from .models import DirectContract
from django import forms
from .models import jobModel, ContractModel


from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


class jobPostingForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    hours_per_day = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_hours_per_day(self):
        hours_per_day = self.cleaned_data.get('hours_per_day')

        if hours_per_day and hours_per_day > 24:
            raise forms.ValidationError("Hours per day cannot exceed 24.")

        return hours_per_day

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')

        if start_date and start_date < timezone.now().date():
            raise forms.ValidationError("Start date cannot be in the past.")

        return start_date

    def clean(self):
        cleaned_data = super().clean()
        salary = cleaned_data.get('salary')

        if salary and int(salary) < 15120:
            raise forms.ValidationError(
                "Salary cannot be less than Ksh. 15,120.")

        return cleaned_data

    class Meta:
        model = jobModel
        fields = '__all__'
        exclude = ('employer', 'date_posted')
        widgets = {
            'job_description': forms.Textarea(attrs={'placeholder': 'Include all the tasks, number of children (if available), etc.'})
        }

    def save(self, commit=True):
        job_posting = super().save(commit=False)
        job_posting.employer = self.user
        if commit:
            job_posting.save()
        return job_posting


class JobForm(jobPostingForm):
    def __init__(self, *args, **kwargs):
        # Retrieve the user attribute from kwargs
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].disabled = True

        # Set the user attribute on the form instance
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk and self.user != self.instance.employer and not self.user.is_superuser:
            raise forms.ValidationError(
                "Only the creator or an admin can edit/delete this job."
            )
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

    def clean(self):
        cleaned_data = super().clean()
        salary = cleaned_data.get('salary')

        if salary and int(salary) < 15120:
            raise forms.ValidationError(
                "Salary cannot be less than Ksh. 15,120.")

        return cleaned_data

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')

        if start_date and start_date < timezone.now().date():
            raise forms.ValidationError("Start date cannot be in the past.")

        return start_date

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
