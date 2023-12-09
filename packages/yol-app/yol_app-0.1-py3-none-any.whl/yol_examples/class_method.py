"""Example of class method."""
from yol_app.trace_logic import YolFunctionCall, YolStart

class TestClass:
  """Test class."""
  def __init__(self):
    self.name = 'TestClass'

  @YolFunctionCall
  def test_method(self):
    print('test_method')

  @YolFunctionCall
  def class_method(self, cls):
    print('class_method' + cls)

  @YolFunctionCall
  def static_method(self):
    print('static_method')

testObj = TestClass()

@YolStart
def main():
  testObj.test_method()
  testObj.class_method('this is test class')
  testObj.static_method()

if __name__ == '__main__':
  main()
