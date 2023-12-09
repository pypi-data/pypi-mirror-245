"""Script that will be traced."""
from yol_app.trace_logic import YolFunctionCall, YolStart

@YolStart
def main():
  func1(func2, print)

@YolFunctionCall
def func1(a, b):
  a(3)
  b(4)

@YolFunctionCall
def func2(x):
  print_function = func3()
  print_function(x)

@YolFunctionCall
def func3():
  return print

if __name__ == "__main__":
  main()
