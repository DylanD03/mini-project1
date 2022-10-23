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
    print("              Login Menu              ")
    print(" Enter \'q\' to exit the program")
    print(" Here are your options:\n")
    # Displaying each option and it's corresponding reference number.
    for i, option in enumerate(login_options):
        # Example, " 1 : User/Artist login"
        print(" ",str(i+1),":",option) # design choice - reference numbers range from 1-n (enumarate starts from i=0)
    print("--------------------------------------")

def user_menu(user_options, user = None):
    """
    prints user menu to the terminal

    options (list of strings) : The options to display in the menu
    """
    clear()
    print("--------------------------------------")
    print("               User Menu              ")
    print(" Enter \'q\' to exit the program")
    print(" Enter \'l\' to log out")
    if user is not None:
        print(" Welcome, ",current_user)
    print(" Here are your options:\n")
    # Displaying each option and it's corresponding reference number.
    for i, option in enumerate(user_options):
        # Example, " 1 : Start a session "
        print(" ",str(i+1),":",option) # design choice - reference numbers range from 1-n (enumarate starts from i=0)
    print("--------------------------------------")

def safe_Input(user_Input, options):
    """
    Checks - String is not empty, in the range of our options,

    Parameters: 
    options (list of strings) : The options listed in the corresponding menu.
    Returns
    (string) user_Input : The option selected by the user. 
    """

    if not user_Input.isdigit() or user_Input == '':
        return False # Cant be an empty string, and has to be a digit.  
    if int(user_Input) not in list(range(1, len(options)+1)): # Input must be an integer between [1,n] where n is the number of options
        return False # Input is not in the range of 1-n where n is the number of options
    return True # Passes all sanity checks

def process_login(option):
    """
    Proccessing user input in the Login screen. 
    Parameters:
    option (string) : The selection made by the user in the Login screen.
    Returns:
    """
    if option == "User/Artist Login":
        pass 
    elif option == "Register User":
        pass 
    # probably need to return cid/aid if they log in successfully.

def main():
    login_options = ["User/Artist login", "Register user"]
    database = "./tables.db"
    assert(os.path.exists(database)) 

    # Log in menu
    while True:
        login_menu(login_options)
        user_Input = input(" Your Input: ") # TODO: exception handling (read from file?). Probably dont need.
        if user_Input in ['q','Q']: 
            exit_program()          # close sessions and exit
        if safe_Input(user_Input, login_options): # Checks if input is valid.
            process_login(login_options[int(user_Input)-1]) # User input is 1-indexed (design choice) while python arrays are 0-indexed.


        # User Menu -- after user has succesfully logged in
        while True:
            user_options = ["Start a session", "Search for songs and playlists", 
                "Search for artists", "End the session"
                ]
            user_menu(user_options)
            user_Input = input("Your Input : ")
            if user_Input in ['q','Q']: 
                exit_program()      # close sessions and exit
            if user_Input in ['l','L']:
                break               # log out
            """
            -- Implement user input processing here -- 

            """




if __name__ == "__main__":
    main()