from __future__ import annotations

from rest_framework import generics, permissions, response, status

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")


class NotificationMarkReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()

    def post(self, request, *args, **kwargs):
        notif = self.get_object()
        if notif.user != request.user:
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        notif.is_read = True
        notif.save(update_fields=["is_read"])
        return response.Response({"is_read": True})


