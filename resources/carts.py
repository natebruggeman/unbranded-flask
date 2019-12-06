import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict


cart_bp = Blueprint('carts', 'cart', url_prefix='/cart')


@cart_bp.route('/', methods=["GET"])
def get_all_carts():

    try:
        carts = [model_to_dict(cart) for cart in models.Cart.select()]
        print(carts)
        return jsonify(data=carts, status={"code": 200, "message": "Success"})

    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})


#create cart
@cart_bp.route('/', methods=["POST"])
def create_carts():
    
    payload = request.get_json()

    cart = models.Cart.create(
        garments=payload['garments'])    


    cart_dict = model_to_dict(cart)
    return jsonify(data=cart_dict, status={"code": 201, "message": "Success"})

#     """receiving payload:
        
#         {'addres':..., 'username':..., 'garment_lines':[1,2,3]}

#     """
# # shippingAddress = ForeignKeyField(Address, backref='cart')    
# #     shippingMethod = 1
# #     shipBlind = True
# #     emailConfirmation = 'unbranded.market.us@gmail.com'
# #     autoselectWarehouse = True

#     # get payload
#     payload = request.get_json()
#     # create order in database
#     cart = models.Cart.create(shippingAddress=payload.get('address'),
#         shipBlind=True,
#         emailConfiermarion=payload.get('emailConfirmation'))
#     # push database
#     garments = models.Garments(cart=cart.id)

#     #

@cart_bp.route('/<id>', methods=["GET"])
def get_one_cart(id):
    print(id)
    cart = models.Cart.get_by_id(id)

    return jsonify(data=model_to_dict(cart), status={"code": 200, "message": "Success"})


