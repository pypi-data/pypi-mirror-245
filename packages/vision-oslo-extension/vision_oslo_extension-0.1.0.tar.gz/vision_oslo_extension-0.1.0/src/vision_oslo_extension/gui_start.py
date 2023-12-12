
# Third Party

import tkinter as tk
from tkinter import font as tkfont
#from tkinter import messagebox
#from PIL import Image
#import numpy as np 
#from subprocess import check_output 
import pandas as pd

# Loading subfunctions
# try:
#     from main_page_frame import PageOne, PageTwo, PageThree, PageFour
#     from extraction_frame import F01, F02, F03, F04, F05, F06, F07, F08, F09, F10, F11, F12, F13, F14
#     from processing_frame import P01, P02, P03, P04, P05, P06, P07, P08
#     from check_frame import C01, C02, C03
#     from shared_contents import SharedVariables
# except ModuleNotFoundError:
#     from vision_oslo_extension.main_page_frame import PageOne, PageTwo, PageThree, PageFour
#     from vision_oslo_extension.extraction_frame import F01, F02, F03, F04, F05, F06, F07, F08, F09, F10, F11, F12, F13, F14
#     from vision_oslo_extension.processing_frame import P01, P02, P03, P04, P05, P06, P07, P08
#     from vision_oslo_extension.check_frame import C01, C02, C03
#     from vision_oslo_extension.shared_contents import SharedVariables


# from main_page_frame import PageOne, PageTwo, PageThree, PageFour
# from extraction_frame import F01, F02, F03, F04, F05, F06, F07, F08, F09, F10, F11, F12, F13, F14
# from processing_frame import P01, P02, P03, P04, P05, P06, P07, P08
# from check_frame import C01, C02, C03
# from shared_contents import SharedVariables

from vision_oslo_extension.main_page_frame import PageOne, PageTwo, PageThree, PageFour
from vision_oslo_extension.extraction_frame import F01, F02, F03, F04, F05, F06, F07, F08, F09, F10, F11, F12, F13, F14
from vision_oslo_extension.processing_frame import P01, P02, P03, P04, P05, P06, P07, P08
from vision_oslo_extension.check_frame import C01, C02, C03
from vision_oslo_extension.shared_contents import SharedVariables

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.sub_title_font = tkfont.Font(family='Helvetica', size=12, weight="bold")
        self.big_text_font = tkfont.Font(family='Helvetica', size=10, weight="bold")
        self.text_font = tkfont.Font(family='Helvetica', size=10)
        # root.geometry('300x200')
        self.title('Vision-Oslo Extension')

        # define the top bar menu  'variible called menu
        menu = tk.Menu(self)
        self.config(menu = menu)
        # sub-menu 1 = filemenu
        filemenu = tk.Menu(menu)
        menu.add_cascade(label='File', menu = filemenu)
        filemenu.add_command(label= 'New')
        filemenu.add_command(label= 'Open')
        filemenu.add_separator()
        filemenu.add_command(label= 'Exit', command = self.quit)
        # sub-menu 2 = helpmenu
        helpmenu = tk.Menu(menu)
        menu.add_cascade(label='Help', menu = helpmenu)
        helpmenu.add_command(label='About')

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, \
                  F01, F02, F03, F04, F05, F06, F07, F08, F09, F10, F11, F12, F13, F14, \
                    P01, P02, P03, P04, P05, P06, P07, P08, \
                        C01, C02, C03):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame): # define another object of first page

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.headframe = self.create_frame(fill=tk.BOTH)
        self.nameframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 6))
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(4, 1))
        self.infoframe = self.create_frame(fill=tk.BOTH)

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Welcome to VISION-OSLO Add-In',font = controller.title_font)
        head.pack()
        
        text1 = tk.Label(master=self.nameframe, text = 'Simulation Name',font = controller.text_font)
        text1.grid(row = 0, column = 0) # sticky n alight to top center part

        SharedVariables.sim_variable = tk.StringVar()
        entry1 = tk.Entry(master=self.nameframe,width = 40,textvariable = SharedVariables.sim_variable)
        entry1.grid(row = 0,column = 1)

        # explain1 = tk.Message(master=self.optionframe, text = 'Pre-Model Information Prepare: create VISION-OSLO ready information',aspect = 600, font = controller.text_font)
        # explain1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)
        explain1 = tk.Label(master=self.optionframe, text = 'Pre-Model Information Prepare: create VISION-OSLO ready information', font = controller.text_font)
        explain1.grid(row = 0, column = 0, sticky = "w", padx=5, pady=5)

        button1 = tk.Button(master=self.optionframe, text = 'Model Prepare', command=lambda: self.button_callback("PageOne"))
        button1.grid(row = 0, column = 1, sticky = "w", padx=5, pady=5)

        explain2 = tk.Label(master=self.optionframe, text = 'Model Check Report: check model report. A working VISION-OSLO model is required', font=controller.text_font)
        explain2.grid(row = 1, column = 0, sticky = "w", padx=5, pady=5)

        #button2 = tk.Button(master=optionframe, text = 'Model Check', command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(master=self.optionframe, text = 'Model Check', command=lambda: self.button_callback("PageTwo"))
        button2.grid(row = 1, column = 1, sticky = "w", padx=5, pady=5)

        explain3 = tk.Label(master=self.optionframe, text = 'Default OSLO Extraction: A VISION-OSLO simulation result (oof) file is required.',font = controller.text_font)
        explain3.grid(row = 2, column = 0, sticky = "w", padx=5, pady=5)  

        button3 = tk.Button(master=self.optionframe, text = 'Result Extraction', command=lambda: self.button_callback("PageThree"))
        button3.grid(row = 2, column = 1, sticky = "w", padx=5, pady=5)

        explain4 = tk.Label(master=self.optionframe, text = 'Custmised Post-Processing: A VISION-OSLO simulation result (oof) file is required.',font = controller.text_font)
        explain4.grid(row = 3, column = 0, sticky = "w", padx=5, pady=5)  

        button4 = tk.Button(master=self.optionframe, text = 'Result Process', command=lambda: self.button_callback("PageFour"))
        button4.grid(row = 3, column = 1, sticky = "w", padx=5, pady=5)

        diclaimer = tk.Label(master=self.infoframe, text = 'Version 1.0  CopyRight @ 2023')
        diclaimer.pack()
      
        # label = tk.Label(self, text="This is the start page")
        # label.pack(side="top", fill="x", pady=10)

        # button1 = tk.Button(self, text="Go to Page One",
        #                     command=lambda: controller.show_frame("PageOne"))
        # button2 = tk.Button(self, text="Go to Page Two",
        #                     command=lambda: controller.show_frame("PageTwo"))
        # button1.pack()
        # button2.pack()
    
    def create_frame(self, fill=None, row_weights=None, column_weights=None):
        frame = tk.Frame(self)
        if fill:
            frame.pack(fill=fill)
        if row_weights:
            for i, weight in enumerate(row_weights):
                frame.rowconfigure(i, weight=weight)
        if column_weights:
            for i, weight in enumerate(column_weights):
                frame.columnconfigure(i, weight=weight)
        return frame

    def get_entry_value(self):
        user_input = SharedVariables.sim_variable.get()
        print("User Input: ", user_input )
        #return user_input

    def button_callback(self,target_page):
        self.get_entry_value()
        self.controller.show_frame(target_page)