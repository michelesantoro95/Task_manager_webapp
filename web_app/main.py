from fastapi import FastAPI, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from mangum import Mangum
from database import connect_to_database,write_task_db,get_tasks_from_db
from task import Task

templates = Jinja2Templates(directory="templates")
app=FastAPI()
handler=Mangum(app)


def get_new_id():
    cursor,_=connect_to_database()
    sql = "SELECT id FROM web_app.tasks"
    cursor.execute(sql)
    id_values = [row[0] for row in cursor.fetchall()] 
    lowest_integer = 1
    while lowest_integer in id_values:
        lowest_integer += 1       
    return(lowest_integer)


     

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
    task = Task(id=str(new_id),author=author, deadline=deadline, title=title,description=description)
    write_task_db(task)
    return RedirectResponse(url=app.url_path_for("root"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{task_id}")
async def delete(request: Request, task_id: str):
   cursor,conn=connect_to_database()
   sql=f"DELETE FROM web_app.tasks WHERE id = {task_id}"
   cursor.execute(sql)
   conn.commit()
   cursor.close()
   conn.close()   
   return RedirectResponse(url=app.url_path_for("root"), status_code=status.HTTP_303_SEE_OTHER)

@app.post("/update_task/{task_id}")
async def add(request: Request,id: str = Form(...),author: str = Form(...), deadline: str = Form(...), title: str = Form(...),description: str = Form(...)):
    cursor,conn=connect_to_database()
    sql = "UPDATE web_app.tasks SET author = %s, deadline = %s, title = %s, description = %s WHERE id = %s"
    cursor.execute(sql, (author, deadline, title, description, id))
    conn.commit()  
    cursor.close()
    conn.close()                        
    return RedirectResponse(url=app.url_path_for("root"), status_code=status.HTTP_303_SEE_OTHER)










