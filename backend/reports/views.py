from __future__ import annotations

from django.db.models import Q
from rest_framework import permissions, viewsets, decorators, response

from users.permissions import IsOwnerOrAdmin
from .models import Report
from .serializers import ReportListSerializer, ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by("-created_at")
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return ReportListSerializer
        return ReportSerializer

    def perform_create(self, serializer):
        instance = serializer.save(reported_by=self.request.user)
        # matching trigger will be via signal; placeholder if needed
        return instance

    def get_queryset(self):
        qs = super().get_queryset()
        report_type = self.request.query_params.get("type")
        category = self.request.query_params.get("category")
        status_param = self.request.query_params.get("status")
        q = self.request.query_params.get("q")
        if report_type in {"lost", "found"}:
            qs = qs.filter(report_type=report_type)
        if category:
            qs = qs.filter(category_id=category)
        if status_param:
            qs = qs.filter(status=status_param)
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(location__icontains=q))
        return qs

    @decorators.action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def find_matches(self, request, pk=None):
        # Placeholder: actual matching will run; return 202 Accepted
        return response.Response({"triggered": True})


