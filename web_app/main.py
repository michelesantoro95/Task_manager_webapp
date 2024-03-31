from fastapi import FastAPI, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from task import Task


templates = Jinja2Templates(directory="templates")

app=FastAPI()
tasks=[]


@app.get("/")
async def root(request:Request):
    return templates.TemplateResponse("base_template.html",
                                      {"request": request,"tasks":tasks})

@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("add_new_task.html", {"request": request})

@app.get("/edit_task/{task_id}")
async def edit(request: Request, task_id: str):
   for t in tasks:
       if task_id==t.id:
            task=t
   return templates.TemplateResponse("edit_task.html", {"request": request, "task":task})

@app.post("/add_task_html")
async def add(request: Request,id: str = Form(...),author: str = Form(...), deadline: str = Form(...), title: str = Form(...),description: str = Form(...)):
    task = Task(id=id,author=author, deadline=deadline, title=title,description=description)
    tasks.append(task)
    return RedirectResponse(url=app.url_path_for("root"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{task_id}")
async def delete(request: Request, task_id: str):
   for t in tasks:
       if task_id==t.id:
         tasks.remove(t)
   return RedirectResponse(url=app.url_path_for("root"), status_code=status.HTTP_303_SEE_OTHER)


@app.post("/update_task/{task_id}")
async def add(request: Request,id: str = Form(...),author: str = Form(...), deadline: str = Form(...), title: str = Form(...),description: str = Form(...)):

    for t in tasks:
        if id==t.id:    
            t.author=author
            t.deadline=deadline
            t.title=title
            t.description=description            
            
    return RedirectResponse(url=app.url_path_for("root"), status_code=status.HTTP_303_SEE_OTHER)










