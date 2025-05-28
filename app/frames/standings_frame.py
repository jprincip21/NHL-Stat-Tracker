import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

import threading

from utilities import get_standings, get_team_logo
from assets.constants import *

class StandingsFrame(ctk.CTkFrame):
    """Create Frame for displaying standings"""
    def __init__(self, parent):
        super().__init__(parent)
        self.active_button = None
        
        #Layout Config
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0) #Heading
        self.rowconfigure(1, weight=0, minsize=5) #seperator
        self.rowconfigure(2, weight=0) #Filter Buttons

        
        #Heading label
        heading = ctk.CTkLabel(self, text="STANDINGS", font=("IMPACT", 50)) #Create Label
        heading.grid(row=0, column=0, padx=15, pady=PADY, sticky="nw" ) #Place Label

        #Seperator Line
        separator = ctk.CTkFrame(self, height=5) #Create Separator
        separator.grid(row=1, column=0, padx=PADX, pady=PADY, sticky="ew") #Place Separator
        separator.grid_propagate(False) #Prevents Shrinking

        self.filter_btn_frame = ctk.CTkFrame(self) #Frame for Standings Filter Buttons
        self.filter_btn_frame.grid(row=2, column=0, padx=PADX, pady=PADY, sticky="ew") 
        

        self.filter_btn_frame.grid_columnconfigure(0,weight=1) 
        self.filter_btn_frame.grid_columnconfigure(1,weight=1)
        self.filter_btn_frame.grid_columnconfigure(2,weight=1)
        self.filter_btn_frame.grid_columnconfigure(3,weight=1)

        self.division_btn = self.create_button("Division", 0)
        self.wildcard_btn = self.create_button("Wild Card", 1)
        self.conference_btn = self.create_button("Conference", 2)
        self.overall_btn = self.create_button("Overall", 3)

        self.division_btn.configure(command=lambda: self.change_filter(self.division_btn, "Division"))
        self.wildcard_btn.configure(command=lambda: self.change_filter(self.wildcard_btn, "Wild Card"))
        self.conference_btn.configure(command=lambda: self.change_filter(self.conference_btn, "Conference"))
        self.overall_btn.configure(command=lambda: self.change_filter(self.overall_btn, "Overall"))
        
        self.standings_main_frame = ctk.CTkScrollableFrame(self, height=430)

        self.standings_main_frame.columnconfigure(0, weight=1)
        self.standings_main_frame.columnconfigure(1, weight=0)
        self.standings_main_frame.columnconfigure(2, weight=0)
        self.standings_main_frame.columnconfigure(3, weight=0)
        self.standings_main_frame.columnconfigure(4, weight=0)
        
        self.standings_main_frame.grid(row=3, column=0, padx=PADX, pady=PADY, sticky="ew")

        labels_frame = ctk.CTkFrame(self.standings_main_frame) 
        labels_frame.grid(row=0, column=0, padx=PADX, pady=PADY) 

        headers = [
                ("Team", 250),
                ("GP", 30),
                ("Pts", 30),
                ("W-L-OTL", 50),
                ("Pts%", 30),
                ("RW", 30),
                ("ROW", 30),
                ("GF", 30),
                ("GA", 30),
                ("GD", 30),
                ("SO W-L", 40),
                ("Last 10", 40),
                
            ]
        
        for i, (text, width) in enumerate(headers):
            self.create_label(labels_frame, text, width, i)

        self.progress_bar = ctk.CTkProgressBar(self.standings_main_frame, width=600, determinate_speed=0.25)
        self.overall_standings = None    
        self.conference_standings = {"Eastern" : [], 
                                     "Western" : []}
        self.division_standings = {"Atlantic" : [], 
                                   "Metropolitan" : [], 
                                   "Central" : [], 
                                   "Pacific" : []}
        
        self.fetch_standings()

    def create_button(self, text, col, disabled=False, command=None):
        """Creates Buttons with provided command if needed"""
        button = ctk.CTkButton(self.filter_btn_frame, 
                               text=text,  
                               fg_color="transparent", 
                               text_color=("black", "white"),
                               font=("IMPACT", 18),
                               anchor="center",
                               hover="false")
        button.grid(column=col, row=0, padx=PADX, pady=PADY)

        return button
    
    def change_filter(self, clicked_button, filter_type):
        """Command for buttons to update Button State and UI"""
        self.render_standings(filter_type)

        if self.active_button and self.active_button != clicked_button:
            self.active_button.configure(state="normal", fg_color="transparent", text_color=("black", "white"))

        clicked_button.configure(state="disabled", fg_color="#3D75A0")
        

        self.active_button = clicked_button

    def fetch_standings(self):
        """Starts thread for Fetching Standings and Creates Progress bar"""
        print("Fetching Standings...")

        self.progress_bar.set(0)
        self.progress_bar.start()
        self.progress_bar.grid(row=3, column=0, padx=PADX, pady=PADY)

        thread = threading.Thread(target=self.fetch_standings_thread)
        thread.start()
    
    def fetch_standings_thread(self):
        """Fetches Standings and Calls Process_standings After"""
        try:
            data = get_standings()
            self.after(0, lambda: self.progress_bar.set(1))
            self.after(0, lambda: self.process_standings(data))
        except Exception as e:
            print(f"Error fetching standings data: {e}") 

    def process_standings(self, standings):
        self.overall_standings = standings

        if not self.overall_standings: #Catches Errors
            failed_label = ctk.CTkLabel(self, text="Failed to Fetch Data", font=("IMPACT", 24)) #Create Label
            failed_label.grid(row=3, column=0, padx=PADX, pady=PADY, sticky="ew") #Place Label
            return 
            
        self.organize_standings()

        self.progress_bar.grid_remove() 
        self.progress_bar.stop()
        self.change_filter(self.division_btn, "Division") #Sets Default Frame
        # for team in standings:
        #     print(team)
        
    def organize_standings(self):
        """Function to Organize Standings by points, Conference and Division"""
        # Clear existing entries in each list
        for conf in self.conference_standings:
            self.conference_standings[conf].clear()

        for div in self.division_standings:
            self.division_standings[div].clear()

        for team in self.overall_standings:
            self.conference_standings[team["conference"]].append(team) #Seperate Teams By conference
            self.division_standings[team["division"]].append(team) # Seperate Teams by Division

        self.overall_standings.sort(key=lambda x: x["points"], reverse=True) #Sort Standings
        
        for conf in self.conference_standings:
            self.conference_standings[conf].sort(key=lambda x:x["points"], reverse=True) #Sort Conference Standings
        
        for div in self.division_standings:
            self.division_standings[div].sort(key=lambda x:x["points"], reverse=True) #Sort Division Standings

    def render_standings(self, filter_type):
        """Function which renders standings by sent filter type"""
        if hasattr(self, "standings_display_frame"):
            self.standings_display_frame.destroy()

        self.standings_display_frame = ctk.CTkFrame(self.standings_main_frame)
        self.standings_display_frame.grid(row=1, column=0, padx=PADX, pady=PADY)

        if filter_type == "Division":

            self.render_group_standings(self.division_standings, self.standings_display_frame)
            
        elif filter_type == "Wild Card":
            pass

        elif filter_type == "Conference":
            self.render_group_standings(self.conference_standings, self.standings_display_frame)        

        elif filter_type == "Overall":
            for row, team in enumerate(self.overall_standings): 
                self.render_team_row(row, team, self.standings_display_frame)

    def render_group_standings(self, grouped_data, frame):
        """Function which creates a label of category and then calls render team row to display teams in that category"""
        current_row = 0
        for group_name, teams in grouped_data.items(): #Testing
            conference_label = ctk.CTkLabel(self.standings_display_frame,
                                            text=group_name,
                                            font=("IMPACT", 20),
                                            anchor="w")
            conference_label.grid(row=current_row, 
                                    column=0, 
                                    columnspan=12, 
                                    sticky="w", 
                                    padx=10,
                                    pady=10)
            current_row +=1

            for team in teams:
                self.render_team_row(current_row, team, frame)
                current_row += 1                


    def render_team_row(self, row, team, frame):
        """Function which makes a tuple of team info and label size"""
        logo = team["team_logo"]
        team_stats = [
            (f"{team['team_name']}", 250),
            (f"{team['games_played']}", 30),
            (f"{team['points']}", 30),
            (f"{team['record']}", 50),
            (f"{round(team['points_percent'], 3)}", 30),
            (f"{team['regulation_wins']}", 30),
            (f"{team['regulation_ot_wins']}", 30),
            (f"{team['goals_for']}", 30),
            (f"{team['goals_against']}", 30),
            (f"{team['goal_diff']}", 30),
            (f"{team['shootout']}", 40),
            (f"{team['last_ten']}", 40),
        ]
        for col, (text, width) in enumerate(team_stats):
            self.create_label(frame, text, width, col, row=row, image=logo)


    def create_label(self, parent, text, width, col, row=0, image=None):
        """Function which creates labels"""
        label = ctk.CTkLabel(
                    parent,
                    image=image if col==0 and image else None, #Image is default None, If an Image is sent, only display on Column 0
                    compound="left",
                    text=text,
                    font=("IMPACT", 14),
                    width=width,
                    anchor="w"
                )
        label.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
