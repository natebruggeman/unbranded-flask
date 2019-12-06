import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict


garment_bp = Blueprint('garments', 'garment', url_prefix='/garment')


@garment_bp.route('/', methods=["GET"])
def get_all_garments():

    try:
        garments = [model_to_dict(garment) for garment in models.Garment.select()]

        print(garments)
        return jsonify(data=garments, status={"code": 200, "message": "Success"})

    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})



@garment_bp.route('/', methods=["POST"])
def create_garments():
    
    payload = request.get_json()
    garment = models.Garment.create(**payload)    
    garment_dict = model_to_dict(garment)
    return jsonify(data=garment_dict, status={"code": 201, "message": "Success"})



@garment_bp.route('/<id>', methods=["GET"])
def get_one_garment(id):
    print(id)
    garment = models.Garment.get_by_id(id)

    return jsonify(data=model_to_dict(garment), status={"code": 200, "message": "Success"})







