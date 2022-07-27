import aioredis
from asgiref.sync import async_to_sync

from config.settings import REDIS_HOST

redis = aioredis.from_url(f'redis://{REDIS_HOST}:6379')