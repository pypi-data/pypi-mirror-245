from yol_app.trace_logic import YolFunctionCall, YolStart

@YolFunctionCall
def func1(a, b):
  return a+b

@YolFunctionCall
def func2(numbers):
  a = numbers[0]["a"]
  b = numbers[0]["b"]
  return a-b

@YolFunctionCall
def func3(numbers):
  return numbers

@YolStart
def main():
  sum = func1(1, 2)
  diff = func2([{"a": 1, "b": 2, "nest": {"a": 1, "b": 2, "C": {"a": 1, "b": {"a": 1, "b": {"a": 1, "b": {"a": 1, "b": 2}}}}}}])
  func3([{"a": 1, "b": 2, "nest": {"a": 1, "b": 2, "C": {"a": 1, "b": {"a": 1, "b": {"a": 1, "b": {"a": 1, "b": 2}}}}}}])

  return {"a": 1, "b": 2}

if __name__ == "__main__":
  main()