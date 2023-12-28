import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def execute_sql(conn, sql):
    """Execute SQL query"""
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def create_tables(conn):
    """Create projects and tasks tables"""
    create_projects_sql = """
    CREATE TABLE IF NOT EXISTS projects (
        id integer PRIMARY KEY,
        name text NOT NULL,
        start_date text,
        end_date text
    );
    """
    create_tasks_sql = """
    CREATE TABLE IF NOT EXISTS tasks (
        id integer PRIMARY KEY,
        project_id integer NOT NULL,
        name VARCHAR(250) NOT NULL,
        description TEXT,
        status VARCHAR(15) NOT NULL,
        start_date text NOT NULL,
        end_date text NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    );
    """
    execute_sql(conn, create_projects_sql)
    execute_sql(conn, create_tasks_sql)

def insert_project(conn, project):
    """Insert a new project into the projects table"""
    sql = '''INSERT INTO projects(name, start_date, end_date)
             VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def insert_task(conn, task):
    """Insert a new task into the tasks table"""
    sql = '''INSERT INTO tasks(project_id, name, description, status, start_date, end_date)
             VALUES(?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid

def select_all_tasks(conn):
    """Query all tasks"""
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    return rows

def update_task(conn, id, update_data):
    """Update a task"""
    sql = '''UPDATE tasks SET name = ?, description = ?, status = ?, start_date = ?, end_date = ?
             WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (*update_data, id))
    conn.commit()

def delete_task(conn, id):
    """Delete a task by task id"""
    sql = 'DELETE FROM tasks WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def main():
    database = "example.db"

    conn = create_connection(database)

    with conn:
        create_tables(conn)

        project = ('Cool Project', '2020-01-01', '2020-12-31')
        project_id = insert_project(conn, project)

        task_1 = (project_id, 'Analysis', 'Data analysis', 'started', '2020-01-05', '2020-01-10')
        task_2 = (project_id, 'Development', 'Develop features', 'pending', '2020-02-01', '2020-03-01')
        insert_task(conn, task_1)
        insert_task(conn, task_2)

        print("All tasks:", select_all_tasks(conn))

        update_data = ('Design', 'UI/UX Design', 'completed', '2020-01-15', '2020-01-20')
        update_task(conn, 1, update_data)

        delete_task(conn, 2)

        print("Tasks after update and delete:", select_all_tasks(conn))

if __name__ == '__main__':
    main()
