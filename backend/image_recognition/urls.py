from django.urls import path

from .views import ImageMatchView

urlpatterns = [
    path("image-match/", ImageMatchView.as_view(), name="image-match"),
]


