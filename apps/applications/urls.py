from django.urls import path
from . import views
app_name = "applications"
urlpatterns = [
    path("apply/<int:job_id>/", views.ApplyView.as_view(), name="apply"),
    path("mine/", views.MyApplicationsView.as_view(), name="my_applications"),
    path("received/", views.EmployerApplicationsView.as_view(), name="employer_applications"),
    path("<int:pk>/status/", views.ApplicationStatusUpdateView.as_view(), name="status"),
]
