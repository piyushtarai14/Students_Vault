import sqlite3

def create_database():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            reg_no TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            cgpa REAL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
