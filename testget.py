from flask import Flask, render_template, g, jsonify
import requests, json #connection to S&S
from peewee import *




app = Flask(__name__)
DEBUG = True
PORT = 8000

DATABASE = SqliteDatabase('nate.sqlite')
# , pragmas={'foreign_keys': 1} removed from end of sqlitedb

class Garment(Model):
	color = CharField()
	brand = CharField()
	gtin = IntegerField()
	size = CharField()
	price  = DecimalField(max_digits=5, decimal_places=2)

	class Meta:
		database = DATABASE


@app.before_request
def before_request():
    g.db = DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response  



@app.route('/refresh_garments')
def index():


	garments = Garment.select()
	for garment in garments:
		garment.delete_instance()

	req = requests.get(url='https://api.ssactivewear.com/v2/products/?style=05606, Bella 3501', 
	auth=('504411', '4f4d8aa6-3d5b-4b63-a200-148ebc775938'))
	req_json = req.json()

	for garment in req_json:
		if garment['colorName'] in ('Military Green', 'Ash'):
			new = Garment(color=garment['colorName'],
				gtin=garment['gtin'],
				brand=garment['brandName'],
				price=garment['piecePrice'],
				size=garment['sizeName'])
			new.save()


	return render_template('garments.html')

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
DATABASE.connect()
DATABASE.create_tables([Garment], safe=True)
print("Created tables if they weren't already there")

DATABASE.close()


if __name__ == '__main__':
	# initialize()
	app.run(debug=DEBUG, port=PORT)