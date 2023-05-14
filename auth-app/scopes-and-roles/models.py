from datetime import datetime
from enum import unique
from mongoengine.document import Document
from mongoengine.fields import DateTimeField, FloatField ,LazyReferenceField, DictField, EmailField, EmbeddedDocumentField, IntField, ListField, ReferenceField, StringField


class Role(Document):
  scopes = ListField(ReferenceField('Scope'), default=[])
  created = DateTimeField(default=datetime.now())
  name = StringField(unique=True,required=True)

class Scope(Document):
  name = StringField(unique=True, required=True)
  description = StringField(default="")