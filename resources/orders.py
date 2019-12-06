import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict


order_bp = Blueprint('orders', 'order', url_prefix='/order')


@order_bp.route('/', methods=["GET"])
def get_all_orders():

    try:
        orders = [model_to_dict(order) for order in models.Order.select()]

        print(orders)
        return jsonify(data=orders, status={"code": 200, "message": "Success"})

    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})



@order_bp.route('/', methods=["POST"])
def create_orders():
    
    payload = request.get_json()
    order = models.Order.create(**payload)    
    order_dict = model_to_dict(order)
    return jsonify(data=order_dict, status={"code": 201, "message": "Success"})



@order_bp.route('/<id>', methods=["GET"])
def get_one_order(id):
    print(id)
    order = models.Order.get_by_id(id)

    return jsonify(data=model_to_dict(order), status={"code": 200, "message": "Success"})





