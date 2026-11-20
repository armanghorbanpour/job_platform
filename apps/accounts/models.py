from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from django.core.validators import RegexValidator

phone_validator = RegexValidator(r"^09\d{9}$", "شماره موبایل باید با 09 شروع شود و ۱۱ رقم باشد.")

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("شماره موبایل الزامی است.")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password) if password else user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        if not password:
            raise ValueError("رمز عبور مدیر الزامی است.")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if not extra_fields["is_staff"] or not extra_fields["is_superuser"]:
            raise ValueError("مدیر باید دسترسی مدیریتی داشته باشد.")
        return self.create_user(phone_number, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True, validators=[phone_validator], verbose_name="شماره موبایل")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_staff = models.BooleanField(default=False, verbose_name="دسترسی مدیریت")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ عضویت")
    objects = UserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100, blank=True, verbose_name="نام")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="نام خانوادگی")
    email = models.EmailField(blank=True, verbose_name="ایمیل")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="تصویر")
    resume = models.FileField(upload_to="resumes/", blank=True, null=True, verbose_name="رزومه PDF")
    birth_date = models.DateField(blank=True, null=True, verbose_name="تاریخ تولد")
    bio = models.TextField(blank=True, verbose_name="درباره من")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.user.phone_number

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل‌ها"

class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, db_index=True, verbose_name="شماره موبایل")
    code = models.CharField(max_length=128, verbose_name="کد / هش کد")
    created = models.DateTimeField(auto_now_add=True)
    attempts = models.PositiveSmallIntegerField(default=0)
    class Meta:
        ordering = ["-created"]
        verbose_name = "کد ورود"
        verbose_name_plural = "کدهای ورود"
    def __str__(self):
        return f"{self.phone_number} - {self.code}"
