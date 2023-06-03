from fastapi import APIRouter, Response, status

from config.db import collection_name
from schemas.user import userEntity, usersEntity
from models.user import User, UserPost

from passlib.hash import sha256_crypt
from bson import ObjectId
# from starlette.status import HTTP_204_NO_CONTENT 

user = router = APIRouter()


#Get
@user.get('/users')
async def find_all_users():
    users = usersEntity(collection_name.find())
    return users


@user.get('/users/{id}')
async def find_user(id: str):
    return usersEntity(collection_name.find_one({"_id": ObjectId(id)}))


#Post
@user.post('/users')
async def create_user(user:UserPost):
    new_user = dict(user)
    new_user['password'] = sha256_crypt.encrypt(new_user['password'])
    
    _id = collection_name.insert_one(dict(new_user))
    return usersEntity(collection_name.find({"_id": _id.inserted_id}))
    

# Update
@user.put('/users/{id}')
async def update_user(id: str, user:User):
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(user)
    })
    return usersEntity(collection_name.find({"_id": ObjectId(id)}))


#Delete
@user.delete('/users/{id}')
async def delete_user(id: str):
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
    return {"status": "OK"}
