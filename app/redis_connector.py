import redis
import os
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
redis_host = env_vars.get("redis_host")
redis_port = env_vars.get("redis_port")
redis_password = env_vars.get("redis_password")

class RedisConnector:
    def __init__(self):
        self.host = redis_host
        self.port = redis_port
        self.password = redis_password
        self.client = None

    def connect(self):
        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                decode_responses=True
            )
            self.client.ping()
            print('Connected to Redis')
        except redis.exceptions.ConnectionError as e:
            print(f'Error connecting to Redis: {e}')

    def get_value(self, key):
        try:
            value = self.client.get(key)
            return value
        except redis.exceptions.RedisError as e:
            print(f'Error getting value from Redis: {e}')
            return None