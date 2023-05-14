
import json
from app.hashing import Hash
from app.helper import mongo_to_dict
from fastapi import HTTPException, status
from cartorder.models import Cart, CartItem
from bson import ObjectId
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
import logging


def get_cart(uid: str):
  print(uid)
  if not ObjectId.is_valid(uid):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'user id `{uid}` is not valid')
  
  ouid = ObjectId(uid)
  try:
    cart = Cart.objects.get(user=ouid)
  except DoesNotExist:
    return {"items": []}
  
  items = []

  for item in cart.items:
    items.append({"iid": str(item.iid), "qty": item.qty})
  return {"items": items}

def change_item_in_cart(uid: str, iid: str, qty: float):
  if qty < 0:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'quantity should be more than or equal to 0')
  if not ObjectId.is_valid(uid) or not ObjectId.is_valid(iid):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'user id `{uid}` or item it `{iid} is not valid')
  
  ouid = ObjectId(uid)
  oiid = ObjectId(iid)

  cartItem = CartItem(
    iid = oiid,
    qty = qty
  )
  try:
    cart = Cart.objects.get(user=ouid)
  except DoesNotExist:
    cart = Cart(
      user = ouid,
      items = [cartItem]
    )
    savedCart = cart.save()

    items = []

    for item in cart.items:
      items.append({"iid": str(item.iid), "qty": item.qty})

    return {"items": items}

  isItemInCart = False
  for item in cart.items:
    if item.iid == oiid:
      isItemInCart = True
      if qty == 0:
        cart.items.remove(item)
      else:
        item.qty = qty
      break
  
  if not isItemInCart:
    cart.items.append(cartItem)
  
  savedCart = cart.save()
  
  items = []

  for item in cart.items:
    items.append({"iid": str(item.iid), "qty": item.qty})
  return {"items": items}

