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
    # print(type(payload), 'payload')
    garment = models.Garment.create(**payload)    
    # print(garment.__dict__)
    # print(dir(garment))
    # print(model_to_dict(garment), 'model to dict')
    garment_dict = model_to_dict(garment)
    return jsonify(data=garment_dict, status={"code": 201, "message": "Success"})

