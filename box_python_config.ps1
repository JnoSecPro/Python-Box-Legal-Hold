#create variables for Python path.
Write-Host "Configuring environment variables." -BackgroundColor DarkGreen -ForegroundColor DarkYellow
$pythonPath = "C:\Python38"
$pythonScriptsPath = "C:\Python38\Scripts"
$pythonPaths = "$pythonPath;$pythonScriptsPath"

#add Python paths to the Path environment variable for current user.
[Environment]::SetEnvironmentVariable("Path", "$($env:Path);$pythonPaths", [System.EnvironmentVariableTarget]::User)

#create the Python virtual environment in the current user's Documents folder
Write-Host "Creating virtual environment directory." -BackgroundColor DarkGreen -ForegroundColor DarkYellow
python -m venv C:\Users\$env:USERNAME\Documents\BoxAPI\box_venv

#change directory to the box_venv folder that was created
cd C:\Users\$env:USERNAME\Documents\BoxAPI\box_venv

#activate the virtual environment
Write-Host "Installing boxsdk module for Python." -BackgroundColor DarkGreen -ForegroundColor DarkYellow
.\Scripts\Activate.ps1

#install the boxsdk module for Python in the box_venv folder
pip install boxsdk

#install the pyinstaller tool in order to compile the program
Write-Host "Installing PyInstaller to compile executables." -BackgroundColor DarkGreen -ForegroundColor DarkYellow
pip install pyinstaller

#deactivate the the virtual environment
deactivate

Write-Host "Environment configuration is complete." -BackgroundColor DarkGreen -ForegroundColor DarkYellow
Write-Host "Closing window." -BackgroundColor DarkGreen -ForegroundColor DarkYellow
Start-Sleep -Seconds 5