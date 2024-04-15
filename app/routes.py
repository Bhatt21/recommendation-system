from app import app
from flask import request, jsonify

from utils.crypto_utils import CryptoUtils
from . import redis_connection
    
@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    # Parse recommendation ID from request body
    data = request.get_json()
    recommendation_id = data.get('recommendation_id')

    if recommendation_id is None:
        return jsonify({'error': 'No recommendation ID provided'}), 400
    
    decrypted_key = CryptoUtils().getSightsSearchKey(recommendation_id)
    try:
        value = redis_connection.get_value(decrypted_key)
        if value is None:
            return jsonify({'error': 'Value not found in Redis'}), 404
        else:
            result = process_recomendation(value)
            return jsonify(result), 200
    except Exception as e:
        print(f"Exception occurred while getting value from Redis: {e}")
        return jsonify({'error': 'Internal server error'}), 500

