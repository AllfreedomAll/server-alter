import logging
import json
import redis as _redis
from django.conf import settings

import datetime
from django.db.models import Q

pool = _redis.ConnectionPool(host=settings.REDIS_SERVER_IP, port=settings.REDIS_SERVER_PORT,
                             db=settings.REDIS_DB_NO, decode_responses=True)
logger = logging.getLogger(__name__)

cur_redis = _redis.Redis(connection_pool=pool)
