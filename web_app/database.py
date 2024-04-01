# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from task import Task
# DB_NAME = "master"
# DB_USER = "postgres"
# DB_PASS = "1234"
# DB_HOST = "localhost"
# DB_PORT = "5432"

# db_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
# engine = create_engine(
#     db_url, connect_args={}
# )






def connect_to_database():
    DB_NAME = "master"
    DB_USER = "postgres"
    DB_PASS = "1234"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    db_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    conn = psycopg2.connect(  db_url )
    cursor=conn.cursor()
    return cursor,conn


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








