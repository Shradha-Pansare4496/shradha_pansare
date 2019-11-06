"""
Name: Shradha Pansare
CWID: 10449587
"""
from collections import defaultdict
from prettytable import PrettyTable
import unittest
import os


""" using file_reading_gen from HW08  """
def file_reading_gen(path, fields, sep='\t' , header=False):
    #path="/Users/shradhapansare/Desktop/HW09_Shraddha_Pansare.py"
    try:
        fp=open(path,"r")
    except FileNotFoundError:
        raise FileNotFoundError("cant open path")
    else:
        with fp:
            for n, line in enumerate(fp,1):
                fields = line.rstrip('\n').split(sep)
                if len(fields)==fields:
                    print("field not present")
                elif n==1 and header:
                    continue
                else:
                    yield (fields)

class Student:
    """ creating student class  """
    def __init__(self, cwid, name, major):
        #path="/Users/shradhapansare/Desktop/student.txt"
        self._cwid = cwid
        self._name = name
        self._major = major
        self.courses = dict()
        self.coursegrade=dict()
        
    def add_course(self, course, grade):
        self.courses[course] = grade
    def add_course_grade(self,course,grade):
        self.coursegrade[course] = grade
        
    def student_info(self):
        return [self._cwid, self._name, sorted(self.coursegrade.keys())] 
    def pt_row(self):
        return [self._cwid, self._name, sorted(self.courses.keys())]


class Instructor:
    """ creating instructor class  """
    def __init__(self, cwid, name, dept):
       # path="/Users/shradhapansare/Desktop/instructor.txt"
        self._cwid = cwid
        self._name = name
        self._dept = dept
        self.courses = defaultdict(int)

    def add_student(self, course):
        self.courses[course] += 1
    def instr(self):
        for course, count in self.courses.items():   
            return [self._cwid, self._name, self._dept, course, count]
    def pt_row(self):
        for course, count in self.courses.items():
            yield [self._cwid, self._name, self._dept, course, count]


class Repository:
        """ creating repository  """
        def __init__(self, path, ptables=True):
            os.chdir(path)
            self.students = dict()
            self.instructors = dict()
            self._get_students("students.txt")
            self._get_instructors("instructors.txt")
            self._get_grades("grades.txt")
            print("\n Student Summary \n")
            self.student_table()
            print("\n Instructor Summary \n")
            self.instructor_table()

        def _get_students(self,path):
            for cwid,name,major in file_reading_gen(path,3,'\t', False):
                self.students[cwid] = Student(cwid,name,major)

        def _get_instructors(self, path):
            #for cwid, name, dept in file_reading_gen(path, 3, 'cwid\tname\tdept'):
            for cwid,name,dept in file_reading_gen(path,3,'\t', False):
                self.instructors[cwid] = Instructor(cwid, name, dept)
        
        def _get_grades(self, path):
            #for student_cwid,course,grade,instructor_cwid in file_reading_gen(path, 4, 'student_cwid\tcourse\tgrade\tinstructor_cwid'):
            for student_cwid,course,grade,instructor_cwid in file_reading_gen(path, 4, '\t', False):
                if student_cwid in self.students:
                    self.students[student_cwid].add_course(course, grade)
                else:
                    print("Unknown student grade present '{}'".format(student_cwid))

                if instructor_cwid in self.instructors:
                    self.instructors[instructor_cwid].add_student(course)
                else:
                    print("Unknown instructor grade present '{}'".format(instructor_cwid))

        def student_table(self):  #to print 3 fields in student summary - cwid, name, completed courses
            pt = PrettyTable(field_names=['CWID','Name','Completed Courses'])
            for student in self.students.values():
                pt.add_row(student.pt_row())
            print(pt)

        def instructor_table(self):
            pt = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Student'])  #to print 4 fields in instructor table
            for instructor in self.instructors.values():
                for row in instructor.pt_row():
                    pt.add_row(row)
            print(pt)

def omain():
    path="/Users/shradhapansare/Desktop/test_repository"
    repository = Repository(path)
    
    print("\n Student Summary \n")
    repository.student_table()

    print("\n Instructor Summary \n")
    repository.instructor_table()
    
    """  to perform unittesting  """
class InstructorTest(unittest.TestCase): 
    def test_instructor(self):
        """ test case for instructor  """
        instructor = Instructor('98763','Newton, I','SYEN')
        instructor.add_student('Morton, A')
        self.assertEqual(instructor.instr(),['98763', 'Newton, I', 'SYEN', 'Morton, A', 1])

class StudentsTest(unittest.TestCase):
    def test_student(self):
        """ test case for student info """
        student = Student('11788',' Fuller, E ',' SYEN')
        student.add_course_grade('SSW 555', 'A')
        self.assertEqual(student.student_info(), ['11788',' Fuller, E ', ['SSW 555']])

def main():
    wdir09 = '/Users/shradhapansare/Desktop/HW09_Repository'
    wdir10 = '/Users/shradhapansare/Desktop/HW09_Repository'
    wdir_bad_data = '/Users/shradhapansare/Desktop/HW09_Repository_BadData'

    print("Good data")
    _ = Repository(wdir09)

    print("\nBad Data")
    print("should report unknown student and unknown instructor")
    _ = Repository(wdir_bad_data)

    print("\nBad Fields\n")
    print("should report bad student, grade, instructor feeds")
    _ = Repository(wdir10)
    
    

if __name__ == '__main__':
    main()
        
if __name__ == '__main__':
    main()
