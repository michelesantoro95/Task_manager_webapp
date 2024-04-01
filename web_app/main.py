from fastapi import FastAPI, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import SessionLocal,engine,connect_to_database
from task import Task
import task
task.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")
app=FastAPI()
# tasks=[]

def get_new_id():
    cursor,_=connect_to_database()
    sql = "SELECT id FROM web_app.tasks"
    cursor.execute(sql)
    id_values = [row[0] for row in cursor.fetchall()] 
    print(id_values)
    lowest_integer = 1
    while lowest_integer in id_values:
        lowest_integer += 1       
    return(lowest_integer)

def write_task_db(task):
        cursor,conn=connect_to_database()
        values=(task.id,task.author,task.deadline,task.title,task.description)
        sql = "INSERT INTO  web_app.tasks (id, author, deadline, title,description) VALUES (%s, %s, %s, %s, %s)"        
        cursor.execute(sql, values)
        conn.commit()

def get_tasks_from_db():
    cursor,_=connect_to_database()
    cursor.execute("select * from web_app.tasks")  
    tasks = [Task(id=str(t[0]), author=t[1], deadline=t[2], title=t[3], description=t[4]) for t in cursor.fetchall()  ]
    return tasks
     

@app.get("/")
async def root(request:Request):
    tasks=get_tasks_from_db()
    return templates.TemplateResponse("base_template.html",
                                      {"request": request,"tasks":tasks})

@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("add_new_task.html", {"request": request})

@app.get("/edit_task/{task_id}")
async def edit(request: Request, task_id: str):
   tasks=get_tasks_from_db()
   for t in tasks:
       if task_id==t.id:
            task=t
   return templates.TemplateResponse("edit_task.html", {"request": request, "task":task})

@app.post("/add_task_html")
async def add(request: Request,author: str = Form(...), deadline: str = Form(...), title: str = Form(...),description: str = Form(...)):
    new_id=get_new_id()
    print(new_id)
    task = Task(id=str(new_id),author=author, deadline=deadline, title=title,description=description)
    write_task_db(task)
    return RedirectResponse(url=app.url_path_for("root"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{task_id}")
async def delete(request: Request, task_id: str):
   cursor,conn=connect_to_database()
   sql=f"DELETE FROM web_app.tasks WHERE id = {task_id}"
   cursor.execute(sql)
   conn.commit()
   return RedirectResponse(url=app.url_path_for("root"), status_code=status.HTTP_303_SEE_OTHER)


@app.post("/update_task/{task_id}")
async def add(request: Request,id: str = Form(...),author: str = Form(...), deadline: str = Form(...), title: str = Form(...),description: str = Form(...)):
    cursor,conn=connect_to_database()
    sql = "UPDATE web_app.tasks SET author = %s, deadline = %s, title = %s, description = %s WHERE id = %s"
    cursor.execute(sql, (author, deadline, title, description, id))
    conn.commit()                      
    return RedirectResponse(url=app.url_path_for("root"), status_code=status.HTTP_303_SEE_OTHER)










