# WSL2 Installation Guide 

## 1. Enabling and Installing WSL2 

1. Open PowerShell or Windows Command Prompt in administrator mode by right-clicking and selecting “Run as administrator”. 
2. Enter the following command to enable the optional WSL and Virtual Machine Platform components:  
   ``` 
   wsl --install 
   ``` 
3. Wait for the command to complete. It may take several minutes depending on your internet speed and system configuration. You may see some messages asking you to restart your machine or press Y to confirm. 
4. If prompted, restart your machine to apply the changes. 
5. After restarting, open PowerShell or Windows Command Prompt again in administrator mode and enter the following command to set WSL2 as the default version:  
   ``` 
   wsl --set-default-version 2 
   ``` 
6. Open PowerShell or Windows Command Prompt again in administrator mode and enter the following command to verify that WSL2 is set as the default version:  
   ``` 
   wsl --list --verbose 
   ``` 
7. You should see a table showing your installed Linux distributions (if any) and their versions. The version column should say “2” for all distributions. 

## 2. Downloading and Installing Ubuntu 

1. Open the Microsoft Store app by clicking its icon on your taskbar or searching for it in your Start menu. 
2. In the search box at the top right corner of the app window, type “Ubuntu” and press Enter. 
3. You should see a list of Ubuntu versions available for download. Choose your preferred version by clicking its name or icon. For this guide, we will use Ubuntu 22.04 LTS. 
4. On the Ubuntu page, click the “Get” button to start the download and installation process. You may need to sign in with your Microsoft account if you haven’t done so already. 
5. Wait for the download and installation to complete. It may take several minutes depending on your internet speed and system configuration. You can monitor the progress on the Downloads and updates page of the Microsoft Store app. 
6. Once the installation is finished, you can launch Ubuntu by clicking the “Launch” button on the Ubuntu page or by searching for it in your Start menu. 

## 3. Configuring Ubuntu and Installing Python 

1. When you launch Ubuntu for the first time, you will see a terminal window with a message asking you to enter a new UNIX username. Choose a username that you like, and press Enter. The username should be lowercase and should not contain any spaces or special characters. 
2. Next, you will be asked to enter a new UNIX password for your user account. Choose a password that is strong and secure, press Enter. You will need to retype the password to confirm it. The password will not be shown on the screen as you type it. 
3. After setting up your user account, you will see a message saying, “Installation successful” and a prompt with your username and hostname. This means that you are now logged in to your Ubuntu terminal. 
4. To update your system packages, enter the following command:  
   ``` 
   sudo apt update && sudo apt upgrade 
   ``` 
5. You will be asked to enter your password again. Enter the same password that you created earlier, and press Enter. The password will not be shown on the screen as you type it. 
6. Wait for the command to complete. It may take several minutes depending on your internet speed and system configuration. You may see some messages asking you to press Y or N to confirm or cancel some actions. 
7. To install Python, enter the following command:  
   ``` 
   sudo apt install python3 
   ``` 
8. Wait for the command to complete. It may take a few minutes depending on your internet speed and system configuration. You may see some messages asking you to press Y or N to confirm or cancel some actions. 
9. To verify that Python is installed correctly, enter the following command:  
   ``` 
   python3 --version 
   ``` 
   You should see a message showing the version of Python that you have installed. For example: Python 3.8.10 

## Accessing BIOS Setup 
1. **Restart your computer:** 
   - While the computer is booting up, look for a message that indicates which key to press to enter the BIOS or UEFI settings. This key is often displayed briefly on the screen, typically keys like F2, F10, ESC, or DEL. 
2. **Locate Virtualization Setting:** 
   - Once you're in the BIOS/UEFI settings, navigate using the arrow keys. The exact layout and options may vary depending on your motherboard manufacturer. 
   - Look for a setting related to virtualization. It may be labeled as "Intel Virtualization Technology (Intel VT-x)" for Intel processors or "AMD Virtualization (AMD-V)" for AMD processors. This setting might be under different categories such as "Advanced," "CPU Configuration," or "Security." 
3. **Enable Virtualization:** 
   - Once you've located the virtualization setting, select it. 
   - Change the setting to "Enabled" or "Enable." 
   - Save your changes and exit the BIOS/UEFI settings. Usually, you can do this by pressing a key like F10, and then confirm the changes. 
4. **Restart Your Computer:** 
   - After saving the changes in BIOS/UEFI, your computer will restart. 

**Verify Virtualization Support:** 
```bash 
grep -E --color 'vmx|svm' /proc/cpuinfo 
``` 

## 4. Installing and Setting up VSCode with Python Extension 

1. Open your web browser and go to the official VSCode website. 
2. Click the “Download for Windows” button to download the VSCode installer for Windows. 
3. Run the downloaded file and follow the instructions to install VSCode on your machine. 
4. Once the installation is finished, launch VSCode by clicking its icon on your taskbar or searching for it in your Start menu. 
5. A new VSCode window will open with a green badge on the bottom left corner saying “WSL: Ubuntu-22.04”. This means that you are now connected to your Ubuntu terminal through WSL2. 
6. To open a folder or file in your Ubuntu terminal from VSCode, click the “Open Folder” button on the welcome page. 
