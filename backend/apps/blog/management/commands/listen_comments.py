# Python modules
import asyncio
import json
import logging

# Django modules
from django.core.management.base import BaseCommand
from django.conf import settings

# Third-party modules
import redis.asyncio as aioredis

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Subscribe to Redis comments channel using async Redis client"

    def handle(self, *args, **options):
        """
        Why async: Redis pub/sub is I/O bound — we're just waiting for messages.
        Sync version would block the thread while waiting.
        Async version uses asyncio event loop — no thread blocking.
        """
        self.stdout.write(self.style.SUCCESS("Starting async Redis subscriber..."))
        asyncio.run(self.listen())

    async def listen(self):
        """
        Async Redis listener using asyncio event loop.
        If written synchronously, the thread would block on pubsub.listen()
        preventing any other work. Async allows cooperative multitasking.
        """
        r = aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
            decode_responses=True,
        )

        try:
            await r.ping()
            self.stdout.write(self.style.SUCCESS("Connected to Redis"))

            pubsub = r.pubsub()
            await pubsub.subscribe("comments")
            self.stdout.write(self.style.SUCCESS("Subscribed to 'comments' channel"))
            self.stdout.write(self.style.WARNING("Listening for messages (Ctrl+C to stop)...\n"))

            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])
                        self.stdout.write(self.style.SUCCESS("=" * 60))
                        self.stdout.write("New Comment Event:")
                        self.stdout.write(f"  Post slug:  {data.get('post_slug')}")
                        self.stdout.write(f"  Author ID:  {data.get('author_id')}")
                        self.stdout.write(f"  Body:       {data.get('body')}")
                        self.stdout.write(self.style.SUCCESS("=" * 60))

                        logger.info(f"Received comment event: post_slug={data.get('post_slug')}")

                    except json.JSONDecodeError as e:
                        self.stdout.write(self.style.ERROR(f"Failed to parse: {e}"))

        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\nStopped by user"))
        finally:
            await pubsub.close()
            await r.aclose()
            self.stdout.write(self.style.SUCCESS("Redis connection closed"))
