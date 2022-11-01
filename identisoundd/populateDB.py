import json
import psycopg2

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

with open("../movieData.txt", "r") as file:
    contents = file.readlines()

for x in range(1, 4):
    movieInfo = contents[x].split(';')
    title = movieInfo[0]
    title = title.rstrip()
    songInfo = movieInfo[2]
    songs = songInfo.split("%")
    songs = songs[:-1]
    cursor.execute("INSERT INTO movies (name) VALUES(%s);", (title,))
    for song in songs:
        songName, artist = song.split("$") 
        songName = songName.rstrip()
        artist = artist.rstrip()
        cursor.execute("INSERT INTO songs (name, artistinfo) VALUES(%s, %s);", (songName, artist,))

cursor.execute('SELECT * FROM movies;')
rows = cursor.fetchall()
print(rows)

cursor.execute('SELECT * FROM songs;')
rows = cursor.fetchall()
print(rows)
