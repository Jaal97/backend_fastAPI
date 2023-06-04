from pymongo import MongoClient

client = MongoClient('Aqui va el enlace de su base de datos mongoDB')


db = client.users_db

collection_name = db["users"]