import uvicorn
from fastapi import FastAPI,Body,Depends
from config.db import collection_name
from schemas.schemas import post_serializer,posts_serializer
from models.model import PostSchema,UserSchema,UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer
from pymongo import MongoClient



app = FastAPI()



users = []

#test
@app.get('/',tags=["test"])
async def greet():
    posts = posts_serializer(collection_name.find())
    return {"status": "ok", "data" : posts}


#get all posts
@app.get('/all_posts',tags=["posts"])
def index():
    posts = posts_serializer(collection_name.find())
    return {"status": "ok", "data" : posts}


#get a single post using ID
@app.get('/posts/{id}',tags=["posts"])
def single_post(id: int):
    posts = post_serializer(collection_name.find_one({
        "id":id
    }))
    return {"data":posts}

#delete a post using ID
@app.delete('/posts/{id}',dependencies=[Depends(jwtBearer())],tags=["posts"])
def delete_post(id: int):
    post = post_serializer(collection_name.find_one_and_delete({
        "id":id
    }))
    return {"Delete Post": post}




@app.post('/posts',dependencies=[Depends(jwtBearer())],tags=["posts"])
def add_post(post : PostSchema):
    collection_name.insert_one(post_serializer(post))
    return {
        "info":"Post Added"
    }

@app.put('/update/{id}',dependencies=[Depends(jwtBearer())],tags=["posts"])
def add_post(id:int,post : PostSchema):
    collection_name.find_one_and_update({"id":id},{
        "$set":post_serializer(post)
    })
    return {
        "Info":"Post Updated"
    }


@app.post('/user/signup', tags=["user"])
def user_signup(user: UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        else:
            return False


@app.post('/user/login',tags=["user"])
def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            "error" : "Invalid Login Details"
        }








