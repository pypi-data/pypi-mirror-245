"""A complex school simulation example"""
from yol_app.trace_logic import YolFunctionCall, YolStart


class Subject:

  def __init__(self, name, grade):
    self.name = name
    self.grade = grade


class Student:

  def __init__(self, name, subjects):
    self.name = name
    self.subjects = subjects


class Teacher:

  def __init__(self, name, main_subject):
    self.name = name
    self.main_subject = main_subject


class Classroom:

  def __init__(self, teacher, students):
    self.teacher = teacher
    self.students = students


class School:

  def __init__(self, name, classrooms):
    self.name = name
    self.classrooms = classrooms


@YolStart
def describe_school(school_obj):
  return f"{school_obj.name } has {len(school_obj.classrooms)} classrooms."


# Example usage
math_teacher = Teacher("Mr. Anderson", "Math")
english_teacher = Teacher("Ms. Smith", "English")

students_class1 = [
    Student("John", [Subject("Math", "A"), Subject("English", "B")]),
    Student("Emma", [Subject("Math", "B"), Subject("English", "A")]),
]

students_class2 = [
    Student("Liam", [Subject("Math", "C"), Subject("English", "B")]),
    Student("Olivia", [Subject("Math", "B+"), Subject("English", "A-")]),
]

classroom1 = Classroom(math_teacher, students_class1)
classroom2 = Classroom(english_teacher, students_class2)

school = School("Greenwood High", [classroom1, classroom2])
describe_school(school)
