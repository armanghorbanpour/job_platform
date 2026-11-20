from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    title = models.CharField(max_length=120, unique=True, verbose_name="عنوان")
    slug = models.SlugField(max_length=140, unique=True, allow_unicode=True)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.title
    class Meta:
        ordering = ("title",)
        verbose_name = "دسته شغلی"
        verbose_name_plural = "دسته‌های شغلی"

class Job(models.Model):
    EMPLOYMENT_TYPES = [
        ("full_time", "تمام‌وقت"), ("part_time", "پاره‌وقت"),
        ("remote", "دورکاری"), ("contract", "قراردادی"), ("internship", "کارآموزی"),
    ]
    EXPERIENCE = [
        ("no_experience", "بدون سابقه"), ("1_3", "۱ تا ۳ سال"),
        ("3_6", "۳ تا ۶ سال"), ("6_plus", "بیش از ۶ سال"),
    ]
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posted_jobs")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="jobs")
    title = models.CharField(max_length=180, verbose_name="عنوان شغلی")
    company_name = models.CharField(max_length=180, verbose_name="نام شرکت")
    city = models.CharField(max_length=100, verbose_name="شهر")
    description = models.TextField(verbose_name="شرح شغل")
    requirements = models.TextField(blank=True, verbose_name="شرایط احراز")
    benefits = models.TextField(blank=True, verbose_name="مزایا")
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES, default="full_time")
    experience = models.CharField(max_length=20, choices=EXPERIENCE, default="no_experience")
    min_salary = models.PositiveBigIntegerField(null=True, blank=True, verbose_name="حداقل حقوق (تومان)")
    max_salary = models.PositiveBigIntegerField(null=True, blank=True, verbose_name="حداکثر حقوق (تومان)")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        ordering = ("-created_at",)
        verbose_name = "آگهی شغلی"
        verbose_name_plural = "آگهی‌های شغلی"
    def __str__(self): return self.title
    @property
    def is_open(self):
        return self.is_active and (not self.expires_at or self.expires_at >= timezone.now())
