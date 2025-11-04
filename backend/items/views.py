from __future__ import annotations

from rest_framework import viewsets

from users.permissions import IsAdminOrReadOnly
from .models import Category, SubCategory
from .serializers import CategorySerializer, SubCategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)



class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.select_related("category").all().order_by("name")
    serializer_class = SubCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """Optionally filter subcategories by ?category=<id>."""
        qs = SubCategory.objects.select_related("category").all().order_by("name")
        category = self.request.query_params.get("category")
        if category:
            try:
                qs = qs.filter(category_id=int(category))
            except (ValueError, TypeError):
                # ignore invalid filter and return full list
                pass
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)


