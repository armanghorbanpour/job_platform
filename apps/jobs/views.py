from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Job, Category
from .forms import JobForm

class JobListView(ListView):
    model = Job
    template_name = "jobs/job_list.html"
    context_object_name = "jobs"
    paginate_by = 12
    def get_queryset(self):
        qs = Job.objects.filter(is_active=True).select_related("category", "employer")
        q = self.request.GET.get("q", "").strip()
        city = self.request.GET.get("city", "").strip()
        category = self.request.GET.get("category", "").strip()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(company_name__icontains=q) | Q(description__icontains=q))
        if city: qs = qs.filter(city__icontains=city)
        if category: qs = qs.filter(category__slug=category)
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.filter(is_active=True)
        ctx.update({"q": self.request.GET.get("q", ""), "city": self.request.GET.get("city", "")})
        return ctx

class JobDetailView(DetailView):
    model = Job
    template_name = "jobs/job_detail.html"
    context_object_name = "job"
    def get_queryset(self):
        return Job.objects.filter(is_active=True).select_related("category", "employer")

class EmployerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.get_object().employer_id == self.request.user.id if hasattr(self, "get_object") else True

class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"
    success_url = reverse_lazy("jobs:my_jobs")
    def form_valid(self, form):
        form.instance.employer = self.request.user
        messages.success(self.request, "آگهی منتشر شد.")
        return super().form_valid(form)

class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"
    success_url = reverse_lazy("jobs:my_jobs")
    def test_func(self): return self.get_object().employer_id == self.request.user.id

class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = "jobs/job_confirm_delete.html"
    success_url = reverse_lazy("jobs:my_jobs")
    def test_func(self): return self.get_object().employer_id == self.request.user.id

class MyJobsView(LoginRequiredMixin, ListView):
    template_name = "jobs/my_jobs.html"
    context_object_name = "jobs"
    def get_queryset(self):
        return Job.objects.filter(employer=self.request.user).select_related("category")
