from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, SubCategoryViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"subcategories", SubCategoryViewSet, basename="subcategory")

urlpatterns = [
    path("", include(router.urls)),
]


