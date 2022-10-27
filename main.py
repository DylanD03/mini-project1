"""     
Mini-Project 1

"""

# Import modules
from pickle import TRUE
from database_functions import *
from getpass import *
import os
DEBUG = True

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

    login_options (list of strings) : The options to display in the menu
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
    user (string) : name of user
    """
    clear()
    print("--------------------------------------")
    print("               User Menu              ")
    print(" Enter \'q\' to exit the program")
    print(" Enter \'l\' to log out")
    if user is not None:
        print(" Welcome, ", user)
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
    options (list of strings) : The options to select from
    user input(list of strings) : either 1 or 2, corresponding to user or artist respectively.
    
    Returns
    bool
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
    username (string) : uid or aid of the user logging in. Returns None if login/register is unsuccessful.
    """
    username = None
    if option == "User/Artist login":
        username = input("\nInput your Username: ")
        pwd = getpass(prompt='\nInput your password: ') 
        if is_user(username) and is_artist(username):
            choice = input("\n Input \'1\' to log in as a user, or Input \'2\' to log in as an artist.")
            if not safe_Input(choice, [1,2]):
                return None # not one of the options. 
            if choice == 1:
                username = user_login(username, pwd)
            else:
                username = artist_login(username, pwd)
        if is_user(username): # cannot be both user and artist. at most 1.
            return user_login(username, pwd)
        if is_artist(username):
            return artist_login(username, pwd)
        return None # user does not exist in either table.

    elif option == "Register User":
        username = input("\nInput your Username (4 characters): ")
        name = input("\nInput your Name: ")
        pwd = getpass(prompt='\nInput your password: ') 
        username = register_user(username, name, pwd) # returns None if unsuccessful. i.e., user with that uid already exists.    

    return username 

def main():
    
    database = "./tables.db"
    assert(os.path.exists(database)) 

    # Log in menu
    while True:
        username = None
        session = None
        login_options = ["User/Artist login", "Register User"]
        login_menu(login_options)
        user_Input = input(" Your Input: ") # TODO: exception handling (read from file?). Probably dont need.
        if user_Input in ['q','Q']: 
            exit_program()          # close sessions and exit
        if safe_Input(user_Input, login_options): # Checks if input is valid.
            username = process_login(login_options[int(user_Input)-1]) # User input is 1-indexed (design choice) while python arrays are 0-indexed.
        if username is None: 
            continue # login is unsuccessful, restart the login screen.

        # User Menu -- after user has succesfully logged in
        while True:
            user_options = ["Start a session", "Search for songs and playlists", 
                "Search for artists", "End the session"
                ]
            user_menu(user_options, username)
            user_Input = input("Your Input : ")
            if user_Input in ['q','Q']: 
                exit_program()      # close sessions and exit
            if user_Input in ['l','L']:
                break               # log out
            """
            -- Implement user input processing here -- 

            """
            # User selects: Start Session
            if user_Input == '1':
                session = start_session(username)

            # User selects: End the session
            if user_Input == '4':
                # Ensure the user is in a current session
                if session == None:
                    print("You are not in a current session!")
                    continue
                else:
                    end_session(username, session)
                    session = None
                    
                   




if __name__ == "__main__":
    main()