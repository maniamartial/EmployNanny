
from django import forms
from .models import Payment
from django.core.exceptions import ValidationError


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ("phone_number", "amount", "description")

        def clean_phone_number(self):
            phone_number = self.cleaned_data["phone_number"]
            if len(str(phone_number)) < 10:
                raise ValidationError(
                    "Phone number must be at least 10 digits")
            return phone_number
