import imp
import sqlite3
import random

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
	else:
		return uid

def artist_login(aid,pwd):
	""" returns the artist's id if the login is successful, returns None if login is unsuccessful. """
	connection, cursor = connect()

	try: 
		cursor.execute("SELECT * FROM artists WHERE aid = (?) AND pwd = (?)", (aid, pwd))
	except sqlite3.Error:
		return None # unsuccesful, maybe user formating error.

	user = cursor.fetchall()
	assert len(user) in [0,1]
	if len(user) == 0:
		return None # No user with that combination of uid, pwd exists. Unsuccesful login.

	return aid # succesful login.

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
		return None 

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

def is_song(artist_id, song_title, song_duration):
	"""
	Checks if this song already exists.
	"""
	connection, cursor = connect()

	query = '''
	SELECT * FROM artists, perform, songs 
	WHERE artists.aid = perform.aid AND perform.sid = songs.sid
	AND artists.aid = (?) AND songs.title = (?) AND songs.duration = (?)
	'''

	cursor.execute(query, (artist_id, song_title, song_duration))
	songs = cursor.fetchall()
	assert len(songs) in [0,1] # should not have multiple songs with the same title and duration by project specifications.
	commit(connection)

	if len(songs) == 0:
		return False # song does not exist
	return True # song does exist

def is_playlist(pid):
	"""
	Checks if a playlist with pid already exists in the database.
	"""
	connection, cursor = connect()

	cursor.execute("SELECT * FROM playlists WHERE pid = (?)", (pid,))
	playlist = cursor.fetchall()
	assert len(playlist) in [0,1] # cannot have multiple playlists with the same pid - primary key
	commit(connection)

	if len(playlist) == 0:
		return False # playlist does not exist
	return True # playlist does exist

def insert_song(artist_id, song_title, song_duration):
	"""
	inserts song into the database assuming it already doesnt exist. 

	returns the unique song id, generated when a new song is made sid.
	"""
	connection, cursor = connect()

	cursor.execute("SELECT sid FROM songs")
	song_ids = cursor.fetchall()

	valid = True
	while valid:
		new_sid = random.randint(1, 1000)

		# If there are no songs
		if len(song_ids) == 0:
			valid = False
			break
		
		# Gather all song ids
		all_sids = []
		for sid in song_ids:
			all_sids.append(sid[0])

		# Ensure that the sid is unique
		valid = False
		if new_sid in all_sids:
			valid = True

	# Add new song with unique sid
	cursor.execute("INSERT INTO songs VALUES (?,?,?)", (new_sid, song_title, song_duration))

	# Add the song to performs table
	cursor.execute("INSERT INTO perform VALUES (?,?)", (artist_id, new_sid))
	commit(connection)

	return new_sid

def insert_artist_performs(artist_id, song_id):
	''' Adds the artist and the song they performed to the performs table.'''

	# Cannot have dangling references.
	assert(is_artist(artist_id))

	connection, cursor = connect()

	cursor.execute("INSERT INTO perform VALUES (?,?)", (artist_id, song_id))

	commit(connection)

def is_perform(artist_id, song_id):
	"""
	Checks if this song already exists.
	"""
	connection, cursor = connect()

	query = '''
	SELECT * FROM perform 
	WHERE aid = (?) AND sid = (?)
	'''
	cursor.execute(query, (artist_id, song_id))
	performs = cursor.fetchall()
	assert len(performs) in [0,1] # primary key integrity.

	commit(connection)

	if len(performs) == 0:
		return False # artist does perform this song
	return True # artist does perform this song

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
		key_words[i] = key_words[i].strip().lower()

	# Query database for matching artist names or songs

	query = ''' DROP VIEW if exists Total;'''
	cursor.execute(query)

	query =	'''	DROP VIEW if exists MadeBy;'''
	cursor.execute(query)
	
	query = '''	CREATE VIEW Total (aid, written)
					as SELECT artists.aid, COUNT(songs.sid) 
					FROM artists, songs, perform
					WHERE artists.aid = perform.aid
					AND perform.sid = songs.sid
					GROUP BY artists.aid;'''
	cursor.execute(query)

	query = '''CREATE VIEW MadeBy 
					AS SELECT artists.aid, songs.title
					FROM artists, songs, perform
					WHERE artists.aid = perform.aid
					AND perform.sid = songs.sid;'''
	cursor.execute(query)

	query = '''	SELECT DISTINCT artists.aid, name, nationality, written
				FROM artists, Total, MadeBy
				WHERE artists.aid = Total.aid
				AND artists.aid = MadeBy.aid
				AND (
				'''
	
	addition = ''
	order_by = 'ORDER BY '
	# CASE WHEN LOWER(artists.name) LIKE '%drake%' THEN 1 ELSE 0 END, CASE WHEN LOWER(MadeBy.title) LIKE '%drake%' THEN 1 ELSE 0 END, CASE WHEN LOWER(MadeBy.title) LIKE '%dance%' THEN 1 ELSE 0 END
	
	for i in range(len(key_words)):
		
		addition += "LOWER(artists.name) LIKE '%" + key_words[i] +"%' OR LOWER(MadeBY.title) LIKE '%" + key_words[i] + "%'" 
		order_by += "CASE WHEN LOWER(artists.name) LIKE '%" + key_words[i] +"%' THEN 1 ELSE 0 END, CASE WHEN LOWER(MadeBY.title) LIKE '%" + key_words[i] + "%' THEN 1 ELSE 0 END" 
		if i + 1 < len(key_words):
			addition += '''OR '''
			order_by += ''', '''
		else:
			addition += ''') '''

	addition += order_by + ''';'''
	query += addition

	cursor.execute(query)
	matches = cursor.fetchall()
	commit(connection)

	return matches
	
	
	# while True:
	# 	print(matches)

	# while True:
	# 	for word in key_words:
	# 		print(word)

def artist_songs(id):
	"""
	Obtains and returns all the songs performed by an artist
	"""
	connection, cursor = connect()

	# Obtain a list of all the songs performed by the artist
	cursor.execute("SELECT songs.sid, title, duration FROM songs, artists, perform WHERE songs.sid = perform.sid AND perform.aid = artists.aid AND artists.aid = ?", (id,))
	all_songs = cursor.fetchall()
	commit(connection)

	return all_songs

def song_info(sid):
	"""
	Prints additional song information based on the input sid
	"""
	connection, cursor = connect()

	# Gather additional information about the song
	cursor.execute("SELECT artists.name, songs.sid, title, duration FROM songs, artists, perform WHERE songs.sid = perform.sid AND perform.aid = artists.aid AND songs.sid = ?;", (int(sid),))
	song_info = cursor.fetchone()

	# Gather playlists that contain the song
	cursor.execute("SELECT playlists.title FROM playlists, plinclude WHERE playlists.pid = plinclude.pid AND plinclude.sid = ?;", (int(sid),))
	playlists = cursor.fetchall()
	commit(connection)

	return song_info, playlists

def top3_users(artist_id):
	"""
	Artist action #2
	Obtains and returns all the top 3 fans of the artist
	"""
	connection, cursor = connect()

	query = '''
			SELECT u1.name
			FROM users u1, listen l1, songs s1, perform p1, artists a1
			WHERE u1.uid = l1.uid AND l1.sid = s1.sid AND s1.sid = p1.sid AND p1.aid = a1.aid
			AND a1.aid = (?)
			GROUP BY l1.uid
			ORDER BY SUM(l1.cnt * s1.duration) DESC
			LIMIT 3

	'''

	cursor.execute(query,(artist_id,))
	top3_fans = cursor.fetchall()
	commit(connection)

	return top3_fans


def top3_playlists(artist_id):
	'''
	Artist action #2
	obtains and returns the top 3 playlist that include the largest number of the artist's songs.
	'''
	connection, cursor = connect()

	query = '''
			SELECT p1.title, u1.name
			FROM users u1, playlists p1, plinclude incl1, songs s1, perform perf1, artists a1
			WHERE u1.uid = p1.uid AND p1.pid = incl1.pid AND incl1.sid = s1.sid
			AND s1.sid = perf1.sid AND perf1.aid = a1.aid
			AND a1.aid = (?)
			GROUP BY p1.pid
			ORDER BY COUNT(s1.sid) DESC
			LIMIT 3

	'''

	cursor.execute(query,(artist_id,))
	top3_playlists = cursor.fetchall()
	commit(connection)

	return top3_playlists


	cursor.execute(query,(artist_id,))
	top3_fans = cursor.fetchall()
	commit(connection)

	return top3_fans

def song_listen(uid, sid):
	"""
	"""
	pass

def create_playlist(title, uid, first_song):
	"""
	creates playlist row and plinclude row with the given title, uid, first song
	"""

	new_pid = random.randint(1, 1000)
	while is_playlist(new_pid):
		new_pid = random.randint(1, 1000)
	
	connection, cursor = connect()

	playlist_query = '''INSERT INTO playlists VALUES (?, ?, ?);'''
	try:
		cursor.execute(playlist_query, (new_pid, title, uid,))
	except sqlite3.Error:
		return None 

	plinclude_query = '''INSERT INTO plinclude VALUES (?, ?, ?);'''
	try:
		cursor.execute(plinclude_query, (new_pid, first_song, 0,))
	except sqlite3.Error:
		return None 

	commit(connection)

	return new_pid

def get_playlists(uid):
	"""
	Gets the title of all playlist belong to the given uid.
	"""
	connection, cursor = connect()

	query = '''SELECT title, pid FROM playlists WHERE uid = ?;'''
	cursor.execute(query, (uid,))
	playlists = cursor.fetchall()
	commit(connection)

	return playlists

def add_to_playlist(pid, sid):
	"""
	Adds song to playlist (aka adds a row to plinclude table) with given playlist and song id
	"""
	
	connection, cursor = connect()

	max_order_query = '''SELECT MAX(sorder) FROM plinclude WHERE pid = ?''' 
	cursor.execute(max_order_query, (pid,))
	max = cursor.fetchone()

	plinclude_query = '''INSERT INTO plinclude VALUES (?, ?, ?);'''
	try:
		cursor.execute(plinclude_query, (pid, sid, (max[0]+1),))
	except sqlite3.Error:
		return None 

	commit(connection)