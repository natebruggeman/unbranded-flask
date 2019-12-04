from flask import Flask, jsonify, g 
import requests #connection to S&S
from flask_cors import CORS
import models
from resources.garments import garment_bp



DEBUG = True
PORT = 8000



app = Flask(__name__)

app.secret_key = "Ernie Kendrick Rosie"




#### get requests
# req = requests.get(url='https://api.ssactivewear.com/v2/styles?search=Gildan 5000', 
# 	auth=('504411', '4f4d8aa6-3d5b-4b63-a200-148ebc775938'))

# print(req.text)
# print(req.json())
# breakpoint()
# in combo with a CLI command about JSON and [0] will allow me to grab different key value pairs


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

app.register_blueprint(garment_bp, url_prefix='/api/v1/garments') 




if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)