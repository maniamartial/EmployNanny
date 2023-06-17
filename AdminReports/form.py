from jobapp.models import ContractModel, DirectContract

from django import forms


class ContractForm(forms.ModelForm):
    class Meta:
        model = ContractModel
        fields = ['duration', 'status']


class DirectContractForm(forms.ModelForm):
    class Meta:
        model = DirectContract
        fields = ['job_category', 'city', 'salary', 'start_date',
                  'end_date', 'job_description', 'status']
