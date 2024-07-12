# AWS CodeWhisperer Installation

## Steps to Install AWS CodeWhisperer

1. **Open Visual Studio Code:**
   - Open Visual Studio Code by clicking its icon on your desktop or searching for it in your Start menu.

2. **Open Extensions View:**
   - Click on the Extensions view icon on the Sidebar.

3. **Search for AWS CodeWhisperer:**
   - In the Extensions view, search for "AWS CodeWhisperer" in the search bar at the top.

4. **Install the AWS CodeWhisperer Extension:**
   - Click on the "Install" button next to the AWS CodeWhisperer extension in the search results.

5. **Verify Installation:**
   - Once the installation is complete, you should see the AWS CodeWhisperer extension listed in your installed extensions.

6. **Authenticate with AWS:**
   - Click on the AWS CodeWhisperer extension icon in the sidebar.
   - Select the Amazon Q + CodeWhisperer authentication panel.
     - It will direct you to the browser with the authentication code.
   - Enter your email, name, and password.
     - You will receive a successful authentication message.


# Google AI Studio - Get API Key Guide

## Steps to Get the API Key

1. **Navigate to Google AI Studio Website:**
   - Visit the website of Google AI Studio by navigating to [Google AI Studio](https://studio.google.com/).

2. **Sign in or Create an Account:**
   - Sign in to your existing Google account or create a new account if you don't have one.

3. **Create a New Project (if required):**
   - If Google AI Studio requires you to create a project, navigate to the projects section and create a new project.

4. **Navigate to API Key Management (or Credentials) Section:**
   - Find the section in the dashboard related to API key management or credentials.

5. **Generate a New API Key:**
   - Click on the "Generate API Key" or similar button to create a new API key.

6. **Copy and Store the API Key Securely:**
   - Once the API key is generated, copy it and store it securely. Treat your API key like a password and do not expose it publicly.

7. **Go to Visual Studio Code and Create .env file:**
   - Open Visual Studio Code.
   - Open the terminal and create a `.env` file by running the command `touch .env`.

8. **Copy and Paste the API Key into .env file:**
   - In the `.env` file, assign the API key to the variable `GOOGLE_API_KEY`.
   - Example: `GOOGLE_API_KEY=your_api_key_here`.

9. **Run the Code:**
   - After setting up the `.env` file, you can now run your code that utilizes the Google API with the API key.
