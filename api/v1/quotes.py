from api.v1 import api_v1
from models.storage.firestore_client import FirestoreClient
from flask import jsonify, request
import requests
from models.quotes import Quotes

@api_v1.route('/quotes', methods=['GET'], strict_slashes=False)
def get_all_quotes():
    quotes = Quotes.get_by_class()
    if len(quotes) == 0:
        return jsonify({'status': 'error', 'quotes': []}), 400
    return jsonify({'status': 'OK', 'quotes': quotes}), 200