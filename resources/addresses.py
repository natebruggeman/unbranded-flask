import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict


address_bp = Blueprint('addresses', 'address', url_prefix='/checkout')


@address_bp.route('/', methods=["GET"])
def get_all_addresses():

    try:
        addresses = [model_to_dict(address) for address in models.Address.select()]

        print(addresses)
        return jsonify(data=addresses, status={"code": 200, "message": "Success"})

    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})



@address_bp.route('/', methods=["POST"])
def create_addresses():
    
    payload = request.get_json()
    # print(type(payload), 'payload')
    address = models.Address.create(**payload)    
    # print(address.__dict__)
    # print(dir(address))
    # print(model_to_dict(address), 'model to dict')
    address_dict = model_to_dict(address)
    return jsonify(data=address_dict, status={"code": 201, "message": "Success"})