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