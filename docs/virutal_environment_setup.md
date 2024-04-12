# Setting up a Virtual Environment for Linux

## Option 1: Using `virtualenv` Package

1. **Install `virtualenv`** (if not already installed):
    ```bash
    python3.10 -m pip install virtualenv
    ```

2. **Create a Virtual Environment**:
    ```bash
    python3.10 -m virtualenv .venv
    ```

3. **Activate the Virtual Environment**:
    ```bash
    source .venv/bin/activate
    ```

4. **Deactivate the Virtual Environment** (after you're done):
    ```bash
    deactivate
    ```

## Option 2: Using Visual Studio Code (Python Select Interpreter)

1. **Open Visual Studio Code**:
   Launch Visual Studio Code by searching for it in your applications menu or by typing `code` in the terminal.

2. **Open Your Project**:
   Open the folder containing your Python project in Visual Studio Code by selecting "File" > "Open Folder" from the menu and navigating to your project directory.

3. **Open the Command Palette**:
   Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) to open the command palette.

4. **Select Interpreter**:
   Type "Python: Select Interpreter" in the command palette and select it.

5. **Choose Virtual Environment**:
   A list of available interpreters will be displayed. Look for the interpreter inside your virtual environment (`.venv`) and select it.

6. **Verify Activation**:
   After selecting the interpreter, Visual Studio Code will automatically activate the virtual environment. You can verify this by opening the integrated terminal (``Ctrl+``) and checking if the virtual environment name appears in the terminal prompt.

7. **Deactivate the Virtual Environment (Optional)**:
   To deactivate the virtual environment and return to the system-wide Python environment, you can use the `deactivate` command in the terminal.
