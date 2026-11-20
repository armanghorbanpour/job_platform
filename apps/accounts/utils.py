import secrets
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from decouple import config
from .models import OtpCode, User

OTP_TTL_MINUTES = 5
OTP_MAX_ATTEMPTS = 5
OTP_RESEND_SECONDS = 60

def generate_otp():
    return f"{secrets.randbelow(1_000_000):06d}"

def send_otp_code(phone_number, code):
    # در توسعه پیامک ارسال نمی‌شود؛ در production کلید API از env خوانده می‌شود.
    if not getattr(settings, "SEND_REAL_SMS", False):
        return {"status": "development", "message": "SMS disabled in development"}
    from kavenegar import KavenegarAPI, APIException, HTTPException
    api_key = config("KAVENEGAR_API_KEY")
    api = KavenegarAPI(api_key)
    try:
        return api.sms_send({
            "sender": config("KAVENEGAR_SENDER", default="2000660110"),
            "receptor": phone_number,
            "message": f"کد تأیید شما: {code}",
        })
    except (APIException, HTTPException) as exc:
        raise RuntimeError("ارسال پیامک ناموفق بود.") from exc

def create_otp(phone_number):
    now = timezone.now()
    last = OtpCode.objects.filter(phone_number=phone_number).order_by("-created").first()
    if last and (now - last.created).total_seconds() < OTP_RESEND_SECONDS:
        raise ValidationError("برای ارسال مجدد کد، کمی صبر کنید.")
    code = generate_otp()
    OtpCode.objects.filter(phone_number=phone_number).delete()
    stored_code = code if settings.DEBUG else make_password(code)
    OtpCode.objects.create(phone_number=phone_number, code=stored_code)
    try:
        send_otp_code(phone_number, code)
    except Exception:
        OtpCode.objects.filter(phone_number=phone_number, code=code).delete()
        raise
    return code

def verify_otp(phone_number, code):
    otp = OtpCode.objects.filter(phone_number=phone_number).order_by("-created").first()
    if not otp:
        return False, "کدی برای این شماره ثبت نشده است."
    if timezone.now() > otp.created + timedelta(minutes=OTP_TTL_MINUTES):
        otp.delete()
        return False, "اعتبار کد به پایان رسیده است."
    if otp.attempts >= OTP_MAX_ATTEMPTS:
        otp.delete()
        return False, "تعداد تلاش‌های ناموفق بیش از حد مجاز است."
    valid_code = secrets.compare_digest(otp.code, code) if settings.DEBUG else check_password(code, otp.code)
    if not valid_code:
        otp.attempts += 1
        otp.save(update_fields=["attempts"])
        return False, "کد واردشده صحیح نیست."
    otp.delete()
    user, _ = User.objects.get_or_create(phone_number=phone_number)
    return True, user
