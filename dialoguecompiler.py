import os
import sys
def compiler(text):
    currdir = sys.path[0]
    os.chdir(currdir+"/dialogue/")
    with open(f"{text}.txt", 'r') as dialogue:
        os.chdir(currdir)
        return dialogue.read()
