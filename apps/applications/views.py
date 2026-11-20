from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.base import ContentFile
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from apps.jobs.models import Job
from .models import Application
from .forms import ApplicationForm

class ApplyView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = "applications/apply.html"
    def dispatch(self, request, *args, **kwargs):
        self.job = get_object_or_404(Job, pk=kwargs["job_id"], is_active=True)
        if Application.objects.filter(job=self.job, applicant=request.user).exists():
            messages.info(request, "قبلاً برای این آگهی درخواست ثبت کرده‌اید.")
            return redirect("applications:my_applications")
        if self.job.employer_id == request.user.id:
            messages.error(request, "برای آگهی خودتان نمی‌توانید درخواست ارسال کنید.")
            return redirect("jobs:detail", pk=self.job.pk)
        if not hasattr(request.user, "profile") or not request.user.profile.resume:
            messages.error(request, "ابتدا رزومه PDF را در پروفایل بارگذاری کنید.")
            return redirect("accounts:profile")
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        profile = self.request.user.profile
        source = profile.resume
        source.open("rb")
        try:
            content = source.read()
        finally:
            source.close()
        application = form.save(commit=False)
        application.job = self.job
        application.applicant = self.request.user
        application.resume_snapshot.save(source.name.split("/")[-1], ContentFile(content), save=False)
        try:
            application.save()
        except IntegrityError:
            form.add_error(None, "برای این آگهی قبلاً درخواست ثبت کرده‌اید.")
            return self.form_invalid(form)
        messages.success(self.request, "درخواست استخدام با موفقیت ثبت شد.")
        return redirect("applications:my_applications")
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["job"] = self.job
        return ctx

class MyApplicationsView(LoginRequiredMixin, ListView):
    template_name = "applications/my_applications.html"
    context_object_name = "applications"
    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user).select_related("job", "job__category")

class EmployerApplicationsView(LoginRequiredMixin, ListView):
    template_name = "applications/employer_applications.html"
    context_object_name = "applications"
    def get_queryset(self):
        queryset = Application.objects.filter(
            job__employer=self.request.user
        ).select_related(
            "job",
            "applicant",
            "applicant__profile")
        job_id = self.request.GET.get("job")
        if job_id:
            queryset = queryset.filter(job_id=job_id)
        return queryset

class ApplicationStatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Application
    fields = ("status",)
    template_name = "applications/status_form.html"
    success_url = reverse_lazy("applications:employer_applications")
    def test_func(self):
        return self.get_object().job.employer_id == self.request.user.id
