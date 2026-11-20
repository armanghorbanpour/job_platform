from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, UpdateView
from .forms import PhoneForm, OtpVerifyForm, ProfileForm
from .models import Profile
from .utils import create_otp, verify_otp

class OtpRequestView(FormView):
    template_name = "accounts/otp_request.html"
    form_class = PhoneForm
    def form_valid(self, form):
        phone = form.cleaned_data["phone_number"]
        try:
            create_otp(phone)
        except Exception as exc:
            form.add_error(None, str(exc))
            return self.form_invalid(form)
        self.request.session["otp_phone"] = phone
        self.request.session["otp_next"] = self.request.GET.get("next", "")
        messages.success(self.request, "کد تأیید ارسال شد.")
        return redirect("accounts:verify_otp")

class OtpVerifyView(FormView):
    template_name = "accounts/otp_verify.html"
    form_class = OtpVerifyForm
    def get_initial(self):
        return {"phone_number": self.request.session.get("otp_phone", "")}
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("otp_phone"):
            return redirect("accounts:request_otp")
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        phone = self.request.session.get("otp_phone")
        ok, result = verify_otp(phone, form.cleaned_data["code"])
        if not ok:
            form.add_error("code", result)
            return self.form_invalid(form)
        login(self.request, result, backend="django.contrib.auth.backends.ModelBackend")
        self.request.session.pop("otp_phone", None)
        next_url = self.request.session.pop("otp_next", "")
        from django.utils.http import url_has_allowed_host_and_scheme
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return redirect(next_url)
        return redirect(self.get_success_url())
    def get_success_url(self):
        return self.request.GET.get("next") or reverse("core:home")

class LogoutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        return redirect("core:home")

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/profile_form.html"
    success_url = "/accounts/profile/"
    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile
    def form_valid(self, form):
        messages.success(self.request, "پروفایل ذخیره شد.")
        return super().form_valid(form)
