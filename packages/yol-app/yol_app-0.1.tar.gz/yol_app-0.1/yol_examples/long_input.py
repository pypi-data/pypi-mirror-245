"""Script that will be traced."""
import time
from yol_app.trace_logic import YolFunctionCall, YolStart

# @YolStart(port=8990) (optional)


@YolStart
def main():
  call_vector_db("query", "query", "query", "query", "query", "query", "query")
  call_openai()


@YolFunctionCall
def call_vector_db(query, query1, query2, query3, query4, query5, query6):
  query = query + "!"
  time.sleep(3)  # simulate long runnung application
  return create_prompt()


@YolFunctionCall
def create_prompt():
  time.sleep(2.2)  # simulate long runnung application
  return "Prompt created.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


@YolFunctionCall
def call_openai():
  time.sleep(4.4)  # simulate long runnung application
  return {"data": "openai_data"}


if __name__ == "__main__":
  main()
