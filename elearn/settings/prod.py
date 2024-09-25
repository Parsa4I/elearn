from .base import *


DEBUG = False

ALLOWED_HOSTS = ["*"]

STATIC_ROOT = BASE_DIR / "static/"

CSRF_TRUSTED_ORIGINS = ["http://localhost:1337", "http://127.0.0.1:1337"]
