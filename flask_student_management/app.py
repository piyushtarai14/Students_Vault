from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=('GET', 'POST'))
def add_student():
    if request.method == 'POST':
        reg_no = request.form['reg_no']
        name = request.form['name']
        age = request.form['age']
        cgpa = request.form['cgpa']

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO students (reg_no, name, age, cgpa) VALUES (?, ?, ?, ?)',
                         (reg_no, name, age, cgpa))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Registration number already exists. Please use a unique reg_no."
        finally:
            conn.close()
        return redirect(url_for('index'))
    
    return render_template('add_student.html')

@app.route('/edit/<reg_no>', methods=('GET', 'POST'))
def edit_student(reg_no):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE reg_no = ?', (reg_no,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        cgpa = request.form['cgpa']

        conn.execute('UPDATE students SET name = ?, age = ?, cgpa = ? WHERE reg_no = ?',
                     (name, age, cgpa, reg_no))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_student.html', student=student)

@app.route('/delete/<reg_no>', methods=('POST',))
def delete_student(reg_no):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE reg_no = ?', (reg_no,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
