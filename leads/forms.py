from django import forms
from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["customer", "title", "description", "status", "priority", "source", "estimated_value"]
        widgets = {
            "customer": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "source": forms.TextInput(attrs={"class": "form-control"}),
            "estimated_value": forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "0.01"}),
        }
