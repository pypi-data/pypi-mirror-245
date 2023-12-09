"""nested list of objects as one classroom with a teacher and students"""
from yol_app.trace_logic import YolFunctionCall, YolStart


class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age


class Student:
  def __init__(self, name, grade):
    self.name = name
    self.grade = grade


class Classroom:
  def __init__(self, teacher_param, students_param):
    self.teacher = teacher_param
    self.students = students_param


@YolStart
def describe_classroom(classroom_obj):
  return f"{classroom_obj.teacher.name} teaches {len(classroom_obj.students)} students."


teacher = Person("Ella", 35)
students = [Student("Finn", "A"), Student("Grace", "B")]
classroom = Classroom(teacher, students)
describe_classroom(classroom)
