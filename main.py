from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
#The tasks list
tasks = [{"id":1, "Title": "Learn FASTapi in detail", "Completed": True}
         ,{"id":2, "Title": "Complete the clients project", "Completed": False}
         ,{"id":3, "Title": "Sleep on time", "Completed": False}
         ,]

#Class for posting tasks
class TaskCreate(BaseModel):
    title: str

@app.get("/")
def hello():
    return {"message": "Hello, World!"}

#app description
@app.get("/describe")
def get_describe():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }
#health check
@app.get("/health")
def get_health():
    return {"status": "OK"}


#get method for the complete tasks list
@app.get("/tasks")
def tasks_list():
    return tasks

#Get method for a single task inside the tasks list using the id provided through the browser url
@app.get("/tasks/{task_id}")
def get_task_id(task_id):
    for i in tasks:
        if int(task_id) == i["id"]:
            return i
    return "Not found 404"
    
#posting task endpoint
@app.post("/tasks")
def post_task(task: TaskCreate):
    if task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    else:
        new_task = {"id": len(tasks)+1, "Title": task.title, "Completed": False}
        tasks.append(new_task)
        return new_task

