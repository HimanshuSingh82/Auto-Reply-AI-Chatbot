import pyautogui
from pynput import keyboard
from functools import partial,reduce

def read_key(option):
    if option == 1:
        fp = open(".gen_ai.config","r")
        genai_key = fp.readline()
        fp.close()
        return genai_key
    else:
        fp = open(".open_ai.config","r")
        open_ai_key = fp.readline()
        fp.close()
        return open_ai_key
def write_key(option,api_key):
    if option == 1:
        fp = open(".gen_ai.config","w")
        fp.write(api_key)
        fp.close()
    else:
        fp = open(".open_ai.config","w")
        fp.write(api_key)
        fp.close()


def get_postion(path,key):
    if key.char == 'c':
        ft = open(path,"w")
        coords = f"{pyautogui.position().x},{pyautogui.position().y}"
        ft.write(coords)
        ft.close()
        return False
    return True

def key_listener(path):
    with keyboard.Listener(on_release=partial(get_postion,path)) as listener:
        listener.join()

def read_description():
    ft = open(".description.config","r")
    lines = ft.readlines()
    ft.close()
    description = reduce(lambda x,y: x+y, lines)
    return description

def write_description(description):
    ft = open(".description.config","w")
    ft.write(description)
    ft.close()

def read_name():
    ft = open(".name.config","r")
    name = ft.readline()
    ft.close()
    return name

def write_name(name):
    ft = open(".name.config","w")
    ft.write(name)
    ft.close()


def read_coords(path):
    ft = open(path)
    value = ft.readline()
    ft.close()
    return value