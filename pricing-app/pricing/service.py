
from app.helper import mongo_to_dict
from fastapi import HTTPException
from pricing.schemas import Item as ItemSchema
from pricing.models import Item
from bson import ObjectId
from mongoengine.errors import DoesNotExist, NotUniqueError
import logging


def add_item(itemInput: ItemSchema):
  
  item = Item(
    name = itemInput.name,
    description = itemInput.description,
    price = itemInput.price,
    originalPrice = itemInput.originalPrice,
    stock = itemInput.stock,
    sold = 0.0,
    unit = itemInput.unit
  )
  try:
    i = item.save()
  except NotUniqueError as e:
    logging.error(f'Provided item name `{itemInput.name}` is not unique. {e}', exc_info=True)
    raise HTTPException(status_code=400, detail=f'Provided Item name `{itemInput.name}` is not unique.')
  
  return mongo_to_dict(i)

def find_item_with_id(id: str):
  if not ObjectId.is_valid(id):
    raise HTTPException(status_code=400, detail=f'Provided Item id `{id}` is not valid')
  
  try:
    item = Item.objects.get(pk=id)
  except DoesNotExist as e:
    logging.error(f'Provided item id `{id}` is not found. {e}', exc_info=True)
    raise HTTPException(status_code=404, detail=f'Item with id `{id}` is not exists')
  
  return mongo_to_dict(item)

def get_all_items():
  items: list[Item] = []
  for item in Item.objects:
    items.append(mongo_to_dict(item))

  return items

def update_item(id: str, itemInput: ItemSchema):
  if not ObjectId.is_valid(id):
    raise HTTPException(status_code=400, detail=f'Provided Item id `{id}` is not valid')
  
  try:
    item = Item.objects.get(pk=id)
  except DoesNotExist as e:
    logging.error(f'Provided item id `{id}` is not found. {e}', exc_info=True)
    raise HTTPException(status_code=404, detail=f'Item with id `{id}` is not exists')
  
  item.name = itemInput.name
  item.description = itemInput.description
  item.description = itemInput.description
  item.price = itemInput.price
  item.originalPrice = itemInput.originalPrice
  item.stock = itemInput.stock
  item.unit = itemInput.unit
  item.imageUrl = itemInput.imageUrl

  i = item.save()
  return mongo_to_dict(i)
  
    

