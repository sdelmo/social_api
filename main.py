from fastapi import FastAPI

app = FastAPI()

# This is a path operation / route
# decorator app.get modifies the behavior of root func to turn it into an api function
# async calls we use async keyword for, such as api calls
# the function converts python dicts to json to user

@app.get("/")
async def root():
    return {"message" : "Hello World!"}

@app.get("/posts")
def get_posts():
    return {"data" : "These are your posts"}



