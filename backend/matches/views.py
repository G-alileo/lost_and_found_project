from __future__ import annotations
from django.utils import timezone
from rest_framework import permissions, response, viewsets, decorators
from users.permissions import IsAdminOrReadOnly
from .models import Match
from .serializers import MatchDetailSerializer, MatchSerializer


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Match.objects.all().order_by("-created_at")
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff or getattr(user, "role", None) == "admin":
            return qs
        return qs.filter(lost_report__reported_by=user) | qs.filter(found_report__reported_by=user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MatchDetailSerializer
        return MatchSerializer

    @decorators.action(detail=True, methods=["post"], permission_classes=[IsAdminOrReadOnly])
    def confirm(self, request, pk=None):
        match = self.get_object()
        match.status = Match.Status.CONFIRMED
        match.resolved_at = timezone.now()
        match.save(update_fields=["status", "resolved_at"])
        return response.Response({"status": match.status})

    @decorators.action(detail=True, methods=["post"], permission_classes=[IsAdminOrReadOnly])
    def reject(self, request, pk=None):
        match = self.get_object()
        match.status = Match.Status.REJECTED
        match.resolved_at = timezone.now()
        match.save(update_fields=["status", "resolved_at"])
        return response.Response({"status": match.status})


