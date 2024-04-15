import redis
import os

class RedisConnector:
    def __init__(self):
        self.host = os.getenv('REDIS_HOST')
        self.port = os.getenv('REDIS_PORT')
        self.password = os.getenv('REDIS_PASSWORD')
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