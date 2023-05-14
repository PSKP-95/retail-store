from datetime import datetime
from email.policy import default
from enum import unique
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import ObjectIdField, EmbeddedDocumentListField, DateTimeField, FloatField ,LazyReferenceField, DictField, EmailField, EmbeddedDocumentField, IntField, ListField, ReferenceField, StringField

class CartItem(EmbeddedDocument):
  iid = ObjectIdField(required=True)
  qty = FloatField(required=True)

class Cart(Document):
  user = ObjectIdField(required=True, unique=True)
  items = EmbeddedDocumentListField(CartItem, default=[])

class Address(EmbeddedDocument):
  name = StringField(required=True)
  street = StringField(required=True)
  pin = IntField(required=True)
  village = StringField(required=True)

class OrderItem(EmbeddedDocument):
  iid = ObjectIdField(required=True)
  qty = FloatField(required=True)
  rate = FloatField(required=True)
  price = FloatField(required=True)

class Order(Document):
  user = ObjectIdField(required=True)
  orderedOn = DateTimeField(default=datetime.now())
  items = EmbeddedDocumentListField(OrderItem, default=[])
  lastModified = DateTimeField(default=datetime.now())
  address = EmbeddedDocumentField(Address, required=True)


