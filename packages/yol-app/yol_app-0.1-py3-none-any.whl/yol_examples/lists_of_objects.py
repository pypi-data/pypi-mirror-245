"""list of objects example as employee list"""
from yol_app.trace_logic import YolFunctionCall, YolStart


class Employee:

  def __init__(self, emp_id, name, role):
    self.emp_id = emp_id
    self.name = name
    self.role = role


@YolStart
def list_employees(employees):
  return [f"{emp.name} works as a {emp.role}." for emp in employees]


employees_list = [
    Employee(1, "Charlie", "Developer"),
    Employee(2, "Daisy", "Manager"),
]
list_employees(employees_list)
