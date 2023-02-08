from pymongo import MongoClient
from os import getenv


mongo_password = getenv("mongopassword")
conn = MongoClient(f"mongodb+srv://nekinenadd:{mongo_password}@cluster0.iea1vgg.mongodb.net/?retryWrites=true&w=majority")
db = conn["test"]

collection_name = db["posts"]