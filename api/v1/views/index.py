#!/usr/bin/python3
"""Index view for api v1"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    """Returns OK if endpoint was correctly created"""
    return jsonify({'status': 'OK'})
