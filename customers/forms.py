from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email", "phone", "company"]
        widgets = {name: forms.TextInput(attrs={"class": "form-control"}) for name in ["name", "phone", "company"]}
        widgets["email"] = forms.EmailInput(attrs={"class": "form-control"})
