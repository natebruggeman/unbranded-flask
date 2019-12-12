from flask import Flask, render_template, g, jsonify, request
import requests, json #connection to S&S
from peewee import *
from flask_cors import CORS
from playhouse.shortcuts import model_to_dict
# from decimal import Decimal


app = Flask(__name__)
DEBUG = True
PORT = 8000


DATABASE = SqliteDatabase('nate.sqlite')
# , pragmas={'foreign_keys': 1} removed from end of sqlitedb



########################### MODELS START#####################################

class Garment(Model):
	color = CharField()
	brand = CharField()
	gtin = IntegerField()
	size = CharField()
	price  = DecimalField(max_digits=5, decimal_places=2)
	picture = CharField()

	class Meta:
		database = DATABASE

class Order(Model):
	items= CharField()
	shippingAddress= CharField()
	shippingCity= CharField()
	shippingState= CharField()
	shippingZip= IntegerField()
	creditCard= IntegerField()
	# user = CharField()

	class Meta:
		database = DATABASE

# class Cart(Model):
#     quantity = IntegerField()
#     garment = ForeignKeyField(Garment, backref='products')
#     paid = BooleanField()

class CartItem(Model):
	color = CharField()
	size = CharField()
	garment = ForeignKeyField(Garment, backref='garments')
	warehouseAbbr = CharField(default="IL")
	# identifier = IntegerField() # gtin
	quantity = IntegerField()
	paid = BooleanField(default= False)
    # cart = ForeignKeyField(Order, backref='cart')
    # price = # calc based on API 
	class Meta:
		database = DATABASE


########################### MODELS END #####################################

CORS(app, origins=['http://localhost:3000'], supports_credentials=True) 
### Connect to DB and disconnect

@app.before_request
def before_request():
    g.db = DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response  

###########################GARMENTS START#####################################

#showing all garments in DB
@app.route('/list')
def list():
	garments = Garment.select()
	results = []
	for garment in garments:
		info = {'gtin': garment.gtin,
				'brandName': garment.brand,
				'colorName': garment.color,
				'sizeName': garment.size,
				'piecePrice': str(garment.price),
				'colorFrontImage': garment.picture
				}
		results.append(info)

	return jsonify(results)


#show individual garments
@app.route('/list/<id>', methods=["GET"])
def list_one_garment(id):
	garment = Garment.get_by_id(id)
	garm_dict= model_to_dict(garment)
	#turns price from a decimal to a string
	garm_dict["price"] = str(garm_dict["price"])
	return jsonify(data=garm_dict, status={"code": 200, "message": "Success"})


# add products to DB 
@app.route('/refresh_garments')
def index():

	garments = Garment.select()
	for garment in garments:
		garment.delete_instance()

	req = requests.get(url='https://api.ssactivewear.com/v2/products/?style=05606, Bella 3501', 
	auth=('504411', '4f4d8aa6-3d5b-4b63-a200-148ebc775938'))
	req_json = req.json()

	for garment in req_json:
		if garment['colorName'] in ('Military Green', 'Ash', 'Maroon'):
			new = Garment(color=garment['colorName'],
				gtin=garment['gtin'],
				brand=garment['brandName'],
				price=garment['piecePrice'],
				size=garment['sizeName'],
				picture=garment['colorFrontImage'])
			new.save()


	return render_template('garments.html')


########################### GARMENTS END #####################################


########################### CART START #####################################


# @app.route('/cart/<id>', methods=["POST"])
# def create_cart_item(id):
# 	breakpoint()
# 	garment= Garment.get_by_id(id)
# 	garm_dict= model_to_dict(garment)

# 	print(garm_dict)

# 	data = request.get_json()
# 	print(data)

# 	cart_item = models.CartItem.create(
# 		quantity=data['quantity'],
# 		paid=data['paid'],
# 	)
# 	cart_dict = model_to_dict(cart_item)
# 	return jsonify(data=cart_dict, status={"code": 201, "message": "You successfully created your cart"})
# 	# return 'ok', 200


@app.route('/shoppingcart', methods=['POST'])
def create_cart(id):

	payload = request.get_json()

	print(payload)

	first_item = CartItem(
		quantity=1,
	 	paid= False,
	 	color= payload['color'],
	 	size= payload['size'],
	 	brand= payload['brand'],
		garment = payload['garment'],
		# identifier = payload['gtin'] # gtin	
	 )
	breakpoint()
	first_item.save()
		# color = CharField()
		# size = CharField()
		# name = CharField()
		# garment = ForeignKeyField(Garment, backref='garments')
		# warehouseAbbr = CharField(default="IL")
		# identifier = IntegerField() # gtin
		# quantity = IntegerField()
		# paid = BooleanField(default= False)

		# cart_hash

	# cart_dict = model_to_dict(first_item)
	# print(cart_dict)
	return 'ok', 200
	# return jsonify(data=cart_dict, status={"code": 201, "message": "You successfully created your cart"})


########################### CART END #####################################


###########################ORDERS START#####################################


@app.route('/orders/', methods=['POST'])
def create_orders():
	"""
	{
	   "items":[
	      {
	         "gtin":884913636842,
	         "qty":3
	      },
	      {
	         "gtin":884913636866,
	         "qty":5
	      }
	   ],
	   "shippingAddress":"123 street",
	   "shippingCity":"chicago",
	   "shippingState":"IL",
	   "shippingZip":"60647",
	   "creditCard":"12345"
	}
	"""
	data = request.get_json()
	print(data)
	# breakpoint()

	order = Order(items=json.dumps(data["items"]), # stringifying
		shippingAddress= data["shippingAddress"],
		shippingCity= data["shippingCity"],
		shippingState= data["shippingState"],
		shippingZip= data["shippingZip"],
		creditCard= data["creditCard"],
		# user = "this will be from session"
		)
	order.save()
	print(order)

	return 'ok', 200


########################### ORDERS END #####################################




















########################### DB CONNECTION/ CREATION#####################################



DATABASE.connect()
DATABASE.create_tables([Garment, Order, CartItem], safe=True)
print("Created tables if they weren't already there")

DATABASE.close()


if __name__ == '__main__':
	# initialize()
	app.run(debug=DEBUG, port=PORT)











# req = requests.get(url='https://api.ssactivewear.com/v2/products/?style=00760,Gildan 5000', 
# 	auth=('504411', '4f4d8aa6-3d5b-4b63-a200-148ebc775938'))

# req = requests.get(url='https://api.ssactivewear.com/v2/orders/19850376', 
# 	auth=('504411', '4f4d8aa6-3d5b-4b63-a200-148ebc775938'))

# req = requests.get(url='https://api.ssactivewear.com/v2/products/?style=05606, Bella 3501', 
# 	auth=('504411', '4f4d8aa6-3d5b-4b63-a200-148ebc775938'))



# print(req.text)
# data = req.json()

# dict_data = json.loads(data)
# print(dict_data)

# print(data)
# python_obj = json.loads(data)
# print(python_obj['sizeName: XL'])

# breakpoint()
# in combo with a CLI command about JSON and [0] will allow me to grab different key value pairs

# def initialize():