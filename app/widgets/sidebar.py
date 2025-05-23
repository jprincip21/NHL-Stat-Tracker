import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

from assets.constants import *
from app import get_image_default, get_image_light_dark
from app.frames import ScoresFrame, StandingsFrame

class Sidebar(ctk.CTkFrame):
    """Side Bar of the application"""
     
    def __init__(self, parent, update_frame):
        super().__init__(parent, width=75)
        self.update_frame = update_frame
        
        self.grid_propagate(False) #Prevent Resizing Based on child widgets
        self.grid_columnconfigure(0, weight=1) #Centers All widgets

        #Importing Images
        app_logo = get_image_default(LOGO)
        
        scoreboard_icon = get_image_light_dark(SCOREBOARD_ICON) #Import Scoreboard Icon
        
        standings_icon = get_image_light_dark(STANDINGS_ICON) #Import Standings icon
        
        self.logo = ctk.CTkLabel(self, image=app_logo, text="") #create label 
        self.logo.grid(row=0, column=0, padx=5, pady=5)  #Place App logo At top of frame
        
        #create buttons with function sending image and rows and function
        self.scores_btn = self.create_button(scoreboard_icon, 1, lambda: self.update_frame(ScoresFrame))
        self.standings_btn = self.create_button(standings_icon, 2, lambda: self.update_frame(StandingsFrame))

        self.grid_rowconfigure(3, weight=1)  # Spacer

        self.theme = ctk.IntVar(value=0)
        self.theme_switch = ctk.CTkSwitch(self, 
                                    text="", 
                                    variable=self.theme, 
                                    offvalue=0, 
                                    onvalue=1,
                                    command=self.change_theme,
                                    )
        self.theme_switch.grid(row=4, column=0, padx=18, columnspan=2)

        self.theme_label = ctk.CTkLabel(self, text="Darkmode\n(Off)")
        self.theme_label.grid(row=6, column=0, padx=PADX, pady=PADY)
    
    #TODO: Add command arguement, use command to update interface & Disable button based on user selection & Current menu
    def create_button(self, image, row, function=None):
        """Function for Creating Buttons On the sidebar"""
        button = ctk.CTkButton(self, text="", image=image, fg_color="transparent", command=function, anchor="center")
        button.grid(row=row, column=0, padx=PADX, pady=PADY)

        return button

    def change_theme(self):
        """Function to change the theme"""
        theme = self.theme.get()

        if theme == 1:
            ctk.set_appearance_mode("dark")
            self.theme_label.configure(text="Darkmode\n(On)")
        else:
            ctk.set_appearance_mode("light")
            self.theme_label.configure(text="Darkmode\n(Off)")