import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import customtkinter as ctk
from datetime import datetime
from PIL import Image
from assets.constants import *

class Application(ctk.CTk):
    """GUI Logic for application"""
    def __init__(self, games_data):  
        super().__init__()
        self.games_data = games_data


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
            self.main_area = frame_class(self, self.games_data)
                 
        else:
            self.main_area = frame_class(self) #If scores frame is not selected create a basic class
            
        self.main_area.grid(row=0, column=1, pady=PADY, padx=3, sticky="nsew") # Placed Right of Sidebar, Fills Remaining Area
        
class ScoresFrame(ctk.CTkFrame):
    """Create Frame for displaying scores"""
    def __init__(self, parent, games_data):
        super().__init__(parent)
        
        self.games_data = games_data
        self.calendar_visible = False
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

        # Create a horizontal frame to hold the date label and calendar button side by side
        date_row = ctk.CTkFrame(self)
        date_row.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="w")
        date_row.grid_columnconfigure(0, weight=0)
        date_row.grid_columnconfigure(1, weight=0)

        # Date label
        self.date_label = ctk.CTkLabel(date_row, text=games_data[0]["date"], font=("IMPACT", 20))
        self.date_label.grid(row=0, column=0, padx=(0, 10), pady=0)

        # Calendar button
        open_calendar = ctk.CTkButton(date_row, text="", image=calendar_icon, fg_color="transparent", command=self.toggle_calendar, width=30)
        open_calendar.grid(row=0, column=1, pady=0)

        #Display Games
        for i in games_data:
            home_team = games_data[i]["home_team_name"]
            away_team = games_data[i]["away_team_name"]
            game_time = games_data[i]["game_time"]


            game_frame = ctk.CTkFrame(self)
            game_frame.grid(row=i+3, column=0, padx=PADX, pady=PADY, sticky="nw")

            home_team_label = ctk.CTkLabel(game_frame, text=home_team)
            home_team_label.grid(row=0, column=0, padx=PADX, pady=PADY, sticky="nw")

            game_time_label = ctk.CTkLabel(game_frame, text=game_time)
            game_time_label.grid(row=1, column=1, padx=PADX, pady=PADY, sticky="e")

            away_team_label = ctk.CTkLabel(game_frame, text=away_team)
            away_team_label.grid(row=2, column=0, padx=PADX, pady=PADY, sticky="sw")
        
    def toggle_calendar(self):
        if self.calendar_visible:
            self.calendar_widget.destroy()
            self.calendar_visible = False
        else:
            # Create inline calendar right below the date row
            self.calendar_widget = Calendar(self, selectmode='day')
            self.calendar_widget.grid(row=3, column=0, columnspan=2, padx=15, sticky="w")

            self.calendar_widget.bind("<<CalendarSelected>>", self.date_selected)
            self.calendar_visible = True
        
    def date_selected(self, event):
        selected_date = self.calendar_widget.get_date()
        
        selected_date = datetime.strptime(selected_date, "%m/%d/%y")

        selected_date = selected_date.strftime("%Y-%m-%d")


        self.date_label.configure(text=selected_date)
        self.calendar_widget.destroy()
        self.calendar_visible = False
        print("Selected date:", selected_date)




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

        #Importing Images
        app_logo = ctk.CTkImage(light_image=Image.open(LOGO),
                                dark_image=Image.open(LOGO),
                                size=(50,50))
        
        scoreboard_icon = get_image(SCOREBOARD_ICON)
        
        standings_icon = get_image(STANDINGS_ICON)
        
        self.logo = ctk.CTkLabel(self, image=app_logo, text="")
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
        """Logic to change the theme"""
        theme = self.theme.get()

        if theme == 1:
            ctk.set_appearance_mode("dark")
            self.theme_label.configure(text="Darkmode\n(On)")
        else:
            ctk.set_appearance_mode("light")
            self.theme_label.configure(text="Darkmode\n(Off)")

def get_image(base_path):
    return ctk.CTkImage(light_image=Image.open(base_path + "light.png"),
                        dark_image=Image.open(base_path + "dark.png"),
                        size=(50, 50))