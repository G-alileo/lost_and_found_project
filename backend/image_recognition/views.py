from __future__ import annotations

import random
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ImageMatchLog


class ImageMatchView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        image = request.FILES.get("image")
        log = ImageMatchLog.objects.create(
            uploaded_by=request.user if request.user.is_authenticated else None,
            image=image,
            suggestions=[{"report_id": 1, "confidence": round(random.uniform(0.3, 0.8), 2)}],
        )
        return Response({"suggestions": log.suggestions})


