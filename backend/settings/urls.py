#Django modules
from django.contrib import admin
from django.urls import path, include

# Project modules
from apps.blog.views_async import StatsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("apps.users.auth.urls")),
    path("api/", include("apps.users.urls")),
    path("api/", include("apps.blog.urls")),
    path("api/stats/", StatsView.as_view(), name="stats"),
]
