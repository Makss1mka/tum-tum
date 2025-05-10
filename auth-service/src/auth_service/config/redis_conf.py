from redis.asyncio import Redis
from globals import REDIS_HOST, REDIS_PORT

redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT)
