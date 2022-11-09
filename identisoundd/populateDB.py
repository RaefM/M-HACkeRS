import json
import psycopg2
import string
conn = psycopg2.connect(database="identisounddb",
                        host="localhost",
                        user="chatter",
                        password="chattchatt",
                        port="")

cursor = conn.cursor()
#cursor.execute('TRUNCATE TABLE movies;')
cursor.execute('TRUNCATE ONLY movies, songs, songs_to_movies;')
cursor.execute('ALTER SEQUENCE movies_id_seq RESTART;')
cursor.execute('ALTER SEQUENCE songs_id_seq RESTART;')

with open("../MovieData/movieData.txt", "r", errors='ignore') as file:
    contents = file.readlines()

def cleanse_data(text):
    """Cleanse data by removing puncation and lowercase."""
    return text.translate(str.maketrans('','',string.punctuation)).lower()

for x in range(1, len(contents)):
    movieInfo = contents[x].split(';')
    title = movieInfo[0]
    title = title.rstrip()
    songInfo = movieInfo[2]
    songs = songInfo.split("%")
    songs = songs[:-1]
    cursor.execute("INSERT INTO movies (name) VALUES(%s) RETURNING id;", (title,))
    movieID = cursor.fetchall()[0][0]
    for song in songs:
        songName, artist = song.split("=")
        songName = songName.rstrip()
        if len(songName) == 0:
            continue
        songName = cleanse_data(songName)
        artist = artist.rstrip()
        cursor.execute("SELECT id FROM songs WHERE name=%s;", (songName,))
        foundSong = cursor.fetchall()
        if len(foundSong) == 0:
            cursor.execute("INSERT INTO songs (name, artistinfo) VALUES(%s, %s) RETURNING id;", (songName, artist,))
            songID = cursor.fetchall()[0][0]
        else:
            songID = foundSong[0][0]
        cursor.execute("INSERT INTO songs_to_movies (songid, movieid) VALUES(%s, %s);", (songID, movieID,))

cursor.execute('SELECT * FROM movies;')
rows = cursor.fetchall()
print(rows)

cursor.execute('SELECT * FROM songs;')
rows = cursor.fetchall()
print(rows)

cursor.execute('SELECT * FROM songs_to_movies;')
rows = cursor.fetchall()
print(rows)

conn.commit()
conn.close()
