from app import get_games_by_date, Application

def main():
    
    games_data = get_games_by_date()
    app = Application(games_data) #Send Games Data to GUI

    app.mainloop()
    



if __name__ == "__main__":
    main()