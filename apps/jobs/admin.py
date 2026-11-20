from django.contrib import admin
from .models import Category, Job
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active")
    prepopulated_fields = {"slug": ("title",)}
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company_name", "city", "employer", "is_active", "created_at")
    list_filter = ("is_active", "category", "employment_type", "city")
    search_fields = ("title", "company_name", "city")
