# Python modules
import asyncio
import logging

# Third-party modules
import httpx
from adrf.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response as DRFResponse
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

# Project modules
from apps.blog.models import Post, Comment

logger = logging.getLogger(__name__)


class StatsView(APIView):
    """
    Async view for GET /api/stats/

    Why async: this view makes two external HTTP calls concurrently.
    If written synchronously, total time = time(er-api) + time(timeapi).
    With asyncio.gather, total time = max(time(er-api), time(timeapi)).
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Blog statistics",
        description="Returns blog stats combined with live exchange rates and current Almaty time. Two external API calls happen concurrently via asyncio.gather. No authentication required.",
        tags=["Stats"],
        responses={
            200: OpenApiResponse(
                description="Stats returned successfully",
                examples=[
                    OpenApiExample(
                        "Stats response",
                        value={
                            "blog": {"total_posts": 42, "total_comments": 137, "total_users": 15},
                            "exchange_rates": {"KZT": 490.20, "RUB": 79.34, "EUR": 0.86},
                            "current_time": "2026-03-14T04:36:23",
                        },
                    ),
                ],
            ),
        },
    )
    async def get(self, request):
        # Async: два внешних запроса одновременно через asyncio.gather
        async with httpx.AsyncClient(timeout=10.0) as client:
            rates_resp, time_resp = await asyncio.gather(
                client.get("https://open.er-api.com/v6/latest/USD"),
                client.get("https://timeapi.io/api/time/current/zone?timeZone=Asia/Almaty"),
            )

        # DB queries через async ORM Django
        total_posts = await Post.objects.acount()
        total_comments = await Comment.objects.acount()
        total_users = await get_user_model().objects.acount()

        rates = rates_resp.json().get("rates", {})
        current_time = time_resp.json().get("dateTime", "")

        logger.info("Stats endpoint called: external APIs fetched concurrently")

        return DRFResponse({
            "blog": {
                "total_posts": total_posts,
                "total_comments": total_comments,
                "total_users": total_users,
            },
            "exchange_rates": {
                "KZT": rates.get("KZT"),
                "RUB": rates.get("RUB"),
                "EUR": rates.get("EUR"),
            },
            "current_time": current_time,
        })
