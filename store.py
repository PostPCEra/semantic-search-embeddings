import sqlite3

def connectToDB():
    conn = sqlite3.connect('tasks.db')
    return conn

def createTasksTable():
    try:
        conn = connectToDB()
        conn.execute('''DROP TABLE IF EXISTS tasks''')
        conn.execute('''
            CREATE TABLE tasks (
                id TEXT PRIMARY KEY NOT NULL,
                taskId TEXT NOT NULL
            );
        ''')
        conn.commit()
        print("Tasks table created successfully")
    except:
        print("Tasks table creation failed")
    finally:
        conn.close()

def insertTask(task):
    insertedTask = {}
    try:
        conn = connectToDB()
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (id, taskId) VALUES (?, ?)", (task['id'], task['taskId']) )
        conn.commit()
        insertedTask = getTaskById(cur.lastrowid)
    except:
        conn().rollback()
    finally:
        conn.close()
    return insertedTask

def doesIdExists(id):
    task = {}
    try:
        conn = connectToDB()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE id = ?", (id,))
        row = cur.fetchone()
        # convert row object to dictionary
        task["taskId"] = row["taskId"]
        task["id"] = row["id"]
    except:
        task = {}

    return task

def getTaskById(taskId):
    task = {}
    try:
        conn = connectToDB()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE taskId = ?", (taskId,))
        row = cur.fetchone()
        # convert row object to dictionary
        task["taskId"] = row["taskId"]
        task["id"] = row["id"]
    except:
        task = {}

    return task