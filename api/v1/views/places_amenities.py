#!/usr/bin/python3
"""
Defines place_amenity endpoints
"""
from models import storage
from flask import request, jsonify, abort
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def get_amenities_by_place_id(place_id):
    """Gets all Amenities by Place id."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Deletes a Place-Amenity link."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return {}, 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def post_place_amenity(place_id, amenity_id):
    """Creates a Place-Amenity link."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return amenity.to_dict(), 200
    place.amenities.append(amenity)
    storage.save()
    return amenity.to_dict(), 201
