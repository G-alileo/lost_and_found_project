from __future__ import annotations

from django.db.models import Count
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from matches.models import Match
from reports.models import Report


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_staff or getattr(user, "role", None) == "admin"))


class AdminStatsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        total_lost = Report.objects.filter(report_type=Report.ReportType.LOST).count()
        total_found = Report.objects.filter(report_type=Report.ReportType.FOUND).count()
        total_matches = Match.objects.count()
        successful_matches = Match.objects.filter(status=Match.Status.CONFIRMED).count()
        unclaimed = Report.objects.filter(status=Report.Status.UNCLAIMED).count()

        top_categories_qs = (
            Report.objects.values("category__name").annotate(total=Count("id")).order_by("-total")[:5]
        )
        top_categories = [{"name": r["category__name"], "count": r["total"]} for r in top_categories_qs]

        return Response(
            {
                "total_lost": total_lost,
                "total_found": total_found,
                "total_matches": total_matches,
                "successful_matches_count": successful_matches,
                "unclaimed_count": unclaimed,
                "top_categories": top_categories,
            }
        )


