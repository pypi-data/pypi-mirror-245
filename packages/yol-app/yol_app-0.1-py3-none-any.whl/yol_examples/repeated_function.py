from yol_app.trace_logic import YolFunctionCall, YolStart


@YolStart
def main():
  func1()
  func3()

@YolFunctionCall
def func1():
  for i in range(5):
    func2(i)

@YolFunctionCall
def func2(i):
  print(i)
  return f"{i} world"

@YolFunctionCall
def func3():
  func1()

if __name__ == "__main__":
  main()
