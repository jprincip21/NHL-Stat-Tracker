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
        
        self.progress_bar = ctk.CTkProgressBar(self, width=600)
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
        self.change_filter(self.overall_btn, "Overall") #Sets Default Frame
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
        
        if hasattr(self, "standings_display_frame"):
            standings_display_frame.destroy()

        standings_display_frame = ctk.CTkScrollableFrame(self, height=411)
        standings_display_frame.columnconfigure(0, weight=1)
        
        standings_display_frame.grid(row=3, column=0, padx=PADX, pady=PADY, sticky="ew")

        if filter_type == "Division":
            division_label = ctk.CTkLabel(standings_display_frame, text="Division", font=("IMPACT", 24)) #Create Label
            division_label.grid(row=0, column=0, padx=PADX, pady=PADY, sticky="ew") #Place Label 

            for div, teams in self.division_standings.items(): #Testing
                print(f"\n{div}")
                for team in teams:
                    print(team["team_name"])
    

        elif filter_type == "Wild Card":
            wildcard_label = ctk.CTkLabel(standings_display_frame, text="Wild Card", font=("IMPACT", 24)) #Create Label
            wildcard_label.grid(row=0, column=0, padx=PADX, pady=PADY, sticky="ew") #Place Label     

        elif filter_type == "Conference":
            conference_label = ctk.CTkLabel(standings_display_frame, text="Conference", font=("IMPACT", 24)) #Create Label
            conference_label.grid(row=0, column=0, padx=PADX, pady=PADY, sticky="ew") #Place Label      
            
            for conf_name, teams in self.conference_standings.items(): #Testing
                print(f"\n{conf_name}")
                for team in teams:
                    print(team["team_name"])

        elif filter_type == "Overall":
            overall_label = ctk.CTkLabel(standings_display_frame, text="Overall", font=("IMPACT", 24)) #Create Label
            overall_label.grid(row=0, column=0, padx=PADX, pady=PADY, sticky="ew") #Place Label    
            print("\n")
            for team in self.overall_standings: #Testing
                print(team["team_name"])  
