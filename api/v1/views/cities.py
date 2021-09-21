#!/usr/bin/python3
"""Cities view for api v1"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def get_all_cities_from_state(state_id):
    """
    Get all cities from a state
    ---
    tags:
      - Cities
    parameters:
      - name: state_id
        description: State's id
        in: path
        type: string
        required: true
        example: d2398800-dd87-482b-be21-50a3063858ad
    responses:
      404:
        description: No state found
        schema:
          type: object
          properties:
            error:
              type: string
              default: "Not found"
              example: "Not found"
      200:
        description: All cities from a given state
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
                description: City creation date (YY-mm-ddTHH:mm.ffffff)
              id:
                type: string
                description: City's uuid4
              name:
                type: string
                description: City's name
              state_id:
                type: string
                description: State's id
              updated_at:
                type: string
                description: City update date (YY-mm-ddTHH:mm.ffffff)
          example:
            [
              {
                "__class__": "City",
                "created_at": "2017-03-25T02:17:06.000000",
                "id": "1da255c0-f023-4779-8134-2b1b40f87683",
                "name": "New Orleans",
                "state_id": "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd",
                "updated_at": "2017-03-25T02:17:06.000000"
              },
              {
                "__class__": "City",
                "created_at": "2017-03-25T02:17:06.000000",
                "id": "45903748-fa39-4cd0-8a0b-c62bfe471702",
                "name": "Lafayette",
                "state_id": "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd",
                "updated_at": "2017-03-25T02:17:06.000000"
              }
            ]
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    return jsonify([city.to_dict() for city in cities]), 200


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['GET'])
def get_city_by_id(city_id):
    """
    Get a city based on its ID
    ---
    tags:
      - Cities
    parameters:
      - name: city_id
        description: City's id
        in: path
        type: string
        required: true
        example: 5481bd82-04ab-4a58-ae01-d67443aec20c
    responses:
      404:
        description: No city found
        schema:
          type: object
          properties:
            error:
              type: string
              default: "Not found"
              example: "Not found"
      200:
        description: City found
        schema:
          type: object
          properties:
            __class__:
              type: string
              description: The object's class
            created_at:
              type: string
              description: City creation date (YY-mm-ddTHH:mm.ffffff)
            id:
              type: string
              description: City's uuid4
            name:
              type: string
              description: City's name
            updated_at:
              type: string
              description: City update date (YY-mm-ddTHH:mm.ffffff)
          example:
            __class__: "City"
            created_at: "2017-03-25T02:17:06.000000"
            id: "5481bd82-04ab-4a58-ae01-d67443aec20c"
            name: "Denver"
            updated_at: "2017-03-25T02:17:06.000000"
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """
    Create a new city in a given state
    ---
    tags:
      - Cities
    parameters:
      - name: create_body
        description: City's information to be stored
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
              description: City's name
          example:
            name: "New York City"
    responses:
      400:
        description: User error
        schema:
          type: object
          properties:
            error:
              type: string
              default: "Missing name"
              example: "Missing name"
      201:
        description: City created
        schema:
          type: object
          properties:
            __class__:
              type: string
              description: The object's class
            created_at:
              type: string
              description: City creation date (YY-mm-ddTHH:mm.ffffff)
            id:
              type: string
              description: City's uuid4
            name:
              type: string
              description: City's name
            updated_at:
              type: string
              description: City update date (YY-mm-ddTHH:mm.ffffff)
          example:
            __class__: "City"
            created_at: "2017-03-25T02:17:06.000000"
            id: "6149e15b-90a4-4d42-9d00-8342774d18b6"
            name: "New York City"
            updated_at: "2017-03-25T02:17:06.000000"
    """
    city_json = request.get_json(silent=True)
    if not city_json:
        return jsonify({'error': 'Not a JSON'}), 400
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if 'name' not in city_json:
        return jsonify({'error': 'Missing name'}), 400
    city_json['state_id'] = state_id
    city = City(**city_json)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """
    Update a city based on its ID
    ---
    tags:
      - Cities
    parameters:
      - name: city_id
        description: City's id
        in: path
        type: string
        required: true
        example: 6149e15b-90a4-4d42-9d00-8342774d18b6
      - name: update_body
        description: City's information to be updated
        in: body
        type: application/json
        required: true
        example:
          {
            "name": "Mountain View"
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
        description: No city found
        schema:
          type: object
          properties:
            error:
              type: string
              default: "Not found"
              example: "Not found"
      200:
        description: City updated
        schema:
          type: object
          properties:
            __class__:
              type: string
              description: The object's class
            created_at:
              type: string
              description: City creation date (YY-mm-ddTHH:mm.ffffff)
            id:
              type: string
              description: City's uuid4
            name:
              type: string
              description: City's name
            updated_at:
              type: string
              description: City update date (YY-mm-ddTHH:mm.ffffff)
          example:
            __class__: "City"
            created_at: "2017-03-25T02:17:06.000000"
            id: "6149e15b-90a4-4d42-9d00-8342774d18b6"
            name: "Mountain View"
            updated_at: "2017-03-25T02:17:06.000000"
    """
    city_json = request.get_json(silent=True)
    if not city_json:
        return jsonify({'error': 'Not a JSON'}), 400
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for key, val in city_json.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """
    Delete a city based on its ID
    ---
    tags:
      - Cities
    parameters:
      - name: city_id
        description: City's id
        in: path
        type: string
        required: true
        example: 6149e15b-90a4-4d42-9d00-8342774d18b6
    responses:
      404:
        description: No city found
        schema:
          type: object
          properties:
            error:
              type: string
              default: "Not found"
              example: "Not found"
      200:
        description: City deleted
        schema:
          type: object
          properties:
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200
