
from typing import List
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import LazyReference, LazyReferenceField, BooleanField, ComplexDateTimeField, DateTimeField, DecimalField, DictField, EmbeddedDocumentField, FloatField, IntField, ListField, StringField, ObjectIdField
from passlib.hash import sha256_crypt


def mongo_to_dict(obj, exclude_fields: List = []):
  return_data = []

  if obj is None:
    return None

  if isinstance(obj, Document):
    return_data.append(("id",str(obj.id)))

  for field_name in obj._fields:

    if field_name in exclude_fields:
      continue

    if field_name in ("id",):
      continue

    data = obj._data[field_name]

    if isinstance(obj._fields[field_name], ListField):
      return_data.append((field_name, list_field_to_dict(data)))
    elif isinstance(obj._fields[field_name], EmbeddedDocumentField):
      return_data.append((field_name, mongo_to_dict(data,[])))
    elif isinstance(obj._fields[field_name], LazyReferenceField):
      return_data.append((field_name, str(data.id)))
    elif isinstance(obj._fields[field_name], DictField):
      return_data.append((field_name, data))
    else:
      return_data.append((field_name, mongo_to_python_type(obj._fields[field_name],data)))

  return dict(return_data)

def list_field_to_dict(list_field):

  return_data = []

  for item in list_field:
    if isinstance(item, EmbeddedDocument):
      return_data.append(mongo_to_dict(item,[]))
    else:
      return_data.append(mongo_to_python_type(item,item))


  return return_data

def mongo_to_python_type(field,data):

  if isinstance(field, DateTimeField):
    return str(data.isoformat())
  elif isinstance(field, ComplexDateTimeField):
    return field.to_python(data).isoformat()
  elif isinstance(field, StringField):
    return str(data)
  elif isinstance(field, FloatField):
    return float(data)
  elif isinstance(field, IntField):
    return int(data)
  elif isinstance(field, BooleanField):
    return bool(data)
  elif isinstance(field, ObjectIdField):
    return str(data)
  elif isinstance(field, DecimalField):
    return data
  elif isinstance(field, LazyReference):
    return str(data.id)
  else:
    return str(data)


def get_sha256_hash(text: bytes):
  return sha256_crypt.hash(text)

def verify_sha256_hash(hash: str, text: bytes) -> bool:
  return sha256_crypt.verify(text, hash)