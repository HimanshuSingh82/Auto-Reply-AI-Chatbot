import tkinter as tk
from utils import *
from functools import partial
import os
from threading import Thread,Event
from bot import autoReply
import keyboard

class AutoReplyBot:
    def __init__(self, master):
        self.master = master
        self.master.title("Auto Reply Bot")
        self.master.geometry("800x600")
        self.stop_exec = Event()

        # root.grid_columnconfigure(3, minsize=60) 
        
        # User Input Section
        tk.Label(master, text="Name:").grid(row=0,column=0)
        self.name_entry = tk.Entry(master,width=40)
        if (os.path.exists(".name.config")):
            value = read_name()
            self.name_entry.insert(0,value)
        self.name_entry.grid(row=0,column=1)

        self.save_button1 = tk.Button(master, text="Save Name", command=self.save_name,width=15)
        self.save_button1.grid(row=0,column=4)

        tk.Label(master, text="Description:").grid(row=1,column=0)
        self.description_entry = tk.Text(master,height=5,width=32)
        if (os.path.exists(".description.config")):
            value = read_description()
            self.description_entry.insert("1.0",value)
        self.description_entry.grid(row=1,column=1)

        self.save_button2 = tk.Button(master, text="Save Description", command=self.save_desc,width=15)
        self.save_button2.grid(row=1,column=4)
        
        # Coordinate Input Section
        self.coordinates = {}
        self.capture_buttons ={}
        labels = ["Whatsapp Icon", "Chat Window Start", "Chat Window End", "Arrow Down Icon", "Search Box Icon","Top Chat"]
        self.paths = {"Whatsapp Icon":".whatsapp.config", "Chat Window Start":".window_start.config","Chat Window End":".window_end.config", "Arrow Down Icon":".arrow.config", "Search Box Icon":".search_box.config","Top Chat":".top_chat.config"}
        
        i = 2
        for label in labels:
            tk.Label(master, text=label).grid(row=i,column=0)
            self.coordinates[label] = tk.Entry(master,width=40)
            if (os.path.exists(self.paths[label])):
                value = read_coords(self.paths[label])
                self.coordinates[label].insert(0,value)
            self.coordinates[label].grid(row=i,column=1)
            tk.Label(master,text="Press C to stop capture").grid(row=i,column=3)
            self.capture_buttons[label] = tk.Button(master, text="Start Capture", command=partial(self.capture_coord,self.paths[label]),width=15)
            self.capture_buttons[label].grid(row=i,column=4)
            i+=1

        # OpenAI and Gemini Key Section
        tk.Label(master, text="OpenAI Key:").grid(row=8,column=0)
        self.openai_key_entry = tk.Entry(master,width=40)
        if (os.path.exists(".open_ai.config")):
            value = read_key(0)
            self.openai_key_entry.insert(0,value)
        self.openai_key_entry.grid(row=8,column=1)
        self.save_openai_key = tk.Button(master, text="Save Key", command=partial(self.add_key,0),width=15)
        self.save_openai_key.grid(row=8,column=4)

        tk.Label(master, text="Gemini Key:").grid(row=9,column=0)
        self.gemini_key_entry = tk.Entry(master,width=40)
        if (os.path.exists(".gen_ai.config")):
            value = read_key(1)
            self.gemini_key_entry.insert(0,value)
        self.gemini_key_entry.grid(row=9,column=1)
        self.save_gemini_key = tk.Button(master, text="Save Key", command=partial(self.add_key,1),width=15)
        self.save_gemini_key.grid(row=9,column=4)


        tk.Label(master,text="If you have configured everything you can go ahead with starting the bot.").grid(row=10,column=0,columnspan=4)

        self.start_bot = tk.Button(master, text="START BOT", command=self.start_bot,width=15)
        self.start_bot.grid(row=11,column=1,columnspan=2)
        # self.stop_bot = tk.Button(master, text="STOP BOT", command=self.stop_bot,width=15)
        # self.stop_bot.grid(row=11,column=3)
        tk.Label(master,text="Press ctrl to Stop").grid(row=12,column=1,columnspan=2)


    def save_name(self):
        value = self.name_entry.get()
        write_name(value)

    def save_desc(self):
        value = self.description_entry.get("1.0","end-1c")
        write_description(value)

    def capture_coord(self,path):
        key_listener(path)
        ft = open(path)
        value = ft.readline()
        ft.close()
        label = [k for k, v in self.paths.items() if v == path][0]
        self.coordinates[label].delete(0,"end")
        self.coordinates[label].insert(0,value)
    

    def add_key(self,option):
        if(option==0):
            value = self.openai_key_entry.get()
            write_key(option,value)
        else:
            value = self.gemini_key_entry.get()
            write_key(option,value)

    def start_bot(self):
        # open_ai_key,genai_key,whatsapp_icon,arrowDown_icon,chat_window_start,chat_window_end,name,description,textbox
        # "Chat Window Start", "Chat Window End", "Arrow Down Icon", "Search Box Icon"
        open_ai_key = read_key(0)
        gen_ai_key = read_key(1)

        whatsapp_icon_coords = read_coords(self.paths["Whatsapp Icon"]).split(",")
        whatsapp_icon = {"x":int(whatsapp_icon_coords[0]),"y":int(whatsapp_icon_coords[1])}
        arrowDown_icon_coords = read_coords(self.paths["Arrow Down Icon"]).split(",")
        arrowDown_icon = {"x":int(arrowDown_icon_coords[0]),"y":int(arrowDown_icon_coords[1])}
        chat_window_start_coords = read_coords(self.paths["Chat Window Start"]).split(",")
        chat_window_start = {"x":int(chat_window_start_coords[0]),"y":int(chat_window_start_coords[1])}
        chat_window_end_coords = read_coords(self.paths["Chat Window End"]).split(",")
        chat_window_end = {"x":int(chat_window_end_coords[0]),"y":int(chat_window_end_coords[1])}
        text_box_coords = read_coords(self.paths["Search Box Icon"]).split(",")
        text_box = {"x":int(text_box_coords[0]),"y":int(text_box_coords[1])}
        top_chat_coords = read_coords(self.paths["Top Chat"]).split(",")
        top_chat  = {"x":int(top_chat_coords[0]),"y":int(top_chat_coords[1])}

        description = read_description()
        name = read_name()
        self.stop_exec.clear()
        Thread(target=autoReply,args=(open_ai_key,gen_ai_key,whatsapp_icon,arrowDown_icon,chat_window_start,chat_window_end,name,description,text_box,top_chat,self.stop_exec),daemon=True).start()

        keyboard.add_hotkey('ctrl',self.stop_bot)


    def stop_bot(self):
        self.stop_exec.set()
        return False
        

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoReplyBot(root)
    root.mainloop()
