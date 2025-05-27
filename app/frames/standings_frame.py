import tkinter as tk
from tkinter import ttk
import customtkinter as ctk


from utilities import get_standings
from assets.constants import *

class StandingsFrame(ctk.CTkFrame):
    """Create Frame for displaying standings"""
    def __init__(self, parent):
        super().__init__(parent)
        self.active_button = None
        
        #Layout Config
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0) #Heading
        self.rowconfigure(1, weight=0, minsize=5) #seperator
        
        #Heading label
        heading = ctk.CTkLabel(self, text="STANDINGS", font=("IMPACT", 50)) #Create Label
        heading.grid(row=0, column=0, padx=15, pady=PADY, sticky="nw" ) #Place Label

        #Seperator Line
        separator = ctk.CTkFrame(self, height=5) #Create Separator
        separator.grid(row=1, column=0, padx=PADX, pady=PADY, sticky="ew") #Place Separator
        separator.grid_propagate(False) #Prevents Shrinking

        self.filters_frame = ctk.CTkFrame(self) #Frame for Standings Filter Buttons
        self.filters_frame.grid(row=2, column=0, padx=PADX, pady=PADY, sticky="ew") 
        

        self.filters_frame.grid_columnconfigure(0,weight=1) 
        self.filters_frame.grid_columnconfigure(1,weight=1)
        self.filters_frame.grid_columnconfigure(2,weight=1)
        self.filters_frame.grid_columnconfigure(3,weight=1)


        self.overall_btn = self.create_button("Overall", 0)
        self.conference_btn = self.create_button("Conference", 1)
        self.division_btn = self.create_button("Division", 2)
        self.wildcard_btn = self.create_button("Wild Card", 3)

        self.overall_btn.configure(command=lambda: self.change_filter(self.overall_btn))
        self.conference_btn.configure(command=lambda: self.change_filter(self.conference_btn))
        self.division_btn.configure(command=lambda: self.change_filter(self.division_btn))
        self.wildcard_btn.configure(command=lambda: self.change_filter(self.wildcard_btn))

        self.change_filter(self.overall_btn)
        get_standings()


    def create_button(self, text, col, disabled=False, command=None):
        button = ctk.CTkButton(self.filters_frame, 
                               text=text,  
                               fg_color="transparent", 
                               text_color=("black", "white"),
                               font=("IMPACT", 18),
                               anchor="center",
                               hover="false")
        button.grid(column=col, row=0, padx=PADX, pady=PADY)

        return button
    
    def change_filter(self, clicked_button):
        if self.active_button and self.active_button != clicked_button:
            self.active_button.configure(state="normal", fg_color="transparent", text_color=("black", "white"))

        clicked_button.configure(state="disabled", fg_color="#3D75A0")

        self.active_button = clicked_button