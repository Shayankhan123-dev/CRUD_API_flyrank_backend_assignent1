from fastapi import FastAPI

app = FastAPI()
#The tasks list
tasks = [{"id":1, "Title": "Learn FASTapi in detail", "Completed": True}
         ,{"id":2, "Title": "Complete the clients project", "Completed": False}
         ,{"id":3, "Title": "Sleep on time", "Completed": False}
         ,]



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

