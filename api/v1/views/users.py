#!/usr/bin/python3
"""Users view for api v1"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'])
def get_all_users():
    """
    Get all users from database
    ---
    tags:
      - Users
    responses:
      200:
        description: All users from the database
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
                description: User creation date (YY-mm-ddTHH:mm.ffffff)
              email:
                type: string
                description: User's email
              first_name:
                type: string
                description: User's first name
              id:
                type: string
                description: User's uuid4
              last_name:
                type: string
                description: User's last name
              updated_at:
                type: string
                description: User update date (YY-mm-ddTHH:mm.ffffff)
          example:
            [
              {
                "__class__": "User",
                "created_at": "2017-03-25T02:17:06.000000",
                "email": "noemail6@gmail.com",
                "first_name": "Todd",
                "id": "00a11245-12fa-436e-9ccc-967417f8c30a",
                "last_name": "Seanez",
                "updated_at": "2017-03-25T02:17:06.000000"
              },
              {
                "__class__": "User",
                "created_at": "2017-03-25T02:17:06.000000",
                "email": "noemail14@gmail.com",
                "first_name": "Leo",
                "id": "df668e22-e344-4c89-a050-e5ad211cbaa6",
                "last_name": "Minnick",
                "updated_at": "2017-03-25T02:17:06.000000"
              }
            ]
    """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users]), 200


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """
    Get a user based on its ID
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        description: User's id
        in: path
        type: string
        required: true
        example: fa44780d-ac48-41ab-9dd0-ac54a15755cf
    responses:
      404:
        description: No user found
        schema:
          type: object
          properties:
            error:
              type: string
              default: "Not found"
              example: "Not found"
      200:
        description: User found
        schema:
          type: object
          properties:
            __class__:
              type: string
              description: The object's class
            created_at:
              type: string
              description: User creation date (YY-mm-ddTHH:mm.ffffff)
            email:
              type: string
              description: User's email
            first_name:
              type: string
              description: User's first name
            id:
              type: string
              description: User's uuid4
            last_name:
              type: string
              description: User's last name
            updated_at:
              type: string
              description: User update date (YY-mm-ddTHH:mm.ffffff)
          example:
            __class__: "User"
            created_at: "2017-03-25T02:17:06.000000"
            email: "noemail20@gmail.com"
            first_name: "Leon"
            id: "fa44780d-ac48-41ab-9dd0-ac54a15755cf"
            last_name: "Sarro"
            updated_at: "2017-03-25T02:17:06.000000"
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user
    ---
    tags:
      - Users
    parameters:
      - name: create_body
        description: User's information to be stored
        in: body
        type: application/json
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              description: User's email
            password:
              type: string
              description: User's password
            first_name:
              type: string
              description: User's first name
            last_name:
              type: string
              description: User's last name
          example:
            email: "noemail@nomail.com"
            password: "pwd01"
            first_name: "Chloe"
            last_name: "Bloom"
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
        description: User created
        schema:
          type: object
          properties:
            __class__:
              type: string
              description: The object's class
            created_at:
              type: string
              description: User creation date (YY-mm-ddTHH:mm.ffffff)
            email:
              type: string
              description: User's email
            first_name:
              type: string
              description: User's first name
            id:
              type: string
              description: User's uuid4
            last_name:
              type: string
              description: User's last name
            updated_at:
              type: string
              description: User update date (YY-mm-ddTHH:mm.ffffff)
          example:
            __class__: "User"
            created_at: "2017-03-25T02:17:06.000000"
            email: "noemail@nomail.com"
            first_name: "Chloe"
            id: "79c6446f-6921-42f3-9298-c5f56ead7af0"
            last_name: "Bloom"
            updated_at: "2017-03-25T02:17:06.000000"
    """
    user_json = request.get_json(silent=True)
    if not user_json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in user_json:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in user_json:
        return jsonify({'error': 'Missing password'}), 400
    user = User(**user_json)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update a user based on its ID
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        description: User's id
        in: path
        type: string
        required: true
        example: fa44780d-ac48-41ab-9dd0-ac54a15755cf
      - name: update_body
        description: User's information to be updated
        in: body
        type: application/json
        required: true
        example:
          {
            "first_name": "Chloe"
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
        description: No user found
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
              description: User creation date (YY-mm-ddTHH:mm.ffffff)
            email:
              type: string
              description: User's email
            first_name:
              type: string
              description: User's first name
            id:
              type: string
              description: User's uuid4
            last_name:
              type: string
              description: User's last name
            updated_at:
              type: string
              description: User update date (YY-mm-ddTHH:mm.ffffff)
          example:
            __class__: "User"
            created_at: "2017-03-25T02:17:06.000000"
            email: "noemail20@gmail.com"
            first_name: "Chloe"
            id: "fa44780d-ac48-41ab-9dd0-ac54a15755cf"
            last_name: "Sarro"
            updated_at: "2017-03-25T02:17:06.000000"
    """
    user_json = request.get_json(silent=True)
    if not user_json:
        return jsonify({'error': 'Not a JSON'}), 400
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    for key, val in user_json.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, val)
    user.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_users(user_id):
    """
    Delete a user based on its ID
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        description: User's id
        in: path
        type: string
        required: true
        example: 150e591e-486b-48ee-be42-4aecba665020
    responses:
      404:
        description: No user found
        schema:
          type: object
          properties:
            error:
              type: string
              default: "Not found"
              example: "Not found"
      200:
        description: User deleted
        schema:
          type: object
          properties:
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200
