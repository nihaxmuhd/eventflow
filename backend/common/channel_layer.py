"""Redis channel-layer diagnostics for live connection failures.

The methods below deliberately record channel and group identifiers only.  They
never log message bodies, JWTs, or connection credentials.
"""

import logging
import time

from channels_redis.core import RedisChannelLayer


logger = logging.getLogger(__name__)


class InstrumentedRedisChannelLayer(RedisChannelLayer):
    """Log the Redis operation that fails without changing retry semantics."""

    async def receive(self, channel):
        started = time.monotonic()
        try:
            return await super().receive(channel)
        except Exception:
            logger.exception(
                "channels_redis receive failed channel=%s elapsed_ms=%d",
                channel,
                (time.monotonic() - started) * 1000,
            )
            raise

    async def receive_single(self, channel):
        started = time.monotonic()
        try:
            return await super().receive_single(channel)
        except Exception:
            logger.exception(
                "channels_redis receive_single failed channel=%s elapsed_ms=%d",
                channel,
                (time.monotonic() - started) * 1000,
            )
            raise

    async def group_add(self, group, channel):
        try:
            return await super().group_add(group, channel)
        except Exception:
            logger.exception(
                "channels_redis group_add failed group=%s channel=%s",
                group,
                channel,
            )
            raise

    async def group_discard(self, group, channel):
        try:
            return await super().group_discard(group, channel)
        except Exception:
            logger.exception(
                "channels_redis group_discard failed group=%s channel=%s",
                group,
                channel,
            )
            raise

    async def group_send(self, group, message):
        try:
            return await super().group_send(group, message)
        except Exception:
            logger.exception("channels_redis group_send failed group=%s", group)
            raise
