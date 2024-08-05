from django import forms
from lib.validators import min_length_validator
from shipping.models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ("city", "zipcode", "address", "number")

    def clean_zipcode(self):
        zipcode = self.cleaned_data["zipcode"]
        if len(zipcode) != 16:
            raise ValueError("Length is not 16")
        return zipcode

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
