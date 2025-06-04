import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

from assets.constants import *
from app import get_image_default, get_image_light_dark, get_display_mode, update_display_mode
from app.frames import ScoresFrame, StandingsFrame

class Sidebar(ctk.CTkFrame):
    """Side Bar of the application"""
     
    def __init__(self, parent, update_frame):
        super().__init__(parent, width=75)
        self.update_frame = update_frame
        self.active_button = None
        
        self.grid_propagate(False) #Prevent Resizing Based on child widgets
        self.grid_columnconfigure(0, weight=1) #Centers All widgets

        #Importing Images
        app_logo = get_image_default(LOGO)

        theme_icon = get_image_light_dark(THEME_ICON)
        
        scoreboard_icon = get_image_light_dark(SCOREBOARD_ICON) #Import Scoreboard Icon
        
        standings_icon = get_image_light_dark(STANDINGS_ICON) #Import Standings icon

        
        self.logo = ctk.CTkLabel(self, image=app_logo, text="") #create label 
        self.logo.grid(row=0, column=0, padx=5, pady=5)  #Place App logo At top of frame
        
        #create buttons with function sending image and rows and function
        self.scores_btn = self.create_button(scoreboard_icon, 1)
        self.standings_btn = self.create_button(standings_icon, 2)
        
        self.scores_btn.configure(command=lambda: self.switch_frame(ScoresFrame, self.scores_btn))
        self.standings_btn.configure(command=lambda: self.switch_frame(StandingsFrame, self.standings_btn))

        self.switch_frame(ScoresFrame, self.scores_btn) #Sets Initial Frame to Scores Frame and disables Scores Btn

        self.grid_rowconfigure(3, weight=1)  # Spacer

        starting_theme = get_display_mode()
        self.theme = ctk.StringVar(self, value=starting_theme)
        self.theme_button = self.create_button(theme_icon, 4, command=self.change_theme)
        self.theme_button.configure(hover="false")
    
    def create_button(self, image, row, command=None):
        """Function for Creating Buttons On the sidebar"""
        button = ctk.CTkButton(self, 
                               text="", 
                               image=image, 
                               fg_color="transparent", 
                               anchor="center",
                               hover=False,
                               command= command if command is not None else None)
                               
        button.grid(row=row, column=0, padx=PADX, pady=PADY)

        return button

    def change_theme(self):
        """Function to change the theme"""
        theme = self.theme.get()

        if theme == "light":
            
            ctk.set_appearance_mode("dark")
            self.theme.set("dark")
            update_display_mode("dark")
        else:
            ctk.set_appearance_mode("light")
            self.theme.set("light")
            update_display_mode("light")

    def switch_frame(self, frame_class, clicked_button):
        """Updates frame and buttons"""
        self.update_frame(frame_class)

        if self.active_button and self.active_button != clicked_button:
            self.active_button.configure(state="normal", fg_color="transparent")

        clicked_button.configure(state="disabled", fg_color="#3D75A0")

        self.active_button = clicked_button