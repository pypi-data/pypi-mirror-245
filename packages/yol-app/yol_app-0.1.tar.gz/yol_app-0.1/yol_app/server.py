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
 
"""This module contains server of yol_app."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from yol_app.trace_logic import trace_manager
from typing import List
import os

app = FastAPI()

current_directory = os.path.dirname(os.path.abspath(__file__))
static_directory = os.path.join(current_directory, "trace_display", "build", "static")
index_file_path = os.path.join(current_directory, "trace_display", "build", "index.html")


# Serve React build as static files
app.mount("/static", StaticFiles(directory=static_directory), name="static")

trace_output = []

@app.get("/")
def read_root():
  return FileResponse(index_file_path)

@app.get("/trace")
def get_trace():
  output = trace_manager.get_trace_output()
  #trace_manager.reset_trace_output()  # Clear the output once it's been fetched
  return output

