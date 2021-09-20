#!/usr/bin/python3
"""Amenities view for api v1"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities',
                 strict_slashes=False, methods=['GET'])
def get_all_amenities():
    """
    Get all amenities from database
    ---
    tags:
      - Amenities
    responses:
      200:
        description: All amenities from the database
        schema:
          type: array
          items:
            type: object
            properties:
              __class__:
                type: string
                description: The object's class
              created_at:
                type: string
                description: Amenity creation date (YY-mm-ddTHH:mm.ffffff)
              id:
                type: string
                description: Amenity's uuid4
              name:
                type: string
                description: Amenity's name
              updated_at:
                type: string
                description: Amenity update date (YY-mm-ddTHH:mm.ffffff)
          example:
            [
              {
                "__class__": "Amenity",
                "created_at": "2017-03-25T02:17:06.000000",
                "id": "017ec502-e84a-4a0f-92d6-d97e27bb6bdf",
                "name": "Cable TV",
                "updated_at": "2017-03-25T02:17:06.000000"
              },
              {
                "__class__": "Amenity",
                "created_at": "2017-03-25T02:17:06.000000",
                "id": "0d375b05-5ef9-4d43-aaca-436762bb25bf",
                "name": "Lockbox",
                "updated_at": "2017-03-25T02:17:06.000000"
              }
            ]
    """
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities]), 200


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def get_amenity_by_id(amenity_id):
    """
    Get an amenity based on its ID
    ---
    tags:
      - Amenities
    parameters:
      - name: amenity_id
        description: Amenity's id
        in: path
        type: string
        required: true
        example: 017ec502-e84a-4a0f-92d6-d97e27bb6bdf
    responses:
      404:
        description: No amenity found
        schema:
          type: object
          properties:
            error:
              type: string
              default: "Not found"
              example: "Not found"
      200:
        description: Amenity found
        schema:
          type: object
          properties:
            __class__:
              type: string
              description: The object's class
            created_at:
              type: string
              description: Amenity creation date (YY-mm-ddTHH:mm.ffffff)
            id:
              type: string
              description: Amenity's uuid4
            name:
              type: string
              description: Amenity's name
            updated_at:
              type: string
              description: Amenity update date (YY-mm-ddTHH:mm.ffffff)
          example:
            __class__: "Amenity"
            created_at: "2017-03-25T02:17:06.000000"
            id: "017ec502-e84a-4a0f-92d6-d97e27bb6bdf"
            name: "Cable TV"
            updated_at: "2017-03-25T02:17:06.000000"
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities',
                 strict_slashes=False, methods=['POST'])
def create_amenity():
    """
    Create a new amenity
    ---
    tags:
      - Amenities
    parameters:
      - name: create_body
        description: Amenity's information to be stored
        in: body
        type: application/json
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              description: Amenity's name
          example:
            name: "TV"
    responses:
      400:
        description: Invalid JSON
        schema:
          type: object
          properties:
            error:
              type: string
              default: "Not a JSON"
              example: "Not a JSON"
      201:
        description: Amenity created
        schema:
          type: object
          properties:
            __class__:
              type: string
              description: The object's class
            created_at:
              type: string
              description: Amenity creation date (YY-mm-ddTHH:mm.ffffff)
            id:
              type: string
              description: Amenity's uuid4
            name:
              type: string
              description: Amenity's name
            updated_at:
              type: string
              description: Amenity update date (YY-mm-ddTHH:mm.ffffff)
          example:
            __class__: "Amenity"
            created_at: "2017-03-25T02:17:06.000000"
            id: "61be5341-92ff-4608-b3ab-30bedad1bd31"
            name: "Hot tub"
            updated_at: "2017-03-25T02:17:06.000000"
    """
    amenity_json = request.get_json(silent=True)
    if not amenity_json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in amenity_json:
        return jsonify({'error': 'Missing name'}), 400
    amenity = Amenity(**amenity_json)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    """
    Update an amenity based on its ID
    ---
    tags:
      - Amenities
    parameters:
      - name: amenity_id
        description: Amenity's id
        in: path
        type: string
        required: true
        example: 61be5341-92ff-4608-b3ab-30bedad1bd31
      - name: update_body
        description: Amenity's information to be updated
        in: body
        type: application/json
        required: true
        example:
          {
            "name": "Gym"
          }
    responses:
      400:
        description: Invalid JSON
        schema:
          type: object
          properties:
            error:
              type: string
              default: "Not a JSON"
              example: "Not a JSON"
      404:
        description: No amenity found
        schema:
          type: object
          properties:
            error:
              type: string
              default: "Not found"
              example: "Not found"
      200:
        description: Amenity updated
        schema:
          type: object
          properties:
            __class__:
              type: string
              description: The object's class
            created_at:
              type: string
              description: Amenity creation date (YY-mm-ddTHH:mm.ffffff)
            id:
              type: string
              description: Amenity's uuid4
            name:
              type: string
              description: Amenity's name
            updated_at:
              type: string
              description: Amenity update date (YY-mm-ddTHH:mm.ffffff)
          example:
            __class__: "Amenity"
            created_at: "2017-03-25T02:17:06.000000"
            id: "61be5341-92ff-4608-b3ab-30bedad1bd31"
            name: "Hot tub"
            updated_at: "2017-03-25T02:17:06.000000"
    """
    amenity_json = request.get_json(silent=True)
    if not amenity_json:
        return jsonify({'error': 'Not a JSON'}), 400
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    for key, val in amenity_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Delete an amenity based on its ID
    ---
    tags:
      - Amenities
    parameters:
      - name: amenity_id
        description: Amenity's id
        in: path
        type: string
        required: true
        example: 61be5341-92ff-4608-b3ab-30bedad1bd31
    responses:
      404:
        description: No amenity found
        schema:
          type: object
          properties:
            error:
              type: string
              default: "Not found"
              example: "Not found"
      200:
        description: Amenity deleted
        schema:
          type: object
          properties:
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200
