import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

from datetime import datetime, date
from PIL import Image

import customtkinter as ctk
from assets.constants import *
from utilities.api_handler import get_games_by_date

#TODO: Import API_Handler, Use when code is initially run as well as when date is changed by sending the formatted date

class Application(ctk.CTk):
    """GUI Logic for application"""
    def __init__(self):  
        super().__init__()

        self.title("NHL Stat Tracker")
        self.geometry("900x600") 
        self.iconbitmap(LOGO_ICON)
        self.resizable(0,0) #Disable Maximizing Code
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

        if frame_class == ScoresFrame: # When Scores Frame is selected Send Games Data
            self.main_area = frame_class(self)
                 
        else:
            self.main_area = frame_class(self) #If scores frame is not selected create a basic class
            
        self.main_area.grid(row=0, column=1, pady=PADY, padx=3, sticky="nsew") # Placed Right of Sidebar, Fills Remaining Area
        
class ScoresFrame(ctk.CTkFrame):
    """Create Frame for displaying scores"""
    def __init__(self, parent):
        super().__init__(parent)

        self.calendar_visible = False #Set calendar Visibility to false
        self.calendar_widget = None 

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

        calendar_icon = get_image(CALENDAR_ICON)

        # Frame to Hold Date and Date Button
        date_frame = ctk.CTkFrame(self, corner_radius=5)
        date_frame.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        date_frame.grid_columnconfigure(0, weight=0)
        date_frame.grid_columnconfigure(1, weight=0)

        
        # Calendar button In date_frame
        open_calendar_button = ctk.CTkButton(date_frame, text="", image=calendar_icon, fg_color="transparent", command=self.toggle_calendar, width=30)
        open_calendar_button.grid(row=0, column=0, pady=0)

        #Initalize Date and Games Data
        self.selected_date = date.today()
        self.games_data = get_games_by_date(self.selected_date) #Sent Data from Api

        print(self.selected_date) # For Testing

        # Date label in date_frame
        self.date_label = ctk.CTkLabel(date_frame, text=self.selected_date, font=("IMPACT", 20))
        self.date_label.grid(row=0, column=1, padx=PADX, pady=0)

        self.games_frame = GamesDisplayFrame(self, self.games_data)
        self.games_frame.grid(row=3, column=0, padx=PADX, pady=PADY, sticky="nsew")    

    def toggle_calendar(self):
        """Function to toggle the calendar on and off"""
        if self.calendar_visible:
            self.calendar_widget.destroy() #Remove Calendar
            self.calendar_visible = False #Update Visibility
        else:
            # Create inline calendar right below the date row
            self.calendar_widget = Calendar(self, selectmode='day') #Create Calendar
            self.calendar_widget.grid(row=3, column=0, columnspan=2, padx=15, sticky="w") #Place Calendar

            self.calendar_widget.bind("<<CalendarSelected>>", self.date_selected) #Bind Calendar Selected to date Selected Function
            self.calendar_visible = True #Update Calendar Visibility
    
    def date_selected(self, event):
        """Return the date when selected"""
        updated_date = self.calendar_widget.get_date() #Grab Selected Date
        
        updated_date = datetime.strptime(updated_date, "%m/%d/%y") #get date Format

        updated_date = updated_date.strftime("%Y-%m-%d") #Update Date format
        self.selected_date = updated_date


        self.date_label.configure(text=self.selected_date) #Update Date label
        self.calendar_widget.destroy() #Destroy the calendar Widget
        self.calendar_visible = False #Update Visibility
        
        print("Selected date:", self.selected_date) #FOR TESTING

        self.refresh_games()

    def refresh_games(self):
        """Function for refreshing data once user selects new date"""
        # Fetch new data
        self.games_data = get_games_by_date(self.selected_date)

        # Destroy existing game frame if it exists
        if hasattr(self, "games_frame"):
            self.games_frame.destroy()

        # Recreate the games frame with new data
        self.games_frame = GamesDisplayFrame(self, self.games_data)
        self.games_frame.grid(row=3, column=0, padx=PADX, pady=PADY, sticky="nsew")

class GamesDisplayFrame(ctk.CTkFrame):
    """Class for Displaying games based on users selected date"""
    def __init__(self, parent, games_data):
        super().__init__(parent)

        self.games_data = games_data

        print(self.games_data)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        #Check If data Is available
        if self.games_data == 0:

            failed_label = ctk.CTkLabel(self, text="Failed to Fetch Data", font=("IMPACT", 24)) #Create Label
            failed_label.grid(row=3, column=0, padx=PADX, pady=PADY, sticky="ew") #Place Label
        
        #Check if there are games on selected date
        elif self.games_data == 1:

            no_games_label = ctk.CTkLabel(self, text="No Games Scheduled Today", font=("IMPACT", 24)) #Create Label
            no_games_label.grid(row=3, column=0, padx=PADX, pady=PADY, sticky="ew") #Place Label
        else:
            for i in range(0, len(self.games_data), 2):
                game1 = self.games_data[i]

                game_frame1 = ctk.CTkFrame(self)
                game_frame1.grid(row=i, column=0, padx=PADX, pady=PADY, sticky="ew")
                game_frame1.columnconfigure(0, weight=1)

                #Config of new frame
                home_team_label = ctk.CTkLabel(game_frame1, text=game1["home_team_name"], font=("IMPACT", 14)) #Create Label
                home_team_label.grid(row=0, column=0, padx=PADX, pady=PADY, sticky="nw") #Place Label

                game_time_label = ctk.CTkLabel(game_frame1, text=game1["game_time"], font=("IMPACT", 14)) #Create Label
                game_time_label.grid(row=0, column=1, padx=PADX, pady=PADY, sticky="e") #Place Label

                away_team_label = ctk.CTkLabel(game_frame1, text=game1["away_team_name"], font=("IMPACT", 14)) #Create Label
                away_team_label.grid(row=1, column=0, padx=PADX, pady=PADY, sticky="sw") #Place LabelACT", 14)).grid(row=1, column=0, padx=PADX, pady=PADY, sticky="sw")

                if i + 1 < len(self.games_data):
                    game2 = self.games_data[i + 1]

                    game_frame2 = ctk.CTkFrame(self)
                    game_frame2.grid(row=i, column=1, padx=PADX, pady=PADY, sticky="ew")
                    game_frame2.columnconfigure(0, weight=1)

                    home_team_label = ctk.CTkLabel(game_frame2, text=game2["home_team_name"], font=("IMPACT", 14)) #Create Label
                    home_team_label.grid(row=0, column=0, padx=PADX, pady=PADY, sticky="nw") #Place Label

                    game_time_label = ctk.CTkLabel(game_frame2, text=game2["game_time"], font=("IMPACT", 14)) #Create Label
                    game_time_label.grid(row=0, column=1, padx=PADX, pady=PADY, sticky="e") #Place Label

                    away_team_label = ctk.CTkLabel(game_frame2, text=game2["away_team_name"], font=("IMPACT", 14)) #Create Label
                    away_team_label.grid(row=1, column=0, padx=PADX, pady=PADY, sticky="sw") #Place Label
        

class StandingsFrame(ctk.CTkFrame):
    """Create Frame for displaying standings"""
    def __init__(self, parent):
        super().__init__(parent)
        
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

        
class Sidebar(ctk.CTkFrame):
    """Side Bar of the application"""
     
    def __init__(self, parent, update_frame):
        super().__init__(parent, width=75)
        self.update_frame = update_frame
        
        self.grid_propagate(False) #Prevent Resizing Based on child widgets
        self.grid_columnconfigure(0, weight=1) #Centers All widgets

        #Importing Images
        app_logo = ctk.CTkImage(light_image=Image.open(LOGO),
                                dark_image=Image.open(LOGO),
                                size=(50,50)) #Import App Logo
        
        scoreboard_icon = get_image(SCOREBOARD_ICON) #Import Scoreboard Icon
        
        standings_icon = get_image(STANDINGS_ICON) #Import Standings icon
        
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
        button = ctk.CTkButton(self, text="", image=image, fg_color="transparent", command=function)
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

def get_image(base_path):
    """Function to open images"""
    return ctk.CTkImage(light_image=Image.open(base_path + "light.png"),
                        dark_image=Image.open(base_path + "dark.png"),
                        size=(50, 50))