#Description
#This script will use pyInstaller and Inno Setup Compiler to create an installation file for the software.
#Both pyinstaller and Inno, are required in order to run this script. 
#output: an executable file for the program, and an installer.

#IMPORTANT BEFORE PACKING
# -Inno Setup 6 must be installed in your windows computer
# - you must patch seleniumbase's code. 
#By not doing this, there will be unexpected behavior if the program gets installed in a write-protected folder, as explained in this thread: https://github.com/seleniumbase/SeleniumBase/issues/2479

#file: seleniumbase/fixtures/constants.py
#replace this code:
'''
class Files:
    # This is a special downloads folder for files downloaded by tests.
    # The "downloaded_files" folder is DELETED when starting new tests.
    # Add "--archive-downloads" to save a copy in "archived_files".
    # (These folder names should NOT be changed.)
    DOWNLOADS_FOLDER = "downloaded_files"
    ARCHIVED_DOWNLOADS_FOLDER = "archived_files"

'''
#with this code:
'''
import os
app_data_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'InstaGrow')
if not os.path.exists(app_data_dir):
    os.makedirs(app_data_dir)

class Files:
    # This is a special downloads folder for files downloaded by tests.
    # The "downloaded_files" folder is DELETED when starting new tests.
    # Add "--archive-downloads" to save a copy in "archived_files".
    # (These folder names should NOT be changed.)
    DOWNLOADS_FOLDER = app_data_dir
    ARCHIVED_DOWNLOADS_FOLDER = "archived_files"
'''

import os
import shutil
import subprocess
import config

#general
appName = config.AppName
folder_resources = 'resources'


#inno setup
icon_name='InstaGrow.ico'
setup_compiler_path = r"C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe" 
script_path = f"{folder_resources}\\setup_script.iss"  
output_dir = 'Windows_Setup_Output'

#clean after packing
foldersToDelete = ['build','__pycache__']
filesToDelete = [f'{appName}.spec']

def pyInstaller():
    os.system('cls')
    print(f'{appName} windows package setup\n')
    print('This setup will install the python requirements, pack the code and create an installation file.\n')
    print(f'WARNING: you should have Inno Setup Compiler installed.\nPath: {setup_compiler_path}\nIf the path doesn\'t match, change it in this script.')
    print(f'Script location: {script_path}')
    input('Continue?')

    if not os.path.exists(setup_compiler_path):
        print(f'The following path was not found, please check your installation or change the path in this same script: {setup_compiler_path}')
        input('exit')
        exit()

    print('Installing requirements...')
    os.system('pip install -r requirements.txt')
    print('Exporting .exe file')
    os.system(f"pyinstaller --noconfirm --onefile --console --clean --name {appName} --distpath {folder_resources} \"main.py\"")

    try:
        for folder in foldersToDelete:
            shutil.rmtree(folder)
        for file in filesToDelete:
            os.remove(file)
    except:
        pass

    print('\nFinished.')
    print('Output file located in dist/ folder')
    print('Creating setup file')

def innoSetup():
    os.system(f"icoextract {folder_resources}\\{config.AppName}.exe {folder_resources}\\{icon_name}")

    script=f'''
[Setup]
AppName={config.AppName}
AppVersion={config.AppVersion}
DefaultDirName={{pf}}\{config.AppName}
DefaultGroupName={config.AppName}
OutputDir={output_dir}
OutputBaseFilename={config.AppName} Installer
Compression=lzma
SolidCompression=yes
UninstallDisplayIcon={{app}}\\{icon_name}
UninstallDisplayName={config.AppName} ({config.AppVersion})

[Files]
Source: "{config.AppName}.exe"; DestDir: "{{app}}\{config.AppName}"
Source: "{icon_name}"; DestDir: "{{app}}"

[Icons]
Name: "{{group}}\\{config.AppName}"; Filename: "{{app}}\\{config.AppName}\\{config.AppName}.exe"
Name: "{{commondesktop}}\\{config.AppName}"; Filename: "{{app}}\\{config.AppName}\\{config.AppName}.exe"
'''
    # Write the script content to a file
    try:
        with open(script_path, "w") as file:
            file.write(script)
            file.close()
    except:
        print(f'Error writing the script path. Please execute this script from its root foler\nPath: {script_path}')
        input('exit')
        exit()

    subprocess.run([setup_compiler_path, script_path])

    print(f'Done. setup located in {folder_resources}/{output_dir}')
    input('Press a key to exit')

pyInstaller()
innoSetup()