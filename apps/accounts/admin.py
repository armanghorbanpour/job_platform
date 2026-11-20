from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from .models import User, Profile, OtpCode
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    ordering = ("phone_number",)
    list_display = ("phone_number", "is_active", "is_staff", "date_joined")
    search_fields = ("phone_number",)
    fieldsets = (
        ("حساب", {"fields": ("phone_number", "password")}),
        ("دسترسی‌ها", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("تاریخ‌ها", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("phone_number", "password1", "password2", "is_staff", "is_superuser")}),)
    readonly_fields = ("date_joined", "last_login")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "email")
    search_fields = ("user__phone_number", "first_name", "last_name")

@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    search_fields = ("phone_number",)
    readonly_fields = ("created", "code")

    def get_list_display(self, request):
        if settings.DEBUG:
            return ("phone_number", "code", "created", "attempts")
        return ("phone_number", "created", "attempts")

    def get_queryset(self, request):
        return super().get_queryset(request)
