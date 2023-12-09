## Yol Recorder

Yol Recorder is a tool designed to trace Python function calls and visualize them through a web interface, allowing developers to monitor and analyze ,their application's function call flows in real-time.

### Running Test Script

1. Clone the repository:

   ```
   git clone https://github.com/Neural-Bridge/yol-recorder.git
   ```

2. Install Python Dependencies:

   Navigate to the root directory of the project and install the required Python packages:

   ```
   cd yol-recorder
   pip install -r requirements.txt
   ```

3. Navigate to the `trace_display` folder and install the required dependencies:

   ```
   cd yol_app
   cd trace_display
   npm install
   ```

4. Build the React application:

   ```
   npm run build
   ```

5. Run the test script:

   ```
   python3 -m yol_examples.script
   ```

6. Open the trace display in your browser:

   ```
   http://localhost:8235
   ```

### How the Yol Application Works

The Yol application is structured to trace Python function calls and display the trace information via a web interface. The tracing information includes function names, arguments, return values, the source code of the functions, and the time taken for their execution.

#### Directory Structure:

At the root level, we have the `yol_app` directory, which contains the core logic and components of the Yol application. Inside the `yol_app`, there are mainly two components:

- `trace_display`: A React app responsible for the user interface.
- `server.py`: A FastAPI server that serves the React application and provides an endpoint to fetch trace data.

#### Core Components:

1. **server.py**:

   This module serves as the web server for the application using FastAPI.

   - It sets up static file serving for the built React app.
   - It provides an endpoint `/trace` to fetch the tracing output.
   - The root endpoint `/` serves the main `index.html` of the React app.

2. **trace_logic.py**:

   This is the core module that provides the functionality to trace function calls.

   - `TraceManager`: A class that manages the tracing state, including the depth of function calls and collected trace outputs. It provides utility methods to handle the tracing process.
   - `YolFunctionCall`: A decorator that wraps around a function to trace its call. When a decorated function is called, this decorator logs the function's name, arguments, return value, execution time, and its source code.
   - `YolStart`: Another decorator that enables tracing and starts the FastAPI server once the decorated function has been executed.

#### Application Flow:

1. Users need to decorate the functions they want to trace with the `@YolFunctionCall` decorator.
2. The primary function to be tracked (like a main function) should be decorated with the `@YolStart` decorator.
3. When the main function (decorated with `@YolStart`) is executed:
   - Tracing is enabled.
   - The function's calls are traced, and output is collected.
   - After the function execution, the FastAPI server is started, allowing users to access the React frontend and see the trace output.
4. On accessing the root URL in a web browser, the built React app is served.
5. The React app can make calls to the `/trace` endpoint to fetch and display the tracing data.

### Local Development

1. **Frontend Development (React App inside `trace_display`)**:

   If you make any changes in the frontend code:

   - Navigate to the `trace_display` directory:

     ```bash
     cd yol-recorder/yol_app/trace_display
     ```

   - Install the required frontend dependencies (only required initially or when adding new dependencies):

     ```bash
     npm install
     ```

   - Make your code changes, and then build the frontend:

     ```bash
     npm run build
     ```

   - After building, navigate back to the root directory:

     ```bash
     cd ../../
     ```

   - Run your test script to reflect the frontend changes:

     ```bash
     python3 -m yol_examples.script
     ```

   - You can view your changes by accessing the React app at:

     ```bash
     http://localhost:8235
     ```

2. **Backend Development (`server.py` and `trace_logic.py`)**:

   If you make any changes in `server.py` or `trace_logic.py`:

   - Ensure you're at the root directory:

     ```bash
     cd yol-recorder
     ```

   - Simply run your test script:

     ```bash
     python3 -m yol_examples.script
     ```

   - This will reflect backend changes and serve the frontend React app. You can access the app at:

     ```bash
     http://localhost:8235
     ```

### Using Yol

1. **Decorate your functions**:
   To trace any function, you need to apply the `@YolFunctionCall` decorator above the function definition. This allows Yol to capture and record function call information.

   ```python
   @YolFunctionCall
   def call_vector_db(query):
       ...
   ```

2. **Initiate tracing**:
   The primary function that acts as the entry point to your program, such as `main()`, should be decorated with the `@YolStart` decorator. This decorator not only starts tracing but also runs the FastAPI server after the function's execution, allowing you to view the trace results in the React frontend.

   Optionally, you can specify a port for the server by providing the `port` parameter to the `@YolStart` decorator.

   ```python
   @YolStart
   def main():
       ...
   ```

   Or, with a specified port:

   ```python
   @YolStart(port=8990)
   def main():
       ...
   ```

3. **Run and View Traces**:
   Once you've decorated your functions, simply execute your script. After the script runs, the Yol server will start, and you can view the trace results by accessing:

   ```bash
   http://localhost:8235
   ```

   If you've specified a different port using `@YolStart(port=<your_port>)`, replace `8235` with your specified port in the URL.

4. **Stopping the Trace Server**:
   Once you're done viewing the traces, you can stop the Yol server by pressing `Ctrl+C` in the terminal where the script was run.

### Example Script

Check out the example script provided: [script.py](https://github.com/Neural-Bridge/yol-recorder/blob/main/yol_examples/script.py)

To run the script (from parent folder):

```
python3 -m yol_examples.script
```
