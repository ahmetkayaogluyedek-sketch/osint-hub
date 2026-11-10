from pathlib import Path
import os
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --- GÜVENLİK VE ORTAM AYARLARI ---
# Koyeb'de Environment Variables kısmına yazdıklarımızı okur.
# Eğer orada yoksa yerel test için varsayılanları kullanır.
SECRET_KEY = config("SECRET_KEY", default='django-insecure-gecici-test-anahtari-12345')
DEBUG = config("DEBUG", default=False, cast=bool)

# ALLOWED_HOSTS: Koyeb alan adına (.koyeb.app) izin verir.
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1,.koyeb.app", cast=lambda v: [s.strip() for s in v.split(",")])
for _h in ("localhost", "127.0.0.1"):
    if _h not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_h)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_bootstrap5",
    "email_holehe",
    "ExifTool",
    "PhoneSearch",
    "UsernameSearch",
    "HashTool",
    "IPLookup",
    "InstagramSniffer",
    "FaceVerify",
    "django_celery_results",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", 
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "osint_hub.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "osint_hub.wsgi.application"

# Database - Yerelde SQLite, Koyeb'de PostgreSQL varsa onu kullanır
db_url = config("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
DATABASES = {"default": dj_database_url.parse(db_url)}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es-mx"
TIME_ZONE = "America/Mexico_City"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SEARCH_RESULTS_DIR = config(
    "SEARCH_RESULTS_DIR",
    default=str(BASE_DIR / "data" / "search_results"),
)

# --- GÜVENLİK AYARLARI (Canlı Ortam İçin) ---
# Koyeb'de HTTPS olduğu için bunları tekrar aktif ettik.
SESSION_COOKIE_SECURE = True 
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True   
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = 31536000 
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CSRF Ayarları (Koyeb'deki URL'leri otomatik alması için)
csrf_trusted_origins_str = config("CSRF_TRUSTED_ORIGINS", default="http://localhost:8000,https://*.koyeb.app")
if csrf_trusted_origins_str:
    CSRF_TRUSTED_ORIGINS = [url.strip() for url in csrf_trusted_origins_str.split(",")]
else:
    CSRF_TRUSTED_ORIGINS = []

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# ExifTool Path (Koyeb Linux kullandığı için burası kritik)
EXIFTOOL_PATH = "/usr/bin/exiftool"
if not os.path.exists(EXIFTOOL_PATH):
    EXIFTOOL_PATH = "/usr/local/bin/exiftool"

# --- CELERY (Redis) AYARLARI ---
# Koyeb'de REDIS_URL tanımlarsan orayı kullanır.
REDIS_URL = config("REDIS_URL", default="redis://redis:6379/0")
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  
CELERY_RESULT_EXPIRES = 86400  
CELERY_CACHE_BACKEND = "default"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# --- CSP AYARLARI ---
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = (
    "'self'",
    "https://cdn.jsdelivr.net", 
    "https://code.jquery.com", 
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    "https://cdn.jsdelivr.net", 
    "https://fonts.googleapis.com", 
)
CSP_IMG_SRC = (
    "'self'",
    "data:",
    "blob:",
    "https://*.openstreetmap.org",
    "https://*.tile.openstreetmap.org",
)
CSP_FONT_SRC = (
    "'self'",
    "https://fonts.gstatic.com",
    "https://cdn.jsdelivr.net", 
)
CSP_FRAME_SRC = (
    "'self'",
    "https://www.openstreetmap.org",
)
CSP_CONNECT_SRC = (
    "'self'",
    "https://cdn.jsdelivr.net",
)
CSP_INCLUDE_NONCE_IN = ["script-src"]
CSP_REPORT_ONLY = False