import psycopg2
from task import Task


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
        cursor.close()
        conn.close()        

def get_tasks_from_db():
    cursor,conn=connect_to_database()
    cursor.execute("select * from web_app.tasks")  
    tasks = [Task(id=str(t[0]), author=t[1], deadline=t[2], title=t[3], description=t[4]) for t in cursor.fetchall()  ]
    cursor.close()
    conn.close()    
    return tasks








