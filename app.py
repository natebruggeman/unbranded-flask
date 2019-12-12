from flask import Flask, jsonify, g 
import requests #connection to S&S
from flask_cors import CORS
import models
from resources.garments import garment_bp
from resources.addresses import address_bp
from resources.carts import cart_bp
from resources.orders import order_bp
import os


DEBUG = True
PORT = 8000



app = Flask(__name__)

app.secret_key = "Ernie Kendrick Rosie"



#app routes
@app.route('/')
def index():
    return 'hi natey'

@app.before_request
def before_request():
    # connect to db
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    # close db connection
    g.db.close()
    return response    





CORS(garment_bp, origins=['http://localhost:3000'], supports_credentials=True) 
CORS(address_bp, origins=['http://localhost:3000'], supports_credentials=True) 
CORS(cart_bp, origins=['http://localhost:3000'], supports_credentials=True)
CORS(order_bp, origins=['http://localhost:3000'], supports_credentials=True)


app.register_blueprint(garment_bp, url_prefix='/api/v1/garments') 
app.register_blueprint(address_bp, url_prefix='/api/v1/address') 
app.register_blueprint(cart_bp, url_prefix='/api/v1/cart') 
app.register_blueprint(order_bp, url_prefix='/api/v1/order') 

if 'ON_HEROKU' in os.environ: 
  print('\non heroku!')
  models.initialize()

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)



