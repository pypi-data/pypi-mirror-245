"""Script that will be traced."""
import time
import threading
from yol_app.trace_logic import YolFunctionCall, YolStart

#@YolStart(port=8990) (optional)
@YolStart
def main():
  # Create and start multiple threads
  threads_1 = [
    threading.Thread(target=call_vector_db, args=("query",)),
    threading.Thread(target=call_openai),
  ]

  for thread in threads_1:
    thread.start()

  for thread in threads_1:
    thread.join()

  some_ops()

  threads_2 = [
    threading.Thread(target=call_openai),
    threading.Thread(target=call_vector_db, args=("query",)),
  ]

  for thread in threads_2:
    thread.start()

  for thread in threads_2:
    thread.join()

@YolFunctionCall
def some_ops():
  time.sleep(0.2)
  threads = [
  threading.Thread(target=call_vector_db, args=("query",)),
  threading.Thread(target=call_openai),
]

  for thread in threads:
    thread.start()

  for thread in threads:
    thread.join()
  return "Some ops done."

@YolFunctionCall
def call_vector_db(query):
  query = query + "!"
  return create_prompt()

@YolFunctionCall
def create_prompt():
  time.sleep(0.2)
  return "Prompt created."

@YolFunctionCall
def call_openai():
  time.sleep(1)
  return {"data": "openai_data"}


if __name__ == "__main__":
  main()
