import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

from assets.constants import *
from app.widgets import Sidebar
from app.frames import *


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
        self.main_area = None
        self.frames = {ScoresFrame : ScoresFrame(self), 
                       StandingsFrame : StandingsFrame(self)} #Pre Load Frames
        
        
        self.columnconfigure(0, weight=0) #Side Bar (Static Size)
        self.columnconfigure(1, weight=1) #Main Area (Stretches Frame to fill screen horizontally)
        self.rowconfigure(0, weight=1) #Strech Frames to fill screen vertically

        #Side Bar Placement With access to Show Frame Function
        self.side_bar = Sidebar(self, self.update_frame)
        self.side_bar.grid(row=0, column=0, pady=PADY, padx=PADX, sticky="nsw") #Placed on Left of Screen, sticks to Top, Bottom & Left
        


    def update_frame(self, frame_class):
        """Replace the current frame in main_area with a new one."""
        # Hide current frame

        if hasattr(self, 'main_area') and self.main_area is not None:
            if hasattr(self.main_area, "stop_auto_refresh"):
                self.main_area.stop_auto_refresh()
            self.main_area.grid_forget()

        self.main_area = self.frames[frame_class]
        self.main_area.grid(row=0, column=1, pady=PADY, padx=3, sticky="nsew")

        if hasattr(self.main_area, "scheduled_refresh"):
                self.main_area.scheduled_refresh()