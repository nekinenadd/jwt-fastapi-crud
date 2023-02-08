import uvicorn
from fastapi import FastAPI,Body,Depends
from config.db import collection_name
from schemas.schemas import post_serializer,posts_serializer
from models.model import PostSchema,UserSchema,UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer
from pymongo import MongoClient



app = FastAPI()





posts = [
    {
        "id":1,
        "title":"Random",
        "text":"Random Random text"
    },
    {
        "id":2,
        "title":"Random",
        "text":"Random Random2 text"
    },
    {
        "id": 3,
        "title":"Random",
        "text":"Random Random3 text"
    }
]

users = []


@app.get('/',tags=["test"])
async def greet():
    posts = posts_serializer(collection_name.find())
    return {"status": "ok", "data" : posts}



@app.get('/all_posts',tags=["posts"])
def index():
    pass

    

@app.get('/posts',tags=["posts"])
def get_posts():
    pass


@app.get('/posts/{id}',tags=["posts"])
def single_post(id: int):
    posts = posts_serializer(collection_name.find())
    for post in posts:
        if posts[id] != id:
            return {
                "error":"Post with this ID does not exist"
            }
        else:
            if posts["id"] == id:
                return {
                    "data": posts
                }


'''
    if id > len(posts_serializer(collection_name.find())):
        return {
            "error":"Post with this ID does not exist!"
        }
    for post in posts:
        if post["id"] == id:
            return {
                "data":post
            }
'''

@app.post('/posts',dependencies=[Depends(jwtBearer())],tags=["posts"])
def add_post(post : PostSchema):
    collection_name.insert_one(post_serializer(post))
    return {
        "info":"Post Added"
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








