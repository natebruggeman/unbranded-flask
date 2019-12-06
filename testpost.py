import requests

def get_orders():

	req = requests.post(url='https://api.ssactivewear.com/v2/orders/', 
		auth=('504411', '4f4d8aa6-3d5b-4b63-a200-148ebc775938'))


	print(req.text)
	print(req.json())




def post_orders():

	data ={
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

	req = requests.post(url='http://localhost:8000/orders/', 
		json=data)


	print(req.text)
	print(req.json())
	

post_orders()



