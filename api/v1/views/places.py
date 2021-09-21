#!/usr/bin/python3
"""Places view for api v1"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_all_places_from_city(city_id):
    """
    Get all places from a city
    ---
    tags:
      - Places
    parameters:
      - name: city_id
        description: City's id
        in: path
        type: string
        required: true
        example: 1da255c0-f023-4779-8134-2b1b40f87683
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
        description: All places from a given city
        schema:
          type: array
          items:
            type: object
            properties:
              __class__:
                type: string
                description: The object's class
              city_id:
                type: string
                description: City's id
              created_at:
                type: string
                description: Place creation date (YY-mm-ddTHH:mm.ffffff)
              description:
                type: string
                description: Place's description
              id:
                type: string
                description: Place's uuid4
              latitude:
                type: number
                description: Place's latitude
              longitude:
                type: number
                description: Place's longitude
              max_guest:
                type: number
                description: Place's maximum number of guests allowed
              name:
                type: string
                description: Place's name
              number_bathrooms:
                type: number
                description: Place's number of bathrooms
              number_rooms:
                type: number
                description: Place's number of rooms
              updated_at:
                type: string
                description: Place update date (YY-mm-ddTHH:mm.ffffff)
              user_id:
                type: string
                description: User's id
          example:
            [
              {
                "__class__": "Place",
                "city_id": "1da255c0-f023-4779-8134-2b1b40f87683",
                "created_at": "2017-03-25T02:17:06.000000",
                "description": "The guest house  [...]",
                "id": "279b355e-ff9a-4b85-8114-6db7ad2a4cd2",
                "latitude": 29.9493,
                "longitude": -90.1171,
                "max_guest": 2,
                "name": "Guest House by Tulane",
                "number_bathrooms": 1,
                "number_rooms": 0,
                "price_by_night": 60,
                "updated_at": "2017-03-25T02:17:06.000000",
                "user_id": "8394fd35-8a8a-479f-a398-48f53b4a6554"
              },
              {
                "__class__": "Place",
                "city_id": "1da255c0-f023-4779-8134-2b1b40f87683",
                "created_at": "2017-03-25T02:17:06.000000",
                "description": "Semi-private room [...]",
                "id": "ffcc9c22-759e-4418-b788-81eda89c2865",
                "latitude": 29.9666,
                "longitude": -90.0519,
                "max_guest": 1,
                "name": "Affordable room in the Marigny",
                "number_bathrooms": 1,
                "number_rooms": 1,
                "price_by_night": 40,
                "updated_at": "2017-03-25T02:17:06.000000",
                "user_id": "7771bbe9-92ab-46d1-a636-864526361d7d"
              }
            ]
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places]), 200


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['GET'])
def get_place_by_id(place_id):
    """
    Get a place based on its ID
    ---
    tags:
      - Places
    parameters:
      - name: place_id
        description: Place's id
        in: path
        type: string
        required: true
        example: 5481bd82-04ab-4a58-ae01-d67443aec20c
    responses:
      404:
        description: No place found
        schema:
          type: object
          properties:
            error:
              type: string
              default: "Not found"
              example: "Not found"
      200:
        description: Place found
        schema:
          type: object
          properties:
            __class__:
              type: string
              description: The object's class
            city_id:
              type: string
              description: City's id
            created_at:
              type: string
              description: Place creation date (YY-mm-ddTHH:mm.ffffff)
            description:
              type: string
              description: Place's description
            id:
              type: string
              description: Place's uuid4
            latitude:
              type: number
              description: Place's latitude
            longitude:
              type: number
              description: Place's longitude
            max_guest:
              type: number
              description: Place's maximum number of guests allowed
            name:
              type: string
              description: Place's name
            number_bathrooms:
              type: number
              description: Place's number of bathrooms
            number_rooms:
              type: number
              description: Place's number of rooms
            updated_at:
              type: string
              description: Place update date (YY-mm-ddTHH:mm.ffffff)
            user_id:
              type: string
              description: User's id
          example:
            __class__: "Place"
            city_id: "1da255c0-f023-4779-8134-2b1b40f87683"
            created_at: "2017-03-25T02:17:06.000000"
            description: "The guest house  [...]"
            id: "279b355e-ff9a-4b85-8114-6db7ad2a4cd2"
            latitude: 29.9493
            longitude: -90.1171
            max_guest: 2
            name: "Guest House by Tulane"
            number_bathrooms: 1
            number_rooms: 0
            price_by_night: 60
            updated_at: "2017-03-25T02:17:06.000000"
            user_id: "8394fd35-8a8a-479f-a398-48f53b4a6554"
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """
    Create a new place in a given city
    ---
    tags:
      - Places
    parameters:
      - name: create_body
        description: Place's information to be stored
        in: body
        type: application/json
        required: true
        schema:
          type: object
          required:
            - name
            - user_id
          properties:
            name:
              type: string
              description: City's name
            user_id:
              type: string
              description: User's id
          example:
            name: "Oh... So Sweet Home!! By UNIVERSAL!! (CAPTAIN A.)"
            user_id: "61302be9-4b31-4be0-92fc-d0dda253e167"
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
        description: Place created
        schema:
          type: object
          properties:
            __class__:
              type: string
              description: The object's class
            city_id:
              type: string
              description: City's id
            created_at:
              type: string
              description: Place creation date (YY-mm-ddTHH:mm.ffffff)
            description:
              type: string
              description: Place's description
            id:
              type: string
              description: Place's uuid4
            latitude:
              type: number
              description: Place's latitude
            longitude:
              type: number
              description: Place's longitude
            max_guest:
              type: number
              description: Place's maximum number of guests allowed
            name:
              type: string
              description: Place's name
            number_bathrooms:
              type: number
              description: Place's number of bathrooms
            number_rooms:
              type: number
              description: Place's number of rooms
            updated_at:
              type: string
              description: Place update date (YY-mm-ddTHH:mm.ffffff)
            user_id:
              type: string
              description: User's id
          example:
            __class__: "Place"
            city_id: "712ffb97-b0eb-42f9-8cb9-69548882ab5d"
            created_at: "2017-03-25T02:17:06.000000"
            description: "CAPTAIN AMERICA ROOM<BR /><BR /> [...]"
            id: "38e38612-a626-47a9-a699-05efa178e155"
            latitude: 28.5558
            longitude: -81.4697
            max_guest: 1
            name: "Oh... So Sweet Home!! By UNIVERSAL!! (CAPTAIN A.)"
            number_bathrooms: 2
            number_rooms: 1
            price_by_night: 16
            updated_at: "2017-03-25T02:17:06.000000"
            user_id: "61302be9-4b31-4be0-92fc-d0dda253e167"
    """
    place_json = request.get_json(silent=True)
    if not place_json:
        return jsonify({'error': 'Not a JSON'}), 400
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if 'user_id' not in place_json:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get(User, place_json.get('user_id'))
    if not user:
        abort(404)
    if 'name' not in place_json:
        return jsonify({'error': 'Missing name'}), 400
    place_json['city_id'] = city_id
    place = Place(**place_json)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """Updates and returns the information of a given place"""
    place_json = request.get_json(silent=True)
    if not place_json:
        return jsonify({'error': 'Not a JSON'}), 400
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for key, val in place_json.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, val)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """Deletes a place and returns an empty JSON"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places_search',
                 strict_slashes=False, methods=['POST'])
def search_place():
    from models.state import State
    """Searches for places given some parameters"""
    search_json = request.get_json(silent=True)
    if search_json is None:
        return jsonify({'error': 'Not a JSON'}), 400
    places = storage.all(Place).values()

    states_param = search_json.get("states")
    cities_param = search_json.get("cities")
    amenities_param = search_json.get("amenities")

    places_search = []
    if states_param:
        for state_id in states_param:
            state = storage.get(State, state_id)
            places_search.extend(
                [place for city in state.cities for place in city.places])
    if cities_param:
        for city_id in cities_param:
            city = storage.get(City, city_id)
            places_search.extend(
                [place for place in city.places if place not in places_search])
    places_search = places_search if places_search else places
    if amenities_param:
        place_amenity_filter = []
        for place in places_search:
            amenity_list = [amenity.id for amenity in place.amenities]
            if all(amenity_id in amenity_list for amenity_id
                    in amenities_param):
                place_amenity_filter.append(place)
        places_search = place_amenity_filter
    return jsonify([place.to_dict() for place in places_search]), 200
