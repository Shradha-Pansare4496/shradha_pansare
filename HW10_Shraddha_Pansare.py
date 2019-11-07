"""
Name: Shradha Pansare
CWID: 10449587
"""
import os
from collections import defaultdict
from prettytable import PrettyTable
import unittest


def file_reader(path, num_fields, expect, sep='\t'):
    try:
        fp = open(path, "r", encoding="utf-8")
    except FileNotFoundError:
        print(" can't open:", path)
    else:
        with fp:
            for n, line in enumerate(fp, 1):
                fields = line.rstrip('\n').split(sep)
                if len(fields) == fields:
                    print("field not present")
                elif n == 1 and expect:
                    continue
                else:
                    yield (fields)


class Repository:
    """ creating repository  """

    def __init__(self, wdir, ptables=True):
        self._wdir = wdir
        self._students = dict()  # instance of class students
        self._instructors = dict()  # instance of class instructors
        self._majors = dict()  # instance of class majors

        self._get_instructors(os.path.join(wdir, 'instructors.txt'))
        self._get_majors(os.path.join(wdir, 'majors.txt'))
        self._get_students(os.path.join(wdir, 'students.txt'))
        self._get_grades(os.path.join(wdir, 'grades.txt'))

        if ptables:
            print("\nMajors Summary")
            self.major_table()
            print("\nStudent Summary")
            self.student_table()
            print("\nInstructors summary")
            self.instructor_table()

    def _get_students(self, path):  # to get student values
        try:
            for cwid, name, major in file_reader(path, 3, 'cwid;name;major', sep=';'):
                if cwid in self._students:
                    print(f"Already exits {cwid}")
                else:
                    self._students[cwid] = Student(cwid, name, major, self._majors[major])
        except ValueError as err:
            print(err)

    def _get_instructors(self, path):  # to get instructor values
        try:
            for cwid, name, dept in file_reader(path, 3, 'cwid|name|department', sep='|'):
                if cwid in self._instructors:
                    print(f"Already exits {cwid}")
                else:
                    self._instructors[cwid] = Instructor(cwid, name, dept)
        except ValueError as err:
            print(err)

    def _get_grades(self, path):  # to get grades
        try:
            for student_cwid, course, grade, instructor_cwid in file_reader(path, 4, 'StudentCWID|Course|Grade|InstructorCWID', sep='|'):
                if student_cwid in self._students:
                    self._students[student_cwid].add_course(course, grade)
                else:
                    print(f"Warning: student cwid {student_cwid} not exist")

                if instructor_cwid in self._instructors:
                    self._instructors[instructor_cwid].add_student(course)
                else:
                    print(f"Warning: Instructor cwid {instructor_cwid} not exist")

        except ValueError as err:
            print(err)

    def _get_majors(self, path):  # to get majors
        try:
            for major, flag, cours in file_reader(path, 3, 'major\tflag\tcours'):
                if major in self._majors:
                    self._majors[major].add_course(flag, cours)
                else:
                    self._majors[major] = Major(major)
                    self._majors[major].add_course(flag, cours)
        except ValueError as err:
            print(err)

    def major_table(self):  # prettytable for major
        pt = PrettyTable(field_names=['Major', 'Required', 'Elective'])
        for major in self._majors.values():
            pt.add_row(major.pt_row())
        print(pt)

    def student_table(self):  # prettytable for student
        pt = PrettyTable(field_names=['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required Courses',
                                      'Remaining Elective Courses'])
        # print(self._students)
        for student in self._students.values():
            pt.add_row(student.pt_row())
        print(pt)

    def instructor_table(self):  # prettytable for instructor
        pt = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        for ins in self._instructors.values():
            for row in ins.pt_row():
                pt.add_row(row)
        print(pt)


class Student:
    """ creating student class  """

    def __init__(self, cwid, name, major, in_major):
        self._cwid = cwid
        self._name = name
        self._major = major
        self._instr_major = in_major
        self.courses = dict()
        self.coursegrade = dict()
        self._courses = dict()

    def add_course(self, course, grade):
        Grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
        if grade in Grades:
            self._courses[course] = grade

    def add_course_grade(self, course, grade):
        self.coursegrade[course] = grade

    def student_info(self):
        return [self._cwid, self._name, sorted(self.coursegrade.keys())]

    def pt_row(self):
        complete_course, remaining_req_course, remaining_elective_course = self._instr_major.grade_check(self._courses)
        return [self._cwid, self._name, self._major, sorted(list(complete_course)), remaining_req_course,
                remaining_elective_course]


class Instructor:
    """ creating instructor class  """

    def __init__(self, cwid, name, dept):
        self._cwid = cwid
        self._name = name
        self._dept = dept
        self._courses = defaultdict(int)

    def add_student(self, course):
        self._courses[course] += 1

    def instr(self):
        for course, count in self._courses.items():
            return [self._cwid, self._name, self._dept, course, count]

    def pt_row(self):
        for course, students in self._courses.items():
            yield [self._cwid, self._name, self._dept, course, students]


class Major:
    """ creating major class """

    def __init__(self, major, passing=None):
        self._major = major
        self._required = set()
        self._elective = set()
        if passing is None:
            self._grades = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}
        else:
            self._grades = passing

    def add_course(self, flag, course):

        if flag == 'R':  # creating flag 'R' for required courses
            self._required.add(course)
        elif flag == 'E':  # creating flag 'E' for elective courses
            self._elective.add(course)
        else:
            raise ValueError(f"Unexcepted flag {flag}")

    def grade_check(self, courses):
        completed_course = {course for course, grade in courses.items() if grade in self._grades}
        if len(completed_course) == 0:  # if no courses are completed then student has to take all courses
            return [completed_course, self._required, self._elective]
        else:
            remaining_req_course = self._required - completed_course  # calculating remaining required courses
            if self._elective.intersection(completed_course):
                remaining_elective_course = None
            else:
                remaining_elective_course = self._elective  # calculating remaining elective courses
            return [completed_course, remaining_req_course, remaining_elective_course]

    def pt_row(self):
        return [self._major, self._required, self._elective]


def main():
    wdir = '/Users/shradhapansare/Desktop/test_repository'
    Stevens = Repository(wdir)

    """ performing unittesting """


"""class Test(unittest.TestCase):
     def test_major(self):  #testing the majors table
         
         actual_result = {'SFEN':('SFEN', {'SSW 540', 'SSW 564', 'SSW 555', 'SSW 567'}, {'CS 501', 'CS 513', 'CS 545'}),
                          'SYEN':('SYEN', {'SYS 671', 'SYS 612', 'SYS 800'}, {'SSW 810', 'SSW 540', 'SSW 565'})}
         expected_result = set()
         wdir = '/Users/shradhapansare/Desktop/test_repository'
         repo = Repository(wdir)
         for major in repo._majors.values():
             expected_result.add(major.pt_row())
         self.assertEqual(actual_result, expected_result)"""


if __name__ == '__main__':
    main()
    unittest.main(exit=False, verbosity=2)
