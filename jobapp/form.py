from .models import DirectContract
from django import forms
from .models import jobModel, ContractModel


class jobPostingForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = jobModel
        fields = '__all__'

        exclude = ('employer', 'date_posted')


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
