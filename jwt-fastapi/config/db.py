from pymongo import MongoClient
from os import getenv


conn = MongoClient(f"mongodb+srv://nekinenadd:{getenv("mongopassword")}@cluster0.iea1vgg.mongodb.net/?retryWrites=true&w=majority")
db = conn["test"]

collection_name = db["posts"]