"""Script that will be traced."""
import time
from yol_app.trace_logic import YolFunctionCall, YolStart

# @YolStart(port=8990) (optional)


@YolStart
def main():
  call_vector_db("somequery", "somequeryextra", vector_db="somevectordb")
  call_openai("somequestion")


@YolFunctionCall
def call_vector_db(query, query_extra, vector_db="vectordb"):
  query = query + "!"
  time.sleep(3)  # simulate long runnung application
  return create_prompt("someprompt")


@YolFunctionCall
def create_prompt(prompt):
  time.sleep(2.2)  # simulate long runnung application
  return "Prompt created."


@YolFunctionCall
def call_openai(question):
  time.sleep(4.4)  # simulate long runnung application
  return {"data": "openai_data"}


if __name__ == "__main__":
  main()
