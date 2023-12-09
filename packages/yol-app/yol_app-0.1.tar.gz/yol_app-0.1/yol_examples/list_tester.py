from yol_app.trace_logic import YolFunctionCall, YolStart

@YolFunctionCall
def func1(a, b):
  return a+b

@YolFunctionCall
def func2(numbers):
  a = numbers[0]["a"]
  b = numbers[0]["b"]
  return a-b

@YolStart
def main():
  sum = func1(1, 2)
  diff = func2([1,2,3,4,5,6,7,8])

  return {"a": 1, "b": 2}

if __name__ == "__main__":
  main()