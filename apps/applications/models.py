
from django.conf import settings
from django.db import models
from django.utils import timezone
from apps.jobs.models import Job


def application_resume_path(instance, filename):
    return (
        f"application_resumes/{instance.applicant_id}/"
        f"{instance.job_id}/"
        f"{timezone.now():%Y%m%d%H%M%S}_{filename}"
    )

class Application(models.Model):

    STATUS = [
        ("submitted", "ثبت‌شده"),
        ("reviewing", "در حال بررسی"),
        ("interview", "دعوت به مصاحبه"),
        ("rejected", "رد شده"),
        ("accepted", "پذیرفته‌شده"),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    resume_snapshot = models.FileField(
        upload_to=application_resume_path,
        verbose_name="نسخه رزومه ارسالی"
    )

    cover_letter = models.TextField(
        blank=True,
        verbose_name="متن معرفی"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="submitted"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("job", "applicant"),
                name="unique_application_per_job"
            )
        ]

        ordering = ("-created_at",)
        verbose_name = "درخواست استخدام"
        verbose_name_plural = "درخواست‌های استخدام"

    def get_status_badge_class(self):
        colors = {
            "submitted": "bg-secondary",
            "reviewing": "bg-primary",
            "interview": "bg-info text-dark",
            "rejected": "bg-danger",
            "accepted": "bg-success",
        }

        return colors.get(self.status, "bg-secondary")

    def __str__(self):
        return f"{self.applicant} - {self.job}"
