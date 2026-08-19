import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

#Database initialization function
def initialize_database():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT,
        done BOOLEAN
    )"""
    )
    #Checking if the database is empty
    cursor.execute("SELECT COUNT(*) FROM tasks")
    task_count = cursor.fetchone()[0]

    #Inserting basic tasks if the database is empty
    if task_count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title,done) VALUES (?, ?)",
            [
            ("Learn FastAPI in detail", True),
            ("Complete the clients project", False),
            ("Sleep on time", False),
            ]
        )

    conn.commit()
    conn.close()

#Initializing the database
initialize_database()

app = FastAPI(description = "A simple CRUD API built for flyrank internship assignment using FastAPI by Shayan Khan(shayandev123@gmail.com)")
#The tasks list
tasks = [{"id":1, "Title": "Learn FASTapi in detail", "Completed": True}
         ,{"id":2, "Title": "Complete the clients project", "Completed": False}
         ,{"id":3, "Title": "Sleep on time", "Completed": False}
         ,]

#Class for posting tasks
class TaskCreate(BaseModel):
    title: str

#Class for updating tasks
class TaskUpdate(BaseModel):
    title : str
    Completed : bool

@app.get("/",description = "returns a simple hello msg")
def hello():
    return {"message": "Hello, World!"}

#app description
@app.get("/describe",description = "returns a simple description of this project and the endpoints")
def get_describe():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }
#health check
@app.get("/health",description = "Returns a status whether or not the server is running")
def get_health():
    return {"status": "OK"}


#get method for the complete tasks list
@app.get("/tasks",description = "returns the list of tasks")
def tasks_list():
    return tasks

#Get method for a single task inside the tasks list using the id provided through the browser url
@app.get("/tasks/{task_id}",description = "returns the specific task through the id in the tasks list")
def get_task_id(task_id):
    for i in tasks:
        if int(task_id) == i["id"]:
            return i
    return "Not found 404"
    
#posting task endpoint
@app.post("/tasks",description = "Adds a new task in the tasks list")
def post_task(task: TaskCreate):
    if task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    else:
        new_task = {"id": len(tasks)+1, "Title": task.title, "Completed": False}
        tasks.append(new_task)
        return new_task


#updating task endpoint
@app.put("/tasks/{task_id}", description = "updates a specific task through the id")
def put_tasks(task_id, task: TaskUpdate):
    if task.title.strip() == "":
        raise HTTPException(status_code = 400, detail = "Empty/invalid body")
    else:
        for i in tasks:
            if int(task_id) == i["id"]:
                i["Title"] = task.title
                i["Completed"] = task.Completed
                return i
    return "Unknown id 404"


# deleting task endpoint
@app.delete("/tasks/{task_id}", description = "Deletes a task through the id")
def delete_task(task_id):
    for i in tasks:
        if int(task_id) == i["id"]:
            tasks.remove(i)
            return {"status": 204}
        return "Unknown id"

