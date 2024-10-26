from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
# Ensure that returns from psycopg have column names with realdict
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):

    title: str
    content: str
    published: bool = True

# Connect to db

while True:
    try:
        conn = psycopg2.connect(
        host = 'localhost',
        database = 'fastapi',
        user = input('input username: '),
        password = None,
        cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print(">>Database connection was successful<<")
        break

    except Exception as e:

        print(">>Connection to database failed<<")
        print("Error: ", e)
        # Retry every two seconds in case of db connection failing
        time.sleep(2)

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

    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()

    return {"data" : posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # Sanitize data to prevent sql injections
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published)
    )

    new_post = cursor.fetchone()
    conn.commit()

    return {"new_post" : new_post}

# Where this id is a path parameter
@app.get("/posts/{id}")
def get_post(id: int, response : Response):

    cursor.execute(
        """SELECT * FROM posts WHERE id = %s""",
        (str(id))
    )

    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} was not found")

    return {"post_detail" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""",
        (str(id))
    )

    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, str(id))
    )

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} does not exist")

    return {"data" : updated_post}






