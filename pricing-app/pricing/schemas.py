from enum import Enum
from fastapi import HTTPException
from typing import Dict, List, Optional, Text
from wsgiref.validate import validator
from pydantic import BaseModel


class Item(BaseModel):
  name: str
  description: Text
  price: float
  originalPrice: float
  stock: float
  unit: str
  isDivisible: bool
  imageUrl: Optional[str]
  tags: List[str] = []


class ItemWithId(Item):
  id: str
  sold: float
