
This code has been created by Brad Ellison for Lamave Research to classify images taken with the RUV camera in Sibaltan

To rebuild latest using pyinstaller, do the following:

1 - Enter a terminal (either "Terminal" for mac, "Powershell" for Windows, or use the terminal on an IDE like VSCode)
2 - Go to the location of this folder on your local environment.
3 - Make sure you have the latest code from GIT by typing "git pull", handle any errors that occur.
4 - Make sure you have all dependencies by running "pip install -r requirements.txt", handle any errors that occur.
5 - Build the program, you must build the windows file from a windows machine and the MacOS file from a Mac.
    for windows, run: "python -m PyInstaller --onefile -n lamave_image_classification main.py"
    for mac, run: "pyinstaller --onefile -n lamave_image_classification main.py"
6 - If that ran correctly, the "dist" folder should contain a new script called main. Double click to run.


Other notes (do not run unless needed):
If you need to update requirements file: pip list --format=freeze > requirements.txt
