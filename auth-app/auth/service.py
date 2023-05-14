
from app.hashing import Hash
from app.helper import mongo_to_dict
from fastapi import HTTPException, status
from auth.schemas import User as UserSchema, UserEdit
from auth.models import Address, Role, User
from bson import ObjectId
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
import logging


def signup(itemInput: UserSchema):
  print(Hash.bcrypt(itemInput.password.get_secret_value()))

  address = Address(
    name = itemInput.name,
    street = itemInput.address.street,
    pin = itemInput.address.pin,
    village = itemInput.address.village
  )
  user = User(
    name = itemInput.name,                       # name of user
    email = itemInput.email,                        # email of user
    mobNum = itemInput.mobNum,                     # mobile number of user
    address = address,
    password = Hash.bcrypt(itemInput.password.get_secret_value()),
    role = Role.objects.get(name="Buyer").pk
  )
  
  try:
    i = user.save()
  except NotUniqueError as e:
    logging.error(e)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  except ValidationError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  
  return mongo_to_dict(i)

def find_user_with_id(id: str, dictFormat = False):
  if not ObjectId.is_valid(id):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Provided Item id `{id}` is not valid')
  
  try:
    user = User.objects.get(pk=id)
  except DoesNotExist:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Item with id `{id}` is not exists')
  if dictFormat: 
    return mongo_to_dict(user)
  return user


def find_user_with_userid(userid: str, password: str):
  # userid can be mob no or email
  # currently support only email
  try:
    user = User.objects.get(email=userid)
  except DoesNotExist:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with email `{userid}` is not exists')
  
  if not Hash.verify(user.password, password):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Authentication Failed')
  
  return user
  

def update_user_profile(id: str, userInput: UserEdit):
  if not ObjectId.is_valid(id):
    raise HTTPException(status_code=400, detail=f'Provided `{id}` is not valid')
  
  try:
    user = User.objects.get(pk=id)
  except DoesNotExist:
    raise HTTPException(status_code=404, detail=f'User with id `{id}` is not exists')
  
  if userInput.name:
    user.name = userInput.name

  if userInput.address:
    user.address = userInput.address

  if userInput.email:
    user.email = userInput.email

  if userInput.mobNum:
    user.mobNum = userInput.mobNum

  i = user.save()
  return mongo_to_dict(i)
  
    

