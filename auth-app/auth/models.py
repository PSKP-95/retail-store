from datetime import datetime
from email.policy import default
from enum import unique
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import BooleanField, DateTimeField, FloatField ,LazyReferenceField, DictField, EmailField, EmbeddedDocumentField, IntField, ListField, ReferenceField, StringField

class Address(EmbeddedDocument):
  name = StringField(required=True)
  street = StringField(required=True)
  pin = IntField(required=True)
  village = StringField(required=True)

class User(Document):
  name = StringField(required=True)                        # name of user
  email = EmailField(required=True, unique=True)                        # email of user
  mobNum = StringField(required=True, unique=True)                      # mobile number of user
  address = EmbeddedDocumentField(Address, required=True)
  kyc = BooleanField(default=False)
  emailValid = BooleanField(default=False)
  password = StringField(required=True)
  role = ReferenceField('Role')

class Scope(Document):
  name = StringField(unique=True, required=True)
  description = StringField(default="")

class Role(Document):
  scopes = ListField(ReferenceField(Scope, reverse_delete_rule=1), default=[])
  created = DateTimeField(default=datetime.now())
  name = StringField(required=True, unique=True)

# class Key(Document):
#   value = StringField(required=True)
#   alg = StringField(required=True)


# class Location(Document):
#   longitude = FloatField(required=True)
#   latitude = FloatField(required=True)
#   address = StringField(required=True)
#   pinCode = IntField(required=True)
#   items = ListField(EmbeddedDocumentField(Item), required=True, default=[])
