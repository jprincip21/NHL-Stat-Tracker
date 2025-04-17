from app import get_games_by_date, Application

def main():
    get_games_by_date()
    app = Application()
    app.mainloop()



if __name__ == "__main__":
    main()