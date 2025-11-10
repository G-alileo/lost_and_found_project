from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/", include("items.urls")),
    path("api/", include("reports.urls")),
    path("api/", include("matches.urls")),
    path("api/", include("notifications.urls")),
    path("api/", include("chatbot.urls")),
    path("api/", include("image_recognition.urls")),
    path("api/admin/", include("adminpanel.urls")),
    path("api/chat/", include("chat.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


