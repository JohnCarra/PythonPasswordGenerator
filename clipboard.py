import os
import platform


def clear_clipboard():
    if platform.system() == "Windows":
        command = 'echo off | clip'
        os.system(command)
    elif platform.system() == "Darwin":
        command = 'echo -n "" | pbcopy'
        os.system(command)
    else:
        command = 'echo -n "" | xclip -selection clipboard'
        os.system(command)
