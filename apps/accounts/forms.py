from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Profile, phone_validator

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("phone_number", "is_staff", "is_superuser")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"

class PhoneForm(forms.Form):
    phone_number = forms.CharField(label="شماره موبایل", max_length=11, validators=[phone_validator])

class OtpVerifyForm(forms.Form):
    phone_number = forms.CharField(widget=forms.HiddenInput(), validators=[phone_validator])
    code = forms.CharField(label="کد تأیید", min_length=6, max_length=6)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "email", "avatar", "resume", "birth_date", "bio")
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "bio": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_resume(self):
        f = self.cleaned_data.get("resume")
        if f:
            if f.size > 5 * 1024 * 1024:
                raise forms.ValidationError("حجم رزومه نباید بیشتر از ۵ مگابایت باشد.")
            if not f.name.lower().endswith(".pdf"):
                raise forms.ValidationError("فقط فایل PDF پذیرفته می‌شود.")
            if f.content_type not in ("application/pdf", "application/octet-stream"):
                raise forms.ValidationError("فایل انتخاب‌شده PDF معتبر نیست.")
        return f
