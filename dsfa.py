
from peewee import *


DATABASE = SqliteDatabase('unbranded.sqlite', pragmas={'foreign_keys': 1})



class User(Model):
    email = CharField(unique = True)
    password = CharField()
#     class Meta:
#         database = DATABASE
# class Address(Model):
    attn = CharField()
    address = CharField()
    city = CharField()
    state = CharField()
    zipcode = CharField()

    class Meta:
        database = DATABASE


# class Garment(Model):
#     warehouseAbbr = CharField(default="IL")
#     identifier = IntegerField() # gtin

#     qty = CharField()
#     # cart = ForeignKeyField(Cart, backref='cart')

#     class Meta:
#         database = DATABASE


class CartItem(Model):
    color
    style
    name
    warehouseAbbr = CharField(default="IL")
    identifier = IntegerField() # gtin
    qty = IntegerField()
    cart = ForeignKeyField(Cart, backref='items')
    price = # calc based on API 




class Cart(Model):
    user = ForeignKeyField(User, backref='carts')
    date
    settled = # date boolean
    class Meta:
        database = DATABASE
# the post request to S&S will have Garment as lines and address as shippingAddress
class Order(Model):
    shippingAddress = ForeignKeyField(Address, backref='orders')    
    use_user_address = boolean
    addr1
    addr2
    city
    state
    zipcode
    shippingMethod = 1
    shipBlind = True
    emailConfirmation = 'unbranded.market.us@gmail.com'
    autoselectWarehouse = True
    # lines = ForeignKeyField(Cart, backref='orders')

    class Meta:
        database = DATABASE













def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Garment, Address, Cart, Order], safe=True)
    DATABASE.close()


