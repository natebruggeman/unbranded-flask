
from peewee import *


DATABASE = SqliteDatabase('unbranded.sqlite')



class Garment(Model):
    gtin = IntegerField()
    qty = CharField()

    class Meta:
        database = DATABASE

class Address(Model):
    attn = CharField()
    address = CharField()
    city = CharField()
    state = CharField()
    zipcode = CharField()

    class Meta:
        database = DATABASE


# the post request to S&S will have Garment as lines and address as 



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Garment, Address], safe=True)
    DATABASE.close()