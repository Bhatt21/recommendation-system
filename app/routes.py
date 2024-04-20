from app import app
from flask import request, jsonify
import json

from app import redis_connection
from app.recomendation import GooglePlacesAPI
from dotenv import dotenv_values

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

def decrypt_aes(encrypted_data, key="VacayBuddy Sightseeing Search"):
    key = key.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, b'VacayBuddy Sightseeing Search')
    decrypted = unpad(cipher.decrypt(base64.b64decode(encrypted_data)), AES.block_size)
    return decrypted.decode('utf-8')

env_vars = dotenv_values(".env")

def extract_location(data):
    latitude = data["geometry"]["location"]["lat"]
    longitude = data["geometry"]["location"]["lng"]
    return f"{latitude},{longitude}"


@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    # Parse recommendation ID from request body
    data = request.get_json()
    recommendation_id = decrypt_aes(data.get('recommendation_id'))
    if recommendation_id is None:
        return jsonify({'error': 'No recommendation ID provided'}), 400
    try:
        value = json.loads(redis_connection.get_value(f"{recommendation_id}"))

        loc = extract_location(value)
        print(value,loc)
    except Exception as e:
        print(f"Exception occurred while getting value from Redis: {e}")
        return jsonify({'error': 'Internal server error'}), 500

    if value is None:
        return jsonify({'error': 'Value not found in Redis'}), 404
    else:
        google_api_key = env_vars.get("google_api_key")
        result = GooglePlacesAPI(google_api_key).get_nearby_places(loc, "tourist_attraction")
        return jsonify(result), 200

