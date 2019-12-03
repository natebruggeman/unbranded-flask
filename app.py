from flask import Flask
import requests 

DEBUG = True
PORT = 8000


app = Flask(__name__)

#### get requests
req = requests.get(url='https://api.ssactivewear.com/v2/styles?search=Gildan 5000', 
	auth=('504411', '4f4d8aa6-3d5b-4b63-a200-148ebc775938'))

print(req.text)
print(req.json())
# breakpoint()



@app.route('/')
def index():
    return 'hi natey'
    

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)