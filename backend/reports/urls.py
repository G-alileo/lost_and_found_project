from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReportViewSet
from .dashboard_views import (
    dashboard_stats, user_reports, user_matches, user_notifications,
    mark_notification_read, confirm_match, reject_match
)

router = DefaultRouter()
router.register(r"reports", ReportViewSet, basename="report")

urlpatterns = [
    path("", include(router.urls)),
    # Dashboard API endpoints
    path("dashboard/stats/", dashboard_stats, name="dashboard-stats"),
    path("dashboard/reports/", user_reports, name="user-reports"),
    path("dashboard/matches/", user_matches, name="user-matches"),
    path("dashboard/notifications/", user_notifications, name="user-notifications"),
    path("dashboard/notifications/<int:notification_id>/read/", mark_notification_read, name="mark-notification-read"),
    path("dashboard/matches/<int:match_id>/confirm/", confirm_match, name="confirm-match"),
    path("dashboard/matches/<int:match_id>/reject/", reject_match, name="reject-match"),
]


