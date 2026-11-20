from django.views.generic import TemplateView
from apps.jobs.models import Job, Category
class HomeView(TemplateView):
    template_name = "core/home.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["latest_jobs"] = Job.objects.filter(is_active=True).select_related("category")[:8]
        ctx["categories"] = Category.objects.filter(is_active=True)[:12]
        return ctx
