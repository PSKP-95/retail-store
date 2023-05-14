from mongoengine import connect
import os
import redis

client = redis.Redis()

def create_db_connection():
    conn = connect(db="PRICING_APP", host=os.environ.get("MONGO_HOST"), port=27017, username=os.environ.get("MONGO_USER"), password=os.environ.get("MONGO_PASSWORD"), authentication_source="admin")
