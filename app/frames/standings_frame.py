import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

import threading

from utilities import get_standings
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

        self.filter_buttons = [self.division_btn, self.wildcard_btn, self.conference_btn, self.overall_btn]
        
        self.standings_main_frame = ctk.CTkScrollableFrame(self, height=430)

        self.standings_main_frame.columnconfigure(0, weight=1)
        self.standings_main_frame.columnconfigure(1, weight=0)
        self.standings_main_frame.columnconfigure(2, weight=0)
        self.standings_main_frame.columnconfigure(3, weight=0)
        self.standings_main_frame.columnconfigure(4, weight=0)
        
        self.standings_main_frame.grid(row=4, column=0, padx=PADX, pady=PADY, sticky="ew")
        self.standings_current_frame = None #Placeholder
        self.standings_frame_list = {} #Placeholder

        labels_frame = ctk.CTkFrame(self) 
        labels_frame.grid(row=3, column=0, padx=PADX, pady=PADY) 

        headers = [
                ("Team", 250),
                ("GP", 30),
                ("PTS", 30),
                ("W-L-OTL", 50),
                ("PTS%", 30),
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
        
        self.wild_card_standings = {"Eastern" : {"Atlantic" : [],
                                                 "Metropolitan" : [],
                                                 "Wild Card": []}, 
                                   
                                   "Western" : {"Pacific" : [],
                                                "Central" : [],
                                                "Wild Card": []}
                                                }
        
        self.fetch_standings()

    def create_button(self, text, col, disabled=False, command=None):
        """Creates Buttons with provided command if needed"""
        button = ctk.CTkButton(self.filter_btn_frame, 
                               text=text,  
                               fg_color="transparent", 
                               text_color=("black", "white"),
                               font=("IMPACT", 18),
                               anchor="center",
                               hover="false",
                               state="disabled")
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
            
        self.organize_standings()

        self.progress_bar.grid_remove() 
        self.progress_bar.stop()
        self.change_filter(self.division_btn, "Division") #Sets Default Frame

        
    def organize_standings(self):
        """Function to Organize Standings by points, Conference and Division"""
        # Clear existing entries in each list
        
        self.overall_standings.sort(key=lambda x: x["points"], reverse=True) #Sort Standings by points
        
        for conf in self.conference_standings:
            self.conference_standings[conf].clear()

        for div in self.division_standings:
            self.division_standings[div].clear()

        for conf in self.wild_card_standings:
            for div in self.wild_card_standings[conf]:
                self.wild_card_standings[conf][div].clear()

        for team in self.overall_standings:
            self.conference_standings[team["conference"]].append(team) #Seperate Teams By conference
            self.division_standings[team["division"]].append(team) # Seperate Teams by Division

        for division, teams in self.division_standings.items():
            top_3 = teams[:3] #Grab top 3 Teams of each division
            for team in top_3:
                self.wild_card_standings[team["conference"]][division].append(team)
        
        for conference, teams in self.conference_standings.items():
            for team in teams: #
                if team not in self.wild_card_standings[conference][team["division"]]:
                    self.wild_card_standings[team["conference"]]["Wild Card"].append(team)

    def render_standings(self, filter_type):
        """Function which renders standings by sent filter type"""  

        if not self.overall_standings: #Catches Errors
            failed_label = ctk.CTkLabel(self.standings_main_frame, text="Failed to Fetch Data", font=("IMPACT", 24)) #Create Label
            failed_label.grid(row=2, column=0, padx=PADX, pady=PADY, sticky="ew") #Place Label
            return 
        
        else:
            for button in self.filter_buttons:
                button.configure(state="enabled") #After Standings Are fetched activate Buttons.
   
        if hasattr(self, "standings_current_frame") and self.standings_current_frame is not None: 
            self.standings_current_frame.grid_forget() #Hide current frame if there is one being displayed
        
        if filter_type not in self.standings_frame_list: #If filter has not yet been selected
            frame = ctk.CTkFrame(self.standings_main_frame)

            if filter_type == "Division":
                self.render_group_standings(self.division_standings, frame)
                
            elif filter_type == "Wild Card":
               self.render_wild_card_standings(self.wild_card_standings, frame)

            elif filter_type == "Conference":
                self.render_group_standings(self.conference_standings, frame)        

            elif filter_type == "Overall":
                for row, team in enumerate(self.overall_standings): 
                    self.render_team_row(row, team, frame)
            
            frame.grid(row=1, column=0, padx=PADX, pady=PADY)

            self.standings_frame_list[filter_type] = frame #add the created frame to the standings frame list to be cached for later
        else:
            frame = self.standings_frame_list[filter_type]
            frame.grid(row=1, column=0, padx=PADX, pady=PADY)

        self.standings_current_frame = frame #set the active frame to standings_display frame so it can be forgotten in the hasattr

    def render_wild_card_standings(self, wild_card, frame):
        current_row = 0
        for conference, divisions in wild_card.items():
            self.create_label(frame, conference, row=current_row, font=("IMPACT", 20), padx=10, pady=10)
            
            current_row +=1
            for division, teams in divisions.items():
                self.create_label(frame, division, row=current_row, font=("IMPACT", 18), padx=10, pady=10)
                current_row +=1

                for team in teams:
                    self.render_team_row(current_row, team, frame)
                    current_row +=1

    def render_group_standings(self, grouped_data, frame, current_row=0):
        """Function which creates a label of category and then calls 
        render team row to display teams in that category (Conference and Division Standings)"""
        for group_name, teams in grouped_data.items():
            self.create_label(frame, group_name, 250, 0, current_row, font=("IMPACT", 20), padx=10, pady=10)
            current_row +=1

            for team in teams:
                self.render_team_row(current_row, team, frame)
                current_row += 1                


    def render_team_row(self, row, team, frame):
        """Function which makes a tuple of team info and label size (Overall Standings)"""
        logo = team["team_logo"]
        team_stats = [
            (f"{team['team_name']}", 250),
            (f"{team['games_played']}", 30),
            (f"{team['points']}", 30),
            (f"{team['record']}", 50),
            (f"{round(team['points_percent'], 2)}", 30),
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


    def create_label(self, parent, text, width=200, col=0, row=0, image=None, font=("IMPACT", 14), padx=5, pady=5):
        """Function which creates labels"""
        label = ctk.CTkLabel(
                    parent,
                    image=image if col==0 and image else None, #Image is default None, If an Image is sent, only display on Column 0
                    compound="left",
                    text=text,
                    font=font,
                    width=width,
                    anchor="w"
                )
        label.grid(row=row, column=col, sticky="ew", padx=padx, pady=pady)
