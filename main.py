from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
app = FastAPI()

class Post(BaseModel):

    title: str
    content: str
    published: bool = True
    rating: Optional[int] | None


my_posts = [
    {"title" : "Silo London", "content": "very nice!", "rating" : 4, "id" : 1},
    {"title" : "Nandos", "content": "not nice!", "rating" : 1, "id" : 2}
            ]

# This is a path operation / route
# decorator app.get modifies the behavior of root func to turn it into an api function
# async calls we use async keyword for, such as api calls
# the function converts python dicts to json to user

@app.get("/")
async def root():
    return {"message" : "Hello World!"}

@app.get("/posts")
def get_posts():
    return {"data" : my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):

    post_dict = new_post.model_dump()
    post_dict['id'] = randrange(2, 100000)
    my_posts.append(post_dict)

    return {"new_post" : f"{post_dict}"}

def find_post(id: int):

    post = [x for x in my_posts if x['id'] == id]

    if post:
        return post[0]
    return

def find_post_index(id: int):

    for i, val in enumerate(my_posts):

        if val['id'] == id:
            return i

    return

# Where this id is a path parameter
@app.get("/posts/{id}")
def get_post(id: int, response : Response):

    post = find_post(id)

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"Post with {id} was not found"}

    return {"post_detail" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} does not exist")

    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    old_post_index = find_post_index(id)

    if old_post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} does not exist")

    new_post = post.model_dump()
    new_title = new_post['title']
    new_content = new_post['content']

    my_posts[old_post_index]['title'] = new_title
    my_posts[old_post_index]['content'] = new_content

    return {"data" : my_posts[old_post_index]}






