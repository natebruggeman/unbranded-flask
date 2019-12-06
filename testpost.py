import requests


req = requests.post(url='https://api.ssactivewear.com/v2/orders/', 
	auth=('504411', '4f4d8aa6-3d5b-4b63-a200-148ebc775938'))


print(req.text)
print(req.json())