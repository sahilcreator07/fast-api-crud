from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware   #cross-origin-resource-sharing (CORSM)
from model import Todo


app = FastAPI()

from database import (
    fetch_one_todo,
    fetch_all_todo,
    create_todo,
    update_todo,
    remove_todo
)

origin = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=origin,
    allow_methods=["*"],
    allow_headers=["*"],
    )

@app.get("/")
def read_root():
    return "listing"

#CRUD methods
@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todo()
    return response

@app.get("/api/todo/{title}", response_model= Todo)
async def get_todo_by_id(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"there no such TODO title  with this title name {title}")


@app.post("/api/todo", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, f"something went wrong, Bad request")


@app.put("/api/todo{title}", response_model=Todo)
async def update_todo(title: str, data: str):
    response = await update_todo(title, data)
    if response:
        return response
    raise HTTPException(404, f"No TODO with this name {title}")


@app.delete("/api/todo{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return "succesfully deleted tdod item"
    raise HTTPException(404, f"No TODO with this name {title}")