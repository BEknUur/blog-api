# third-party imports
from urllib.parse import parse_qs

from channels.db import database_sync_to_async


def get_anonymous_user():
    from django.contrib.auth.models import AnonymousUser

    return AnonymousUser()


@database_sync_to_async
def get_user_from_token(token_str):
    from django.contrib.auth import get_user_model
    from rest_framework_simplejwt.tokens import AccessToken

    try:
        token = AccessToken(token_str)
        User = get_user_model()
        return User.objects.get(id=token["user_id"])
    except Exception:
        return get_anonymous_user()


class JWTAuthMiddleware:
    """Authenticate websocket users from the ?token=<access_token> query param."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        qs = parse_qs(scope["query_string"].decode())
        token_str = qs.get("token", [None])[0]
        scope["user"] = (
            await get_user_from_token(token_str) if token_str else get_anonymous_user()
        )
        return await self.app(scope, receive, send)
