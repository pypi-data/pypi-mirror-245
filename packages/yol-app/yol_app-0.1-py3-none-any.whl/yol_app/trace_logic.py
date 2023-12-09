"""
Copyright 2023 NeuralBridge AI

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
 
"""
Tracing Module: YolApp
======================

This module provides a versatile approach for tracing function calls in your Python codebase.
The primary objective is to enable a deeper insight into the behavior of functions by recording
details like call hierarchy, execution time (latency), source code, arguments, and return values.

How to Use:
------------
1. Decorate functions you want to trace using `@YolFunctionCall`.
2. To initiate tracing, decorate the primary function (e.g., `main()`) using `@YolStart`.
3. Simply run your code, and the trace data will be available on a local web server.

Example:

from yol_app.trace_logic import YolFunctionCall, YolStart

@YolStart
def main():
    call_vector_db("query")
    call_openai()

@YolFunctionCall
def call_vector_db(query):
    ...

@YolFunctionCall
def create_prompt():
    ...

@YolFunctionCall
def call_openai():
    ...

if __name__ == "__main__":
    main()

Note:
-----
- The trace details are accessible via a local web server,
which is initiated when you execute the main function.
- The optional parameter `port` in the `@YolStart` decorator allows
specifying a custom port for the web server.
"""

import time
import inspect
import uvicorn
import threading
from functools import wraps


class TraceManager:
  """Trace Manager Class for tracing function calls."""

  def __init__(self):
    self.should_trace = False
    self.call_stacks = {}
    self.thread_parents = {}
    self.main_output = []
    self.call_counts = {}

  def enter(self, func_name, args, kwargs):
    tid = threading.get_ident()

    if tid not in self.call_stacks:
      self.call_stacks[tid] = []

    call_stack_names = [call["function_name"] for call in self.call_stacks[tid]]
    call_stack_key = (*call_stack_names, func_name, tid)
    self.call_counts[call_stack_key] = self.call_counts.get(call_stack_key, 0) + 1

    call = {
        "function_name": func_name,
        "args": args,
        "kwargs": kwargs,
        "thread_id": tid,
        "children": [],
        "call_count": self.call_counts[call_stack_key],
    }
    # Check if there is a parent call on the stack for this thread
    # and add the current call as its child.
    if self.call_stacks[tid]:
      parent_call = self.call_stacks[tid][-1]
      parent_call["children"].append(call)
    else:
      # Check if this thread was spawned directly (e.g., from main),
      # and use the main's last call as the parent.
      main_tid = threading.main_thread().ident
      if tid != main_tid and main_tid in self.call_stacks and self.call_stacks[main_tid]:
        parent_call = self.call_stacks[main_tid][-1]
        parent_call["children"].append(call)
      else:
        self.main_output.append(call)

    # Add current call to the thread's stack.
    self.call_stacks[tid].append(call)

    return call

  def exit(self, call, details):
    tid = threading.get_ident()
    call.update(details)
    # Remove the call from the thread's stack once it's done.
    self.call_stacks[tid].pop()

  def enable_tracing(self):
    self.should_trace = True

  def disable_tracing(self):
    self.should_trace = False

  def get_trace_output(self):
    return self.main_output


trace_manager = TraceManager()


def YolFunctionCall(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    if not trace_manager.should_trace:
      return f(*args, **kwargs)

    serialized_args = [{"value": repr(arg), "type": type(arg).__name__} if callable(arg) else {
        "value": arg, "type": type(arg).__name__} for arg in args]
    serialized_kwargs = {k: {"value": repr(kwarg), "type": type(kwarg).__name__} if callable(
        kwarg) else {"value": kwarg, "type": type(kwarg).__name__} for k, kwarg in kwargs.items()}

    call = trace_manager.enter(f.__name__, serialized_args, serialized_kwargs)

    # Get the function signature for 'f' and bind the provided args and kwargs.
    # Convert bound arguments to a dict to then replace "args" key of call dict.
    signature = inspect.signature(f)
    bound_args = signature.bind(*serialized_args, **serialized_kwargs)
    bound_args.apply_defaults()

    args_dict = {}
    kwargs_dict = {}

    for param_name, param in signature.parameters.items():
      if param.default is param.empty:  # Parameter is positional
        args_dict[param_name] = bound_args.arguments[param_name]
      else:  # Parameter is keyword
        kwargs_dict[param_name] = bound_args.arguments[param_name]

    call["args"] = args_dict
    call["kwargs"] = kwargs_dict

    start_time = time.time()
    result = f(*args, **kwargs)
    if callable(result):
      result_representation = str(result)
    else:
      result_representation = result
    end_time = time.time()
    latency = end_time - start_time
    source_code = inspect.getsource(f)

    trace_manager.exit(call, {
        "return": result_representation,
        "latency": latency,
        "source_code": source_code,
        "return_type": type(result).__name__
    })

    return result

  return wrapper


def YolStart(func=None, *, port=8235):
  if func is None:
    return lambda func: YolStart(func, port=port)

  @wraps(func)
  def wrapper(*args, **kwargs):
    print("********* YOL ***********")
    print(f"http://localhost:{port}")
    print("*************************")

    # Start the web server on a separate thread to allow tracing to continue in parallel.
    threading.Thread(target=lambda: uvicorn.run("yol_app.server:app",
                     host="0.0.0.0", port=port, log_level="error")).start()

    time.sleep(2)  # Give the server a moment to start up

    trace_manager.enable_tracing()

    serialized_args = [{"value": repr(arg), "type": type(arg).__name__} if callable(arg) else {
        "value": arg, "type": type(arg).__name__} for arg in args]
    serialized_kwargs = {k: {"value": repr(kwarg), "type": type(kwarg).__name__} if callable(
        kwarg) else {"value": kwarg, "type": type(kwarg).__name__} for k, kwarg in kwargs.items()}

    call = trace_manager.enter(func.__name__, serialized_args, serialized_kwargs)

    # Get the function signature for 'f' and bind the provided args and kwargs.
    # Convert bound arguments to a dict to then replace "args" key of call dict.
    signature = inspect.signature(func)
    bound_args = signature.bind(*serialized_args, **serialized_kwargs)
    bound_args.apply_defaults()

    args_dict = {}
    kwargs_dict = {}

    for param_name, param in signature.parameters.items():
      if param.default is param.empty:  # Parameter is positional
        args_dict[param_name] = bound_args.arguments[param_name]
      else:  # Parameter is keyword
        kwargs_dict[param_name] = bound_args.arguments[param_name]

    call["args"] = args_dict
    call["kwargs"] = kwargs_dict

    start_time = time.time()
    result = func(*args, **kwargs)
    if callable(result):
      result_representation = str(result)
    else:
      result_representation = result
    end_time = time.time()
    latency = end_time - start_time
    source_code = inspect.getsource(func)

    trace_manager.exit(call, {
        "return": result_representation,
        "latency": latency,
        "source_code": source_code,
        "return_type": type(result).__name__
    })

    trace_manager.disable_tracing()

    return result

  return wrapper
