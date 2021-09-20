#!/usr/bin/python3
"""States view for api v1"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states',
                 strict_slashes=False, methods=['GET'])
def get_all_states():
    """
    Get all states from database
    ---
    tags:
      - States
    responses:
      200:
        description: All states from the database
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
                description: State creation date (YY-mm-ddTHH:mm.ffffff)
              id:
                type: string
                description: State's uuid4
              name:
                type: string
                description: State's name
              updated_at:
                type: string
                description: State update date (YY-mm-ddTHH:mm.ffffff)
          example:
            [
              {
                "__class__": "State",
                "created_at": "2017-03-25T02:17:06.000000",
                "id": "0e391e25-dd3a-45f4-bce3-4d1dea83f3c7",
                "name": "Alabama",
                "updated_at": "2017-03-25T02:17:06.000000"
              },
              {
                "__class__": "State",
                "created_at": "2017-03-25T02:17:06.000000",
                "id": "10098698-bace-4bfb-8c0a-6bae0f7f5b8f",
                "name": "Oregon",
                "updated_at": "2017-03-25T02:17:06.000000"
              }
            ]
    """
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states]), 200


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['GET'])
def get_state_by_id(state_id):
    """
    Get a state based on its ID
    ---
    tags:
      - States
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
        description: State found
        schema:
          type: object
          properties:
            __class__:
              type: string
              description: The object's class
            created_at:
              type: string
              description: State creation date (YY-mm-ddTHH:mm.ffffff)
            id:
              type: string
              description: State's uuid4
            name:
              type: string
              description: State's name
            updated_at:
              type: string
              description: State update date (YY-mm-ddTHH:mm.ffffff)
          example:
            __class__: "State"
            created_at: "2017-03-25T02:17:06.000000"
            id: "d2398800-dd87-482b-be21-50a3063858ad"
            name: "Illinois"
            updated_at: "2017-03-25T02:17:06.000000"
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route('/states',
                 strict_slashes=False, methods=['POST'])
def create_state():
    """
    Create a new state
    ---
    tags:
      - States
    parameters:
      - name: create_body
        description: State's information to be stored
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
              description: State's name
          example:
            name: "Wyoming"
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
        description: State created
        schema:
          type: object
          properties:
            __class__:
              type: string
              description: The object's class
            created_at:
              type: string
              description: State creation date (YY-mm-ddTHH:mm.ffffff)
            id:
              type: string
              description: State's uuid4
            name:
              type: string
              description: State's name
            updated_at:
              type: string
              description: State update date (YY-mm-ddTHH:mm.ffffff)
          example:
            __class__: "State"
            created_at: "2017-03-25T02:17:06.000000"
            id: "0d9148c0-f394-412d-addc-1e5eb4f3e8db"
            name: "Wyoming"
            updated_at: "2017-03-25T02:17:06.000000"
    """
    state_json = request.get_json(silent=True)
    if not state_json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in state_json:
        return jsonify({'error': 'Missing name'}), 400
    state = State(**state_json)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """
    Update a state based on its ID
    ---
    tags:
      - States
    parameters:
      - name: state_id
        description: State's id
        in: path
        type: string
        required: true
        example: 0d9148c0-f394-412d-addc-1e5eb4f3e8db
      - name: update_body
        description: State's information to be updated
        in: body
        type: application/json
        required: true
        example:
          {
            "name": "Mississippi"
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
        description: No state found
        schema:
          type: object
          properties:
            error:
              type: string
              default: "Not found"
              example: "Not found"
      200:
        description: User updated
        schema:
          type: object
          properties:
            __class__:
              type: string
              description: The object's class
            created_at:
              type: string
              description: State creation date (YY-mm-ddTHH:mm.ffffff)
            id:
              type: string
              description: State's uuid4
            name:
              type: string
              description: State's name
            updated_at:
              type: string
              description: State update date (YY-mm-ddTHH:mm.ffffff)
          example:
            __class__: "State"
            created_at: "2017-03-25T02:17:06.000000"
            id: "0d9148c0-f394-412d-addc-1e5eb4f3e8db"
            name: "Mississippi"
            updated_at: "2017-03-25T02:17:06.000000"
    """
    state_json = request.get_json(silent=True)
    if not state_json:
        return jsonify({'error': 'Not a JSON'}), 400
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for key, val in state_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """
    Delete a state based on its ID
    ---
    tags:
      - States
    parameters:
      - name: state_id
        description: State's id
        in: path
        type: string
        required: true
        example: 0d9148c0-f394-412d-addc-1e5eb4f3e8db
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
        description: State deleted
        schema:
          type: object
          properties:
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200
