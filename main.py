from fastapi import FastAPI
from starlette.responses import JSONResponse, Response
from pydantic import BaseModel
from typing import List
from starlette.requests import Request
from datetime import datetime
import json
import base64


app = FastAPI()

class Post(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime

posts_list: List[Post] = []

def serialized_posts_list():
    converted_posts_list = []
    for post in posts_list:
        converted_posts_list.append(post.model_dump())
    return converted_posts_list

# Q1
@app.get("/ping")
def ping():
    return Response(content="pong", status_code=200, media_type="text/plain")

# Q2
@app.get("/home")
def home():
    with open("welcome.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=200, media_type="text/html")

# Q3
@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open("notFound.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=404, media_type="text/html")

# Q4: POST /posts
@app.post("/posts")
def create_posts(new_posts_list: List[Post]):
    for new_post in new_posts_list:
        posts_list.append(new_post)
    return Response(
        content=json.dumps({"posts": serialized_posts_list()}),
        status_code=201,
        media_type="application/json"
    )

# Q5: GET /posts
@app.get("/posts")
def list_posts():
    return Response(
        content=json.dumps({"posts": serialized_posts_list()}),
        status_code=200,
        media_type="application/json"
    )

# Q6: PUT /posts
@app.put("/posts")
def update_or_create_posts(posts_payload: List[Post]):
    global posts_list
    for new_post in posts_payload:
        found = False
        for i, existing_post in enumerate(posts_list):
            if new_post.title == existing_post.title:
                posts_list[i] = new_post
                found = True
                break
        if not found:
            posts_list.append(new_post)
    return {"posts": serialized_posts_list()}

@app.get("/ping/auth")
def read_ping_with_auth(request: Request):
    valid_username = "admin"
    valid_password = "123456"
    authorization_header = request.headers.get("Authorization")
    if not authorization_header:
        return JSONResponse(
            content={"message": "Authorization header is missing"},
            status_code=401
        )
    auth_type, credentials = authorization_header.split(" ")
    decoded_credentials = base64.b64decode(credentials.encode('utf-8')).decode('utf-8')
    username, password = decoded_credentials.split(':')
    if username != valid_username or password != valid_password:
        return JSONResponse(content={"message": "unauthorized Ressource"},status_code=401)
    elif username == valid_username and password == valid_password:
        return Response(content="pong", media_type="text/plain", status_code=200)

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open ("404.html" , "r" , encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content,status_code=404,media_type="text/html")