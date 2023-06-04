from fastapi import APIRouter

from config.db import collection_name
from schemas.user import usersEntity
from models.user import User

from passlib.hash import sha256_crypt
# from bson import ObjectId
from validate_email import validate_email

user = router = APIRouter()


#Get
@user.get('/users')
async def find_all_users():
    users = usersEntity(collection_name.find())
    return users


@user.get('/users/{email}')
async def find_user(email: str):
    return usersEntity(collection_name.find({"email" : email}))


#Post
@user.post('/users')
async def create_user(user:User):
    new_user = dict(user)
   
    is_valid = validate_email(new_user['email'])
    
    if is_valid:
        _id = collection_name.insert_one(dict(new_user))
        return usersEntity(collection_name.find({"_id": _id.inserted_id}))
    else:
        return'Email no valido'
    

# Update
@user.put('/users/{email}')
async def update_user(email: str, user:User):
    collection_name.find_one_and_update({"email": email}, {
        "$set": dict(user)
    })
    return usersEntity(collection_name.find({"email": email}))


#Delete
@user.delete('/users/{email}')
async def delete_user(email: str):
    collection_name.find_one_and_delete({"email": email})
    return {"status": "OK"}