import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
from assets.constants import *

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

        #Side Bar Placement
        side_bar = Sidebar(self)
        side_bar.grid(row=0, column=0, pady=5, padx=5, sticky="nsw") #Placed on Left of Screen, sticks to Top, Bottom & Left
        
        #Main_area Placement
        main_area = MainFrame(self)
        main_area.grid(row=0, column=1, pady=5, padx=3, sticky="nsew") # Placed Right of Sidebar, Fills Remaining Area
           

class MainFrame(ctk.CTkFrame):
    """Main part of the window"""
    def __init__(self, parent):
        super().__init__(parent)

        
class Sidebar(ctk.CTkFrame):
    """Side Bar of the application"""
     
    def __init__(self, parent):
        super().__init__(parent, width=75)
        
        self.grid_propagate(False) #Prevent Resizing Based on child widgets
        self.grid_columnconfigure(0, weight=1) #Centers All widgets

        #Importing Images (May Move Soon to be Global, Also Have to update how the path is called)
        app_logo = ctk.CTkImage(light_image=Image.open(LOGO),
                                dark_image=Image.open(LOGO),
                                size=(50,50))
        
        scoreboard_icon = ctk.CTkImage(light_image=Image.open(SCOREBOARD_ICON + "light.png"),
                                dark_image=Image.open(SCOREBOARD_ICON + "dark.png"),
                                size=(50,50))
        
        calendar_icon = ctk.CTkImage(light_image=Image.open(CALENDAR_ICON + "light.png"),
                                dark_image=Image.open(CALENDAR_ICON + "dark.png"),
                                size=(50,50))
        
        standings_icon = ctk.CTkImage(light_image=Image.open(STANDINGS_ICON + "light.png"),
                                dark_image=Image.open(STANDINGS_ICON + "dark.png"),
                                size=(50,50))
        
        self.logo = ctk.CTkLabel(self, image=app_logo, text="")
        self.logo.grid(row=0, column=0, padx=5, pady=5)  #Place App logo At top of frame
        
        #create buttons with function sending image and rows
        self.scores_btn = self.create_button(scoreboard_icon, 1)
        self.standings_btn = self.create_button(standings_icon, 2)

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
        self.theme_label.grid(row=6, column=0, padx=5, pady=5)
    
    
    def create_button(self, image, row):
        button = ctk.CTkButton(self, text="", image=image, fg_color="transparent")
        button.grid(row=row, column=0, padx=5, pady=5)

    def change_theme(self):
        """Logic to change the theme"""
        theme = self.theme.get()

        if theme == 1:
            ctk.set_appearance_mode("dark")
            self.theme_label.configure(text="Darkmode\n(On)")
        else:
            ctk.set_appearance_mode("light")
            self.theme_label.configure(text="Darkmode\n(Off)")