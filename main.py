"""     
Mini-Project 1

"""

# Import modules
#from curses.ascii import isdigit
#from curses.ascii import isdigit
from http.client import TOO_MANY_REQUESTS
from pickle import TRUE
from pydoc import isdata
from turtle import pos, position
from database_functions import *
from getpass import *
import sys
import os
DEBUG = True
session = None

def clear():
    '''
    Clears the terminal screen and scroll back to present
    the user with a nice clean, new screen. 
    '''
    os.system('cls||echo -e \\\\033c')

def exit_program():
    # close all sessions then exit the program.
    close_all_sessions() 
    exit()

def print_login_menu(login_options, output):
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
    if output is not None:
        print(output)
    print("--------------------------------------")

def print_user_menu(user_options, user = None, output = None):
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
    if output is not None:
        print(output)
    print("--------------------------------------")

def safe_input(user_Input, options):
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
        if username.strip() == "" or pwd.strip() == "":
            return None, None # cannot be empty string 

        if is_user(username) and is_artist(username): # username is stored in both the users and artists table
            choice = input("\nInput \'1\' to log in as a user, or Input \'2\' to log in as an artist.\n\nYour Input : ")
            if not safe_input(choice, [1,2]):
                return None, None # invalid input
            if choice == '1':
                username = user_login(username, pwd)
                return "User", username
            else:
                username = artist_login(username, pwd)
                return "Artist", username

        if is_user(username):
            return "User", user_login(username, pwd)
        if is_artist(username):
            return "Artist", artist_login(username, pwd)
        return None, None # user does not exist in either table.

    elif option == "Register User":
        username = input("\nInput your Username (4 characters): ")
        name = input("\nInput your Name: ")
        pwd = getpass(prompt='\nInput your password: ') 
        username = register_user(username, name, pwd) # returns None if unsuccessful. i.e., user with that uid already exists.    
        return "User", username 

def song_actions(songs, uid):
    """
    """

    global session
    valid = True
    
    for i in range(len(songs)):
        position = "---" + str(i + 1) + "---\n"
        details = "Song ID: " + str(songs[i][0]) + "\nTitle: " + songs[i][1] + "\nDuration: " +  str(songs[i][2]) + "\n"
        print(position + details)

    # Display user options
    while valid:
        print("------------------------------------")
        print("Type \'b\' to return to user options.")
        print("Enter the postion of the song, followed by a comma, then one of the following options:")
        print("Type \'#, listen\' to listen to the song.")
        print("Type \'#, info\' to obtain more information about the song.")
        print("Or Type \'#, playlist\' to add the song to one of your playlists.")

        # Input processing
        response = input(">>>")
        option = response.split(',')
        for i in range(len(option)):
            option[i] = option[i].strip()
            if option[i].isalpha():
                option[i] = option[i].lower()

        # Options for songs actions
        if option[0] == 'b':
            valid = False
            return
        elif option[0].isdigit() == False:
            print("Please enter a valid song number.")
        elif int(option[0]) <= 0 or int(option[0]) > len(songs):
            print("Song number out of range, please try again.")
        elif option[1] == 'listen':
            if session == None:
                session = start_session(uid)
                print("\n Session Started!\n")

            num_listens = listened_before(uid, session, songs[int(option[0]) - 1][0])
            if (len(num_listens) == 0):
                add_song_listen(uid, session, songs[int(option[0]) - 1][0])
            else:
                increment_song_listen(uid, session, songs[int(option[0]) - 1][0], num_listens[0][0])
            
        elif option[1] == 'info':
            # Obtain the desired results
            info, playlist = song_info(songs[int(option[0]) - 1][0])
            info_print = "\nArtist: " + info[0] + "\nSong ID: " + str(info[1]) + "\nTitle: " + info[2] + "\nDuration: " + str(info[3]) + "\nPlaylists: "
            playlist_print = ""
            if playlist != []:
                for i in range(len(playlist)):
                    playlist_print += playlist[i][0]
                    if i + 1 < len(playlist):
                        playlist_print += ", "
            else:
                playlist_print = "N/A"
            info_print += playlist_print
            print(info_print)
        elif option[i] == 'playlist':
            print("\nExisting Playlists:\n")
            playlists = get_playlists(uid)
            for i in range(len(playlists)):
                print(str(playlists[i][1]) + " | " + playlists[i][0])

            pl_input = input("Enter a playlist id to add to or type 'new' to create a new playlist.")
            goodInput = False
            while goodInput != True:
                if (pl_input == 'new'):
                    title = input("Enter a playlist title: ")
                    create_playlist(title, uid, songs[int(option[0]) - 1][0])
                    goodInput = True
                else:
                    if is_playlist(pl_input):
                        add_to_playlist(pl_input, (songs[int(option[0]) - 1][0]))
                        print("Song added!")
                        goodInput = True
        else:
            print("Invalid option")
        

def main():

    user_msg = None
    global session

    # Log in menu
    while True:

        # Display the login screen
        login_options = ["User/Artist login", "Register User"]
        print_login_menu(login_options, user_msg)
        user_msg = None

        # Process user input
        user_Input = input(" Your Input: ") 
        if user_Input in ['q','Q']: 
            exit_program()  # close sessions and exit

        # Checks if input is valid.
        if not safe_input(user_Input, login_options): 
            user_msg = "\n Invalid input, try again!"
            continue    # restart the login screen     

        # Process user/artist login
        login_type = None # either 'user' or 'artist'
        username = None
        session = None
        login_type, username = process_login(login_options[int(user_Input)-1]) # User input is 1-indexed (design choice) while python arrays are 0-indexed.
        
        if username is None: 

            user_msg = "\n Invalid username or password, try again!"
            continue    # restart the login screen.
        

        # if a valid username/password is entered, we begin the corresponding artist or user menu.
        if login_type == "Artist":

            # Artist Menu 
            while True:

                # Printing out artist menu
                artist_options = ["Add a song", "Find top fans and playlists"]
                print_user_menu(artist_options, username, user_msg)
                user_msg = None 

                # 
                user_Input = input("Your Input : ")
                if user_Input in ['q','Q']: 
                    exit_program()      # close sessions and exit
                if user_Input in ['l','L']:
                    break               # log out
                if not safe_input(user_Input, artist_options): # Checks if input is valid.
                    user_msg = "\n Not a valid Input!"
                    continue            # return to start of user menu

                # Artist selects : Add a song
                if user_Input == '1':

                    song_title = input("\nInput the song title: ")
                    song_duration = input("\nInput the song duration: ") 
                    if not song_duration.isdigit(): # stored as an integer in the database
                        user_msg = "\n The song duration must be an integer!"
                        continue

                    song_duration = int(song_duration)
                    if is_song(username, song_title, song_duration): 
                        # artist already has this song. 
                        user_msg = "\n Artist already has a song with this title and duration!"
                        continue 
                    else:
                        # is a unique song. Can insert.
                        sid = insert_song(username, song_title, song_duration)

                        # asking from input for additional artists
                        user_msg = None
                        while user_Input not in ['q', 'Q']:
                            
                            clear()
                            print("--------------------------------------")
                            print("Song Name :", song_title)
                            print("Song Duration :", song_duration)
                            print("\nInput the id of any additional artist that performed the song!")
                            print("Enter 'q' to exit!")
                            if user_msg is not None:
                                print(user_msg)
                            print("--------------------------------------")
                            user_Input = input('\nYour Input : ')

                            
                            if user_Input == '' or len(user_Input) > 4:
                                user_msg = '\nInvalid artist id. id must be a non-empty string with length <= 4. Try again!'
                                continue

                            if is_artist(user_Input):
                                if is_perform(user_Input, sid):
                                    # artist already performs this song
                                    user_msg = '\nThis artist already performs this song!'
                                else:
                                    insert_artist_performs(user_Input, sid) 
                                    user_msg = '\n'+ user_Input + " now performs this song!"

                            else:
                                user_msg = '\nThis is not a valid artist id. Try again!'

                        user_msg = "\n Song inserted!"

                # Artist selects : Find top fans and playlists
                if user_Input == '2':
                    top_fans = top3_users(username) # top 3 fans of the artist that is logged in.
                    top_playlists = top3_playlists(username) 

                    user_msg = "\n Your top 3 fans are: "

                    for i in range(len(top_fans)):
                        user_msg += "\n "
                        user_msg += str(3-i) + ": " + top_fans[i][0]

                    user_msg += "\n\n Your top 3 playlists are: "

                    for i in range(len(top_playlists)):
                        user_msg += "\n " + str(3-i) + ": "
                        user_msg += top_playlists[i][0] + " Made by, " + top_playlists[i][1] 

                    

        elif login_type == "User":
            # User Menu 
            while True:
                user_options = ["Start a session", "Search for songs and playlists", 
                    "Search for artists", "End the session"
                    ]

                print_user_menu(user_options, username, user_msg)
                user_msg = None

                user_Input = input("Your Input : ")
                if user_Input in ['q','Q']: 
                    exit_program()      # close sessions and exit
                if user_Input in ['l','L']:
                    break               # log out
                if not safe_input(user_Input, user_options): # Checks if input is valid.
                    user_msg = "\n Not a valid Input!"
                    continue            # return to start of user menu

                # User selects: Start Session
                if user_Input == '1':
                    session = start_session(username)
                    user_msg = "\n Session Started!"

                # User selects: Search for songs and playlists
                if user_Input == '2':
                    print("Please enter a list of keywords. \n These keywords will be used to find matching song and playlist titles.")
                    print("Please separate your keywords by a comma ','")
                    key_words = input(">>>")
                    matches = song_playlist_search(key_words)
                    while True:
                        print(matches)

                # User selects: Search for Artists
                if user_Input == '3':
                    print("Please enter a list of keywords. \n These keywords will be used to find matching artists name or \n songs perfromed by that artist.")
                    print("Please separate your keywords by a comma ','")
                    key_words = input(">>>")
                    matches = artist_search(key_words)

                    # Display results on sections of 5
                    start = 0
                    end = 5
                    valid = True
                    while valid:
                        for i in range(start, end):
                            if i < len(matches):
                                position = "---" + str(i + 1) + "---\n"
                                details = "ID: " + matches[i][0] + "\nName: " + matches[i][1] + "\nNationality: " +  matches[i][2] + "\nNumber of Songs: "
                                if matches[i][3] == None:
                                    details += "None\n"
                                else:
                                    details += str(matches[i][3]) + "\n"
                                print(position + details)

                        print("------------------------------------")
                        print("Type \'n\' to display the next page of songs.")
                        print("Select a number to display all the artist's songs")
                        print("Or ype \'q\' to quit.")

                        option = input(">>>")

                        if option.lower() == 'n':
                            if end < len(matches):
                                start += 5
                                end += 5
                            else:
                                print("All results have been displayed!")
                        elif option.isdigit() and int(option) >= 1 and int(option) <= len(matches):
                            songs = artist_songs(matches[int(option) - 1][0])
                            song_actions(songs, username)
                        elif option.lower() == 'q':
                            valid = False
                            break
                        else:
                            print("Invalid Option")
                    
                # User selects: End the session
                if user_Input == '4':
                    # Ensure the user is in a current session
                    if session == None:
                        user_msg = "\n You are not in a current session!"
                    else:
                        end_session(username, session)
                        user_msg = "\n Session Ended!"
                        session = None
                        
                   




if __name__ == "__main__":
    main()