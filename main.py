import sqlite3
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel

# Load variables from the .env file
load_dotenv()

# Get the database path from .env, fallback to "tasks.db" if missing
DB_FILE = os.getenv("DATABASE_FILE", "tasks.db")

#Database initialization function
def initialize_database():
    # Ensure the directory for the database exists (crucial for Docker volumes)
    db_dir = os.path.dirname(DB_FILE)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
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
# tasks = [{"id":1, "Title": "Learn FASTapi in detail", "Completed": True}
#          ,{"id":2, "Title": "Complete the clients project", "Completed": False}
#          ,{"id":3, "Title": "Sleep on time", "Completed": False}
#          ,]

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
    conn = sqlite3.connect(DB_FILE)
    # row_factory formats the SQLite output into dictionaries automatically
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    
    return tasks

#Get method for a single task inside the tasks list using the id provided through the browser url
@app.get("/tasks/{task_id}",description = "returns the specific task through the id in the tasks list")
def get_task_id(task_id):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return dict(task)
    
#posting task endpoint
@app.post("/tasks",description = "Adds a new task in the tasks list", status_code = 201)
def post_task(task: TaskCreate):
    # Validation remains exactly the same
    if not task.title or task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")
        
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Insert the new task. We default 'done' to False (0 in SQLite)
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)", 
        (task.title, False)
    )
    conn.commit()
    
    # Retrieve the auto-generated ID for the new row
    new_task_id = cursor.lastrowid
    
    # Fetch the newly created task from the database to return it
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (new_task_id,))
    new_task = cursor.fetchone()
    
    conn.close()
    
    return dict(new_task)


#updating task endpoint
@app.put("/tasks/{task_id}", description = "updates a specific task through the id")
def put_tasks(task_id: int, task: TaskUpdate):
    if not task.title or task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Empty/invalid body")
        
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check if the task exists
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    existing_task = cursor.fetchone()
    
    if existing_task is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Unknown id 404")
        
    # Update the task
    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (task.title, task.Completed, task_id)
    )
    conn.commit()
    
    # Fetch the updated task to return it
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    updated_task = cursor.fetchone()
    conn.close()
    
    return dict(updated_task)


# deleting task endpoint
@app.delete("/tasks/{task_id}", description="Deletes a task through the id", status_code=204)
def delete_task(task_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check if the task exists
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    existing_task = cursor.fetchone()
    
    if existing_task is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Unknown id")
        
    # Delete the task
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    
    return Response(status_code=204)

