# Connecting to Github with SSH
## Step 1: Generating SSH Key 
1. Open Terminal/Command Prompt: If you're on macOS or Linux, you can use Terminal.
2. Generate SSH Key: Type the following command:
```
  ssh-keygen -t ed25519 -C "your_email@example.com"
  ```
- Replace `your_email@example.com` with your GitHub email.
- Press Enter to accept the default file location and leave the passphrase empty if you don't want to use one.
3. Start SSH Agent: Start the SSH agent to manage your SSH keys:
   ```
   eval "$(ssh-agent -s)"
   ```
4. Add SSH Key to Agent: Add your SSH key to the SSH agent:
   ```
   ssh-add ~/.ssh/id_ed25519
   ```
5. Copy SSH Key to Clipboard: Copy your SSH key to the clipboard:
   ```
   cat ~/.ssh/id_ed25519.pub
## Step 2: Adding SSH Key to GitHub
1. Open GitHub:
   - Go to GitHub and sign in to your account.
2. Access SSH and GPG Keys Settings:
   - Click on your profile icon in the top-right corner, then select Settings.
   - In the left sidebar, click on SSH and GPG keys.
3. Add New SSH Key:
   - Click on New SSH key.
   - In the "Title" field, add a descriptive label for the new key.
   - Paste your SSH key into the "Key" field.
     ```
     ssh -T git@github.com
     ```
   - Click Add SSH key.
## Step 3: Cloning a GitHub Repository
1. Copy Repository SSH URL:
   - Go to the repository you want to clone on GitHub.
   - Click on the green Code button.
   - Make sure SSH is selected and copy the provided URL.
2. Clone the Repository:
   - In your terminal, navigate to the directory where you want to clone the repository.
   - Type the following command, replacing `<repository_url>` with the URL you copied:
     ```
     git clone <repository_url>
     ```
## Step 4: Running Code in Visual Studio Code
1. Open VSCode:
   - Launch Visual Studio Code.
2. Open Cloned Repository:
   - Use the menu bar or command line to navigate to the directory where you cloned the repository.
   - Open the repository folder in VSCode.
3. Run Code:
   - Depending on the project type, you can run code directly from VSCode's integrated terminal or use the specific commands provided by the project's documentation.
