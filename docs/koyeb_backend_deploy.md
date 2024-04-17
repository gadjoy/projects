## Deploying Your Backend Application on koyeb

1. **Sign up:**
- Visit [Koyeb](https://www.koyeb.com/) and click the "Get Started - Free" button to create an account.
- You can sign up using either your email or by connecting your GitHub account.
2. **Create an account:**
- Follow the prompts to create your account, ensuring that you verify your email address if required.
3. **Create a new service:**
- Once you are logged in, click on the "Create Web Service" button under the "Create a New Service" section.
4. **Choose a deployment method:**
- On the "Deploy a New Project on Koyeb" page, click on "GitHub" to connect to your GitHub account.
- Click on "Install GitHub App" to navigate to the GitHub page.
5. **Import project:**
- Select "Only select repository" and choose the repository where your backend code is located.
- Click the "Install" button to install Koyeb in that repository.
6. **Configure service and deploy:**
- After the configuration and deploy page loads, verify that your repository and branch are correct in the "Source" column.
-If your code uses environment variables like "FLN_OAUTH_TOKEN" or "API_KEY":
- Add them in the "Environment Variables" column by clicking "Add variables."
- Enter the name of the variable and select its type. For secret variables, choose "Secret" 
  and add the value in the secret section.
- Click "Create New Secret" to enter the variable value, then click "Create."
- Repeat this process for additional variables.
- Adjust the port number in the "Exposed Ports" column if needed by clicking on it and entering the desired port number.
- Finally, click on the "Deploy" button to start the deployment process.
7. **Monitor the deployment:**
- Once the deploy page loads, monitor the progress on the Koyeb deploy page.
8. **Access your backend:**
- After the deployment is completed, Koyeb will provide you with the backend URL.
- You can access your backend through this URL.
