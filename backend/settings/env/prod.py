from settings.base import * 

DEBUG=False

ALLOWED_HOSTS=[ "localhost","127.0.0.1"]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get("BLOG_SQLITE_PATH", os.path.join(BASE_DIR, "db.sqlite3")),
    },
}

REDIS_HOST = os.environ.get("BLOG_REDIS_HOST", REDIS_HOST)
REDIS_PORT = int(os.environ.get("BLOG_REDIS_PORT", REDIS_PORT))
REDIS_DB = int(os.environ.get("BLOG_REDIS_DB", REDIS_DB))
REDIS_URL = os.environ.get(
    "BLOG_REDIS_URL",
    f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "blog",
        "TIMEOUT": 300,
    }
}
