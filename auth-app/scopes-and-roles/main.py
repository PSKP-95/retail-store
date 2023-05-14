
import json
from database import create_db_connection
from models import Role, Scope
from mongoengine.errors import DoesNotExist, NotUniqueError
import logging

logging.basicConfig(level=logging.INFO)

def create_roles_and_scopes(filename: str):
    create_db_connection()

    f = open(filename, "r")

    data = json.load(f)

    roles = {}

    for file_scope in data:
        try:
            scope = Scope.objects.get(name=file_scope["name"])
            logging.info(f'found scope {scope.name} with id {scope.pk}. Not creating')
        except DoesNotExist as e: 
            logging.info(f'not found scope {file_scope["name"]}. Creating')
            scope = Scope(
                name = file_scope["name"],
                description = file_scope["description"]
            )
            scope = scope.save()
            logging.info(f'Created scope {scope.name}.')
        
        for role in file_scope["roles"]:
            if role in roles:
                roles[role].add(scope.pk)
            else: 
                roles[role] = set({scope.pk})
    
    for key, value in roles.items():
        Role.objects(name=key).update_one(set__scopes=value, upsert=True)

create_roles_and_scopes("scopes.json")