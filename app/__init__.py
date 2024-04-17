from flask import Flask
from app.redis_connector import RedisConnector



# Create a Flask application instance
app = Flask(__name__)

redis_connection = RedisConnector()
redis_connection.connect()
print("redis connected")
# Import routes
from app import routes
