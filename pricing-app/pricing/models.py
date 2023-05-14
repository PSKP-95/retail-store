from email.policy import default
from enum import unique
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import BooleanField, FloatField ,LazyReferenceField, DictField, EmailField, EmbeddedDocumentField, IntField, ListField, ReferenceField, StringField

class Tag(Document):
  name = StringField(required=True, unique=True)
  text = StringField(required=True)
  items = ListField(ReferenceField('Item'), default=[])


class Item(Document):
  name = StringField(required=True, unique=True)                        # name of product
  description = StringField(required=True)                 # description of product if any
  price = FloatField(required=True)                        # current selling price
  originalPrice = FloatField(required=True)                # original price
  stock = FloatField(required=True)                        # available stock
  sold = FloatField(required=True)                         # total sold item
  unit = StringField(required=True)                        # unit of product Kg, Ltr, unit
  isDivisible = BooleanField(required=True, default=True)  # is product divisible (sugar can be divided by soap cant)
  availablePacks = ListField(default=[])                   # if product not divisible then available packs
  imageUrl = StringField(default="")                       # image of product
  tags = ListField(ReferenceField(Tag), default=[])



# class Location(Document):
#   longitude = FloatField(required=True)
#   latitude = FloatField(required=True)
#   address = StringField(required=True)
#   pinCode = IntField(required=True)
#   items = ListField(EmbeddedDocumentField(Item), required=True, default=[])
