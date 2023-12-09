"""example of nested objects as person as house owner"""
from yol_app.trace_logic import YolFunctionCall, YolStart


class Person:

  def __init__(self, name, age):
    self.name = name
    self.age = age


class House:

  def __init__(self, address, owner):
    self.address = address
    self.owner = owner


@YolStart
def describe_house(house_obj):
  return f"{house_obj.address} is owned by\
  {house_obj.owner.name} who is {house_obj.owner.age} years old."


ownerP = Person("Bob", 40)
house = House("456 Main St", ownerP)
describe_house(house)
