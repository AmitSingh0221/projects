from django import forms
from customers.models import Customer
from .models import Inquiry

class PublicInquiryForm(forms.Form):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    company = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    message = forms.CharField(min_length=10, widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}))

class InquiryCreateForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ["customer", "subject", "message"]
        widgets = {
            "customer": forms.Select(attrs={"class": "form-select"}),
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }
