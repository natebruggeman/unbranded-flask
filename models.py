from peewee import *

DATABASE = SqliteDatabase('garments.sqlite')

class Order(Model):


class Garment(Model):
    style = CharField()
    size = CharField()
    color = CharField()

    class Meta:
        database = DATABASE

class Address(Model):
    name = CharField()
    num_street = CharField()
    city = CharField()
    state = CharField()
    zipcode = CharField()

    class Meta:
        database = DATABASE




def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Garment], safe=True)
    DATABASE.close()