from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["name", "rating", "comment"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}),
            "rating": forms.RadioSelect(choices=[(i, "★" * i) for i in range(1, 6)]),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Write your review..."}),
        }
