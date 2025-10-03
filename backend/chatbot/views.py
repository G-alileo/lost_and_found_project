from __future__ import annotations

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class ChatbotView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        message = request.data.get("message", "")
        return Response({"reply": f"Echo: {message}", "intent": "stub", "confidence": 0.0})


