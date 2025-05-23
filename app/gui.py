import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

from assets.constants import *
from app.frames import ScoresFrame
from app.widgets import Sidebar

#TODO: Add Today button to send user back to current date if a different one is selected, Disable Standings and Scores button when selected.
#TODO: Get Team Logos to Display

class Application(ctk.CTk):
    """GUI Logic for application"""
    def __init__(self):  
        super().__init__()

        self.title("NHL Stat Tracker")
        self.geometry("900x600") 
        self.iconbitmap(LOGO_ICON)
        self.resizable(0,0) #Disable Maximizing
        #self.state('zoomed') #Start Maximized
        ctk.set_appearance_mode("light")
        
        
        self.columnconfigure(0, weight=0) #Side Bar (Static Size)
        self.columnconfigure(1, weight=1) #Main Area (Stretches Frame to fill screen horizontally)
        self.rowconfigure(0, weight=1) #Strech Frames to fill screen vertically

        #Side Bar Placement With access to Show Frame Function
        side_bar = Sidebar(self, self.update_frame)
        side_bar.grid(row=0, column=0, pady=PADY, padx=PADX, sticky="nsw") #Placed on Left of Screen, sticks to Top, Bottom & Left
        
        #Main_area Placement for dynamic Content
        self.main_area = None
        self.update_frame(ScoresFrame)

    def update_frame(self, frame_class):
        """Replace the current frame in main_area with a new one."""
        if self.main_area is not None:
            self.main_area.destroy()

        self.main_area = frame_class(self) #If scores frame is not selected create a basic class 
        self.main_area.grid(row=0, column=1, pady=PADY, padx=3, sticky="nsew") # Placed Right of Sidebar, Fills Remaining Area

        
# class Sidebar(ctk.CTkFrame):
#     """Side Bar of the application"""
     
#     def __init__(self, parent, update_frame):
#         super().__init__(parent, width=75)
#         self.update_frame = update_frame
        
#         self.grid_propagate(False) #Prevent Resizing Based on child widgets
#         self.grid_columnconfigure(0, weight=1) #Centers All widgets

#         #Importing Images
#         app_logo = get_image_default(LOGO)
        
#         scoreboard_icon = get_image_light_dark(SCOREBOARD_ICON) #Import Scoreboard Icon
        
#         standings_icon = get_image_light_dark(STANDINGS_ICON) #Import Standings icon
        
#         self.logo = ctk.CTkLabel(self, image=app_logo, text="") #create label 
#         self.logo.grid(row=0, column=0, padx=5, pady=5)  #Place App logo At top of frame
        
#         #create buttons with function sending image and rows and function
#         self.scores_btn = self.create_button(scoreboard_icon, 1, lambda: self.update_frame(ScoresFrame))
#         self.standings_btn = self.create_button(standings_icon, 2, lambda: self.update_frame(StandingsFrame))

#         self.grid_rowconfigure(3, weight=1)  # Spacer

#         self.theme = ctk.IntVar(value=0)
#         self.theme_switch = ctk.CTkSwitch(self, 
#                                     text="", 
#                                     variable=self.theme, 
#                                     offvalue=0, 
#                                     onvalue=1,
#                                     command=self.change_theme,
#                                     )
#         self.theme_switch.grid(row=4, column=0, padx=18, columnspan=2)

#         self.theme_label = ctk.CTkLabel(self, text="Darkmode\n(Off)")
#         self.theme_label.grid(row=6, column=0, padx=PADX, pady=PADY)
    
#     #TODO: Add command arguement, use command to update interface & Disable button based on user selection & Current menu
#     def create_button(self, image, row, function=None):
#         """Function for Creating Buttons On the sidebar"""
#         button = ctk.CTkButton(self, text="", image=image, fg_color="transparent", command=function, anchor="center")
#         button.grid(row=row, column=0, padx=PADX, pady=PADY)

#         return button

#     def change_theme(self):
#         """Function to change the theme"""
#         theme = self.theme.get()

#         if theme == 1:
#             ctk.set_appearance_mode("dark")
#             self.theme_label.configure(text="Darkmode\n(On)")
#         else:
#             ctk.set_appearance_mode("light")
#             self.theme_label.configure(text="Darkmode\n(Off)")