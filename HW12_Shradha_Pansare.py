"""
Name: Shradha .M. Pansare
CWID: 10449587
"""
import sqlite3
from flask import Flask, render_template, request
app = Flask(__name__)

DB_FILE = "/Users/shradhapansare/Desktop/810_startup.db"

@app.route('/student_table')
def students_summary():
    data=[ #LIST OF STUDENTS
		{
			"cwid": "10102",
			"name": "Jobs, S",
			"major": "SFEN",
			"complete":2,
		},
		{
			"cwid": "10115",
			"name": "Bezos, J",
			"major": "SFEN",
			"complete":2,
		},
        {
            "cwid": "10183", 
            "name": "Musk, E",
            "major": "SFEN",
            "complete":2,
        },
        {
            "cwid":"11714",
            "name":"Gates, B",
            "major": "CS",
            "complete":3,
        }
	]
    return render_template("student_courses.html",title="Stevens Repository",table_title="Completed Courses by Students",student=data)
@app.route('/student')
def student_courses():
    dbpath='/Users/shradhapansare/Desktop/810_startup.db'
    try:
        db=sqlite3.connect(dbpath)
    except sqlite3.OperationalError:
        return ("Error: Unable to open database at {dbpath}")
    else:
        query = """ SELECT i.CWID, i.NAME, i.DEPT, g.COURSE, COUNT(*) AS student FROM instructors i JOIN grades g ON i.CWID=g.Instructor GROUP BY i.NAME, i.CWID, i.DEPT, g.COURSE """

        data=[{'cwid':CWID, 'name':NAME, 'major':MAJOR,'complete':COMPLETE} for CWID, NAME, MAJOR, COMPLETE in db.execute(query) ]
    
        db.close()
        return render_template('student_courses.html', title='Stevens Repository', table_title='Number of Completed Courses',student=data)


@app.route('/choose_student')
def choose_student():
    query= "SELECT CWID,NAME FROM student GROUP BY CWID,NAME"
    db = sqlite3.connect(DB_FILE)
    results = db.execute(query)
    student = [{'cwid':CWID,'name':NAME} for CWID, NAME in results]
    db.close()
    return render_template('student_form.html',student=student)

@app.route('/show_student' , method=['POST'])
def show_student():
    """ user chose a student from the form and now wants information"""

    if request.method == 'POST':
        cwid=request.form['cwid']
        query="SELECT COURSE,GRADE FROM grades WHERE StudentCWID=? "
        args=(cwid,)
        table_title=("Courses/Grades for CWID{cwid}")

        db=sqlite3.connect(DB_FILE)
        results = db.execute(query,args)
        rows=[{'COURSE':course,'GRADE':grade} for course, grade in results]
        db.close()

        return render_template('grade_form.html',title="Student Repository", table_title=table_title, rows=rows)

app.run(debug=True)

