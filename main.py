from app import Application, initialize_database, update_display_mode, get_display_mode

def main():
    
    initialize_database() #Initializees database if it has not already been created

    app = Application() #Send Games Data to GUI

    app.mainloop()
    
if __name__ == "__main__":
    main()