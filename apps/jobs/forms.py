from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ("category", "title", "company_name", "city", "description", "requirements",
                  "benefits", "employment_type", "experience", "min_salary", "max_salary", "expires_at")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 6}),
            "requirements": forms.Textarea(attrs={"rows": 4}),
            "benefits": forms.Textarea(attrs={"rows": 3}),
            "expires_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
    def clean(self):
        data = super().clean()
        low, high = data.get("min_salary"), data.get("max_salary")
        if low and high and high < low:
            self.add_error("max_salary", "حداکثر حقوق نمی‌تواند کمتر از حداقل حقوق باشد.")
        return data
