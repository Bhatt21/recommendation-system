# app/__init__.py
from flask import Flask
from app import routes
from redis_connector import RedisConnector
def get_redis_instance():
    if redis_connection != None:
        return redis_connection
    redis_connection = RedisConnector()
    redis_connection.connect()
    print("redis connected!")
    return redis_connection

redis_connection = get_redis_instance()

def create_app():
    app = Flask(__name__)
    return app



# from redis_connector import RedisConnector

