from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "review", "name", "email"]
        widgets = {
            "review": forms.Textarea(attrs={"rows": 3, "placeholder": "Write your review..."}),
            "name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Your email"}),
        }
