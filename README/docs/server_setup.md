# Server Setup on Linux

Setting up a server on Linux. Follow the steps below to get started:

1. **Install Python**:

   Ensure Python is installed on your Linux machine.

   ```bash
   'sudo apt update'
   'sudo apt install python3'

2. **Create a Server Script**:

    - Create a new file named `app.py`.
    - Write your server code in `app.py`. This could be a Flask application.

3. **Create a requirements.txt**:
    -This file lists all the Python packages required by your application. When you run
    
    ```bash
    'pip install -r requirement.txt'-it will install Flask and any other packages listed in the file.

4. **Run the Server**:

    - Open a terminal window.
    - Navigate to the directory containing `app.py`.
    - Execute the following command to run the server:

      ```bash
      'python3 app.py'
      ```


