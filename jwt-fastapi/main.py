import uvicorn
from fastapi import FastAPI,Body,Depends,Request
from fastapi.encoders import jsonable_encoder
from config.db import collection_name
from schemas.schemas import post_serializer,posts_serializer
from models.model import PostSchema,UserSchema,UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer
from pymongo import MongoClient



app = FastAPI()



users = []

#test

'''
@app.get('/',tags=["test"])
async def greet():
    posts = posts_serializer(collection_name.find())
    return {"status": "ok", "data" : posts}
'''

#get all posts
@app.get('/all_posts',tags=["posts"])
async def index(request:Request):
    posts = posts_serializer(collection_name.find())
    return {"status": "ok", "data" : posts}


#get a single post using ID
@app.get('/posts/{id}',tags=["posts"])
async def single_post(id: int):
    posts = post_serializer(collection_name.find_one({
        "id":id
    }))
    return {"data":posts}

#delete a post using ID
@app.delete('/posts/{id}',dependencies=[Depends(jwtBearer())],tags=["posts"])
async def delete_post(id: int):
    post = post_serializer(collection_name.find_one_and_delete({
        "id":id
    }))
    return {"Delete Post": post}



#make a post
@app.post('/posts/add',dependencies=[Depends(jwtBearer())],tags=["posts"])
async def add_post(request: Request,post : PostSchema):
    post = jsonable_encoder(post)

    collection_name.insert_one(post)
    return {
        "info":"Post Added"
    }


#Update a post 
@app.put('/update/{id}',dependencies=[Depends(jwtBearer())],tags=["posts"])
async def add_post(id:int,post : PostSchema):

    collection_name.update_one({"id":id},{
        "$set":post_serializer(post)
    })
    return {
        "Info":"Post Updated"
    }


#signup a user - not saving in db currently
#Authenticate user by email address (logic is imported) then insert_one into collection
@app.post('/user/signup', tags=["user"])
async def user_signup(user: UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)

async def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        else:
            return False


#loging a user - not reading from a db currently 
@app.post('/user/login',tags=["user"])
async def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            "error" : "Invalid Login Details"
     
 



