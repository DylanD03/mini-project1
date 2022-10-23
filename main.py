"""		
Mini-Project 1

"""

# Import modules
from database_functions import *
import os

def clear():
    '''
    Clears the terminal screen and scroll back to present
    the user with a nice clean, new screen. 
    '''
    os.system('cls||echo -e \\\\033c')

def exit_program():
    # close all sessions then exit the program.
    close_all_sessions() # FIX: need to implement "close all sessions" part # defined in database_functions.py file
    pass

def login_menu(login_options):
    """
    prints login menu to the terminal

    options (list of strings) : The options to display in the menu
    """
    clear()
    print("--------------------------------------")
    print("\t","Login Menu","\n")
    print(" Enter \'q\' to exit the program")
    print(" Here are your options:\n")
    # Displaying each option and it's corresponding reference number.
    for i, option in enumerate(login_options):
        # Example, " 1 : User/Artist login"
        print(" ",str(i+1),":",option) # reference numbers range from 1-n
    print("--------------------------------------")

def user_menu(user_options, user = None):
    """
    prints user menu to the terminal

    options (list of strings) : The options to display in the menu
    """
    clear()
    print("--------------------------------------")
    print("\t","Login Menu","\n")
    print(" Enter \'q\' to exit the program")
    print(" Enter \'l\' to log out")
    if user is not None:
        print(" Welcome, ",current_user)
    print(" Here are your options:\n")
    # Displaying each option and it's corresponding reference number.
    for i, option in enumerate(user_options):
        # Example, " 1 : Start a session "
        print(" ",str(i+1),":",option) # reference numbers range from 1-n
    print("--------------------------------------")



def main():
    login_options = ["User/Artist login", "Register user"]
    database = "./tables.db"
    assert(os.path.exists(database)) 

    # Log in menu
    while True:
        login_menu(login_options)
        user_Input = input("Your Input : ")
        if user_Input == "q" or user_Input == "Q": # Exit the Program
            exit_program() 
       
        """
        -- Need to Implement login proccessing here --

        """


        # User Menu -- after user has succesfully logged in
        while True:
            user_options = ["Start a session", "Search for songs and playlists", 
                "Search for artists", "End the session"
                ]
            user_menu(user_options)
            user_Input = input("Your Input : ")
            if user_Input == "q" or user_Input == "Q": # Exit the Program
                exit_program() 
            """
            -- Implement user input processing here -- 

            """



if __name__ == "__main__":
    main()