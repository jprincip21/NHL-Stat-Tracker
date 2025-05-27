import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import threading
import customtkinter as ctk

from datetime import datetime, date

from assets.constants import *
from utilities import get_games_by_date, get_image_light_dark, get_team_logo

class ScoresFrame(ctk.CTkFrame):
    """Create Frame for displaying scores"""
    def __init__(self, parent):
        super().__init__(parent)

        self.calendar_visible = False #Set calendar Visibility to false
        self.calendar_widget = None 
        self.refresh_job = None

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

        calendar_icon = get_image_light_dark(CALENDAR_ICON)

        # Frame to Hold Date and Date Button
        self.date_frame = ctk.CTkFrame(self, corner_radius=5)
        self.date_frame.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")
        self.date_frame.grid_columnconfigure(0, weight=0)
        self.date_frame.grid_columnconfigure(1, weight=0)

        
        # Calendar button In date_frame
        self.open_calendar_button = ctk.CTkButton(self.date_frame, text="", image=calendar_icon, fg_color="transparent", command=self.toggle_calendar, width=30, anchor="center")
        self.open_calendar_button.grid(row=0, column=0, pady=0)

        #Initalize Date and Games Data
        self.selected_date = date.today().strftime("%Y-%m-%d")
        self.progress_bar = ctk.CTkProgressBar(self, width=600,)
        self.games_data = None  # placeholder

        #print(self.selected_date) # FOR TESTING

        # Date label in date_frame
        self.date_label = ctk.CTkLabel(self.date_frame, text=self.selected_date, font=("IMPACT", 20))
        self.date_label.grid(row=0, column=1, padx=PADX, pady=0)

        self.scheduled_refresh()

    def toggle_calendar(self):
        """Function to toggle the calendar on and off"""
        date_obj = datetime.strptime(self.selected_date, "%Y-%m-%d")
        if self.calendar_visible:
            self.calendar_widget.destroy() #Remove Calendar
            self.calendar_visible = False #Update Visibility
        else:
            # Create inline calendar right below the date row
            self.calendar_widget = Calendar(self, 
                                            selectmode='day', 
                                            firstweekday='sunday', 
                                            date_pattern=("yyyy-mm-dd"), #Return Format from get_date() Function

                                            background="#4A4A4A",
                                            foreground="white",
                                            headersbackground="#4A4A4A",
                                            headersforeground="white",
                                            normalbackground="#7C7C7C",
                                            normalforeground="white",
                                            weekendbackground="#7C7C7C",
                                            weekendforeground="white",
                                            othermonthbackground="#5A5A5A",
                                            othermonthforeground="white",
                                            othermonthwebackground="#5A5A5A",
                                            othermonthweforeground="white",

                                            year=date_obj.year, 
                                            month=date_obj.month, 
                                            day=date_obj.day) #Create Calendar
            self.calendar_widget.grid(row=3, column=0, columnspan=2, padx=15, sticky="w") #Place Calendar

            self.calendar_widget.bind("<<CalendarSelected>>", self.date_selected) #Bind Calendar Selected to date Selected Function
            self.calendar_visible = True #Update Calendar Visibility
    
    def date_selected(self, event):
        """Return the date when selected"""
        new_date = self.calendar_widget.get_date()

        if new_date == self.selected_date: #If Same date is selected do nothing.
            print("Same date selected... No Change")
            self.calendar_widget.destroy()
            self.calendar_visible = False
            return 
        
        self.selected_date = self.calendar_widget.get_date() #Grab Selected Date

        self.date_label.configure(text=self.selected_date) #Update Date label
        self.calendar_widget.destroy() #Destroy the calendar Widget
        self.calendar_visible = False #Update Visibility
        
        #print("Selected date:", self.selected_date) #FOR TESTING

        self.games_frame.grid_forget()
        
        if self.refresh_job is not None:
            print("Scheduled Refresh Canceled")
            self.after_cancel(self.refresh_job)
            self.refresh_job = None

        if self.selected_date == str(date.today()):
            self.scheduled_refresh()

        else: 
            self.refresh_games()

    def scheduled_refresh(self):
        """Refreshes GamesDisplayFrame After 30 Seconds"""
        
        if self.selected_date == str(date.today()):
            print("Scheduled Refresh...")
            self.refresh_games()
            self.refresh_job = self.after(30000, self.scheduled_refresh)
            
        else:
            self.refresh_games()

    def refresh_games(self):
        """Refresh games using background thread and show progress bar."""
        
        print("Refreshing...")

        # Show and start progress bar
        self.progress_bar.set(0)
        self.progress_bar.start()
        self.progress_bar.grid(row=3, column=0, padx=PADX, pady=PADY)

        # Start background thread to fetch game data
        thread = threading.Thread(target=self.fetch_games_thread)
        thread.start()

    def fetch_games_thread(self):
        """Background thread to fetch data and update UI."""
        try:
            data = get_games_by_date(self.selected_date)
            self.after(0, lambda: self.progress_bar.set(1))
            self.after(0, lambda: self.update_games_display(data))
        except Exception as e:
            print(f"Error fetching game data: {e}") 

    def update_games_display(self, data):
        """Safely update the UI with new game data."""
        self.games_data = data

        # Destroy old frame
        if hasattr(self, "games_frame"):
            self.games_frame.destroy()

        #Remove Progress bar
        self.progress_bar.grid_remove() 
        self.progress_bar.stop()
        # Create new frame
        self.games_frame = GamesDisplayFrame(self, self.games_data, self.selected_date)
        self.games_frame.grid(row=3, column=0, padx=PADX, pady=PADY, sticky="nsew")



class GamesDisplayFrame(ctk.CTkFrame):
    """Class for Displaying games based on users selected date"""
    def __init__(self, parent, games_data, selected_date):
        super().__init__(parent)

        self.games_data = games_data
        self.selected_date = selected_date

        #print(self.games_data) #For Testing

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        #Check If data Is available
        if self.games_data == 0:

            failed_label = ctk.CTkLabel(self, text="Failed to Fetch Data", font=("IMPACT", 24)) #Create Label
            failed_label.grid(row=0, column=0, padx=PADX, pady=PADY, sticky="ew") #Place Label
        
        #Check if there are games on selected date
        elif self.games_data == 1:

            no_games_label = ctk.CTkLabel(self, text=f"No Games Scheduled for {self.selected_date}", font=("IMPACT", 24)) #Create Label
            no_games_label.grid(row=0, column=0, padx=PADX, pady=PADY, sticky="ew") #Place Label
        else:
            
            self.columnconfigure(1, weight=1) # Update Column 1 Here so previous Labels are centered

            for i in range(0, len(self.games_data), 2):
                game1 = self.games_data[i]

                home_team1_logo = get_team_logo(game1["home_team_logo"])
                away_team1_logo = get_team_logo(game1["away_team_logo"])

                game_frame1 = ctk.CTkFrame(self)
                game_frame1.grid(row=i, column=0, padx=PADX, pady=PADY, sticky="ew")
                game_frame1.columnconfigure(0, weight=1)

                #Config of new frame
                home_team_label = ctk.CTkLabel(game_frame1, 
                                               image=home_team1_logo,
                                               compound="left", 
                                               text=game1["home_team_name"], 
                                               font=("IMPACT", 14)) #Create Label
                home_team_label.grid(row=0, column=0, padx=PADX, pady=PADY, sticky="nw") #Place Label

                away_team_label = ctk.CTkLabel(game_frame1, 
                                               image=away_team1_logo,
                                               compound="left", 
                                               text=game1["away_team_name"], 
                                               font=("IMPACT", 14)) #Create Label
                away_team_label.grid(row=1, column=0, padx=PADX, pady=PADY, sticky="sw") #Place Label 

                if game1["home_team_score"] is not None and game1["away_team_score"] is not None:
                    home_score_label = ctk.CTkLabel(game_frame1, text=game1["home_team_score"], font=("IMPACT", 14)) #Create Label
                    home_score_label.grid(row=0, column=1, padx=PADX, pady=PADY, sticky="e") #Place Label

                    away_score_label = ctk.CTkLabel(game_frame1, text=game1["away_team_score"], font=("IMPACT", 14)) #Create Label
                    away_score_label.grid(row=1, column=1, padx=PADX, pady=PADY, sticky="e") #Place Label   
                    
                    period_label = ctk.CTkLabel(game_frame1, text=game1["period"], font=("IMPACT", 14)) #Create Label
                    period_label.grid(row=0, column=2, padx=PADX, pady=PADY, sticky="e") #Place Label
                    
                    time_label = ctk.CTkLabel(game_frame1, text=game1["time_remaining"], font=("IMPACT", 14)) #Create Label
                    time_label.grid(row=1, column=2, padx=PADX, pady=PADY, sticky="w") #Place Label

                else:
                    game_time_label = ctk.CTkLabel(game_frame1, text=game1["game_time"], font=("IMPACT", 14)) #Create Label
                    game_time_label.grid(row=0, column=1, padx=PADX, pady=PADY, sticky="e") #Place Label                

                if i + 1 < len(self.games_data):
                    game2 = self.games_data[i + 1]

                    home_team2_logo = get_team_logo(game2["home_team_logo"])
                    away_team2_logo = get_team_logo(game2["away_team_logo"])

                    game_frame2 = ctk.CTkFrame(self)
                    game_frame2.grid(row=i, column=1, padx=PADX, pady=PADY, sticky="ew")
                    game_frame2.columnconfigure(0, weight=1)

                    home_team_label = ctk.CTkLabel(game_frame2, 
                                                   image=home_team2_logo,
                                                   compound="left", 
                                                   text=game2["home_team_name"], 
                                                   font=("IMPACT", 14)) #Create Label
                    home_team_label.grid(row=0, column=0, padx=PADX, pady=PADY, sticky="nw") #Place Label

                    away_team_label = ctk.CTkLabel(game_frame2, 
                                                   image=away_team2_logo,
                                                   compound="left", 
                                                   text=game2["away_team_name"], 
                                                   font=("IMPACT", 14)) #Create Label
                    away_team_label.grid(row=1, column=0, padx=PADX, pady=PADY, sticky="sw") #Place Label
                
                    if game2["home_team_score"] is not None and game2["away_team_score"] is  not None:

                        home_score_label = ctk.CTkLabel(game_frame2, text=game2["home_team_score"], font=("IMPACT", 14)) #Create Label
                        home_score_label.grid(row=0, column=1, padx=PADX, pady=PADY, sticky="e") #Place Label

                        away_score_label = ctk.CTkLabel(game_frame2, text=game2["away_team_score"], font=("IMPACT", 14)) #Create Label
                        away_score_label.grid(row=1, column=1, padx=PADX, pady=PADY, sticky="e") #Place Label

                        period_label = ctk.CTkLabel(game_frame2, text=game2["period"], font=("IMPACT", 14)) #Create Label
                        period_label.grid(row=0, column=2, padx=PADX, pady=PADY, sticky="e") #Place Label

                        time_label = ctk.CTkLabel(game_frame2, text=game2["time_remaining"], font=("IMPACT", 14)) #Create Label
                        time_label.grid(row=1, column=2, padx=PADX, pady=PADY, sticky="w") #Place Label


                    else:
                        game_time_label = ctk.CTkLabel(game_frame2, text=game1["game_time"], font=("IMPACT", 14)) #Create Label
                        game_time_label.grid(row=0, column=1, padx=PADX, pady=PADY, sticky="e") #Place Label 