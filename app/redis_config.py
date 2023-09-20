import redis
import config
cache = redis.Redis(host=config.REDIS_HOST,port=config.REDIS_PORT, db=config.REDIS_DB,decode_responses=True)