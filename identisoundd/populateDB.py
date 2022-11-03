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

for x in range(65, 68):
    print(contents[x])
    movieInfo = contents[x].split(';')
    title = movieInfo[0]
    title = title.rstrip()
    songInfo = movieInfo[2]
    songs = songInfo.split("%")
    songs = songs[:-1]
    cursor.execute("INSERT INTO movies (name) VALUES(%s) RETURNING id;", (title,))
    movieID = cursor.fetchall()[0][0]
    for song in songs:
        songName, artist = song.split("$") #Ty Dolla $ign messes this up 
        print(songName) 
        songName = songName.rstrip()
        if len(songName) == 0:
            continue
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
