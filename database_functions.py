from audioop import add
import imp
import sqlite3
import random
from urllib.response import addinfo

def connect():
	# connects to the sqlite database
	database_name = "./tables.db"
	connection = sqlite3.connect(database_name)
	cursor = connection.cursor()
	return connection, cursor

def commit(connection):
	connection.commit()
	connection.close()

def close_all_sessions(): 
	pass # TODO : close sessions by setting all NULL values in sessions.end to current date/time

def user_login(uid,pwd):
	""" returns user if succesful login, None if unsuccessful. """
	connection, cursor = connect()

	try: 
		cursor.execute("SELECT * FROM users WHERE uid = (?) AND pwd = (?)", (uid, pwd))
	except sqlite3.Error:
		return None # unsuccesful, maybe user formating error.

	user = cursor.fetchall()
	assert len(user) in [0,1]
	if len(user) == 0:
		return None # No user with that combination of uid, pwd exists. Unsuccesful login.

	return uid # succesful login.

def register_user(uid, name, password):
	"""
	registers user only if uid is not in the users database already
	returns the uid of user if its successful
	"""

	connection, cursor = connect()
	if is_user(uid):
		return None # user already exists

	try:
		cursor.execute("INSERT INTO users VALUES (?,?,?)", (uid, name, password))
	except sqlite3.Error:
		return None # misformatted, uid should be 4 characters.

	commit(connection)
	return uid


def is_user(uid):
	"""
	Checks if a user with uid already exists in the database.
	"""
	connection, cursor = connect()

	cursor.execute("SELECT * FROM users WHERE uid = (?)", (uid,))
	user = cursor.fetchall()
	assert len(user) in [0,1] # cannot have multiple users with the same uid - primary key
	commit(connection)

	if len(user) == 0:
		return False # user does not exist
	return True # user does exist

def is_artist(aid):
	"""
	Checks if a artist with aid already exists in the database.
	"""
	connection, cursor = connect()

	cursor.execute("SELECT * FROM artists WHERE aid = (?)", (aid,))
	artist = cursor.fetchall()
	assert len(artist) in [0,1] # cannot have multiple artists with the same aid - primary key
	commit(connection)

	if len(artist) == 0:
		return False # artist does not exist
	return True # artist does exist

def start_session(uid):
	"""
	Generates random session number for the user
	Ensure that the generates session number does not exist
	"""
	connection, cursor = connect()

	cursor.execute("SELECT sno FROM sessions WHERE uid = ?", (uid,))
	user_sessions = cursor.fetchall()

	valid = True
	while valid:
		new_session = random.randint(1, 1000)

		# If this is a new user
		if len(user_sessions) == 0:
			valid = False
			break
		
		# Gather all user session
		all_sessions = []
		for session in user_sessions:
			all_sessions.append(session[0])

		# Esnure that the sesion number is unique
		valid = False
		if new_session in all_sessions:
			valid = True
		
	# Add new session value
	query = '''INSERT INTO sessions VALUES (?, ?, date(), NULL);'''
	cursor.execute(query, (uid, new_session,))
	commit(connection)
	return new_session

def end_session(uid, sno):
	"""
	End session sno for specified user uid
	Update the end date/time
	"""
	connection, cursor = connect()

	query = '''UPDATE sessions SET end = date() WHERE uid = ? AND sno = ?;'''
	cursor.execute(query, (uid, sno,))
	commit(connection)

def artist_search(key_words_string):
	"""
	Obtain a list of keywords
	These keys will be examined alongside artist names and songs
	"""
	connection, cursor = connect()

	# Convert string to a list
	key_words = key_words_string.split(',')

	# Data processing - ensure there are no uncessary white spaces
	for i in range(len(key_words)):
		key_words[i] = key_words[i].strip()

	# Query database for matching artist names or songs

	# query = ''' WITH Total(aid, written) 
	# 				as SELECT (artists.aid, COUNT(songs.sid)) 
	# 				FROM artists, songs, perform
	# 				WHERE artists.aid = perform.aid
	# 				AND perform.sid = songs.sid
	# 				GROUP BY artists.aid
	# 			WITH MadeBy(aid, title)
	# 				AS SELECT (artists.aid, songs.title)
	# 				FROM artists, songs, perform
	# 				WHERE artists.aid = perform.aid
	# 				AND perform.sid = songs.sid
	# 			SELECT artists.aid, name, nationality, written
	# 			FROM artists, Total, MadeBy
	# 			WHERE artists.aid = Total.aid
	# 			AND artists.aid = MadeBy.aid
	# 			AND (
	# 			'''
	# addition = ''
	# for i in range(len(key_words)):
	# 	addition += "artists.name LIKE '%" + key_words[i] +"%' OR MadeBY.title LIKE '%" + key_words[i] + "%'" 
	# 	if i + 1 < len(key_words):
	# 		addition += '''OR '''
	# 	else:
	# 		addition += ''');'''

	# query += addition

	query = '''SELECT artists.aid, COUNT(songs.sid)
					FROM artists, songs, perform
					WHERE artists.aid = perform.aid
					AND perform.sid = songs.sid'''
	addition = " AND artists.name LIKE '%" + key_words[0] + "%';" 
				
	query += addition				
	cursor.execute(query)
	matches = cursor.fetchall()
	commit(connection)
	print(matches)

	# while True:
	# 	for word in key_words:
	# 		print(word)