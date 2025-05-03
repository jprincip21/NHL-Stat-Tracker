import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
from assets.constants import *

PADX = 5
PADY = 5


class Application(ctk.CTk):
    """GUI Logic for application"""
    def __init__(self):  
        super().__init__()

        self.title("Basic Setup")
        self.geometry("900x600") 
        self.iconbitmap(LOGO_ICON)
        self.resizable(0,0) #Disable Maximizing Code
        ctk.set_appearance_mode("light")
        #self.state('zoomed') #Start Maximized
        
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

        self.main_area = frame_class(self)
        self.main_area.grid(row=0, column=1, pady=PADY, padx=3, sticky="nsew") # Placed Right of Sidebar, Fills Remaining Area
        
class ScoresFrame(ctk.CTkFrame):
    """Create Frame for displaying scores"""
    def __init__(self, parent):
        super().__init__(parent)
        
        #Layout Config
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0) #Heading
        self.rowconfigure(1, weight=0, minsize=5) #seperator

        #Heading label
        heading = ctk.CTkLabel(self, text="SCORES", font=("IMPACT", 50))
        heading.grid(row=0, column=0, padx=15, pady=PADY, sticky="nw" )

        #Seperator Line
        separator = ctk.CTkFrame(self, height=5)
        separator.grid(row=1, column=0, padx=PADX, pady=PADY, sticky="ew")
        separator.grid_propagate(False) #Prevents Shrinking

class StandingsFrame(ctk.CTkFrame):
    """Create Frame for displaying standings"""
    def __init__(self, parent):
        super().__init__(parent)
        
        #Layout Config
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0) #Heading
        self.rowconfigure(1, weight=0, minsize=5) #seperator

        #Heading label
        heading = ctk.CTkLabel(self, text="STANDINGS", font=("IMPACT", 50))
        heading.grid(row=0, column=0, padx=15, pady=PADY, sticky="nw" )

        #Seperator Line
        seperator = ctk.CTkFrame(self, height=5)
        seperator.grid(row=1, column=0, padx=PADX, pady=PADY, sticky="ew")
        seperator.grid_propagate(False) #Prevents Shrinking

        
class Sidebar(ctk.CTkFrame):
    """Side Bar of the application"""
     
    def __init__(self, parent, update_frame):
        super().__init__(parent, width=75)
        self.update_frame = update_frame
        
        self.grid_propagate(False) #Prevent Resizing Based on child widgets
        self.grid_columnconfigure(0, weight=1) #Centers All widgets

        #Importing Images (May Move Soon to be Global, Also Have to update how the path is called)
        app_logo = ctk.CTkImage(light_image=Image.open(LOGO),
                                dark_image=Image.open(LOGO),
                                size=(50,50))
        
        scoreboard_icon = self.get_image(SCOREBOARD_ICON)
        
        calendar_icon = self.get_image(CALENDAR_ICON)
        
        standings_icon = self.get_image(STANDINGS_ICON)
        
        self.logo = ctk.CTkLabel(self, image=app_logo, text="")
        self.logo.grid(row=0, column=0, padx=5, pady=5)  #Place App logo At top of frame
        
        #create buttons with function sending image and rows
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
        button = ctk.CTkButton(self, text="", image=image, fg_color="transparent", command=function)
        button.grid(row=row, column=0, padx=PADX, pady=PADY)

        return button

    def change_theme(self):
        """Logic to change the theme"""
        theme = self.theme.get()

        if theme == 1:
            ctk.set_appearance_mode("dark")
            self.theme_label.configure(text="Darkmode\n(On)")
        else:
            ctk.set_appearance_mode("light")
            self.theme_label.configure(text="Darkmode\n(Off)")

    def get_image(self, base_path):
        return ctk.CTkImage(light_image=Image.open(base_path + "light.png"),
                        dark_image=Image.open(base_path + "dark.png"),
                        size=(50, 50))