"""Script that will be traced."""
from yol_app.trace_logic import YolFunctionCall, YolStart


class Person:
  def __init__(self, name, age, address):
    self.name = name
    self.age = age
    self.address = address


@YolStart
def greet(nof_people, person_obj):
  return f"Hello, {person_obj.name}. Here are {nof_people} to greet!"


person = Person("Alice", 30, "123 Main St")
greet(5, person)
