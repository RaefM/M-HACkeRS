import json
import os
import requests
from bs4 import BeautifulSoup

baseUrl = "https://www.imdb.com"

def getTop100():
    with open("movieData.txt", "r+") as file:
        file.truncate()
    with open("movieData.txt", "w") as file:
        file.write("Movie Title;IMdb Code;Soundtrack(Song Name=Artists%)\n")
    topChartsUrl = baseUrl + "/chart/top/"
    page = requests.get(topChartsUrl)
    soup = BeautifulSoup(page.text, 'html.parser')
    movieList = soup.find("body").find(id="pagecontent").find("table").find("tbody").find_all("tr")
    file = open("movieData.txt", "a")
    for x in range(100):
        content = movieList[x].find_all("a")
        title = content[1].text
        code = content[1]['href']
        file.write(title + ";" + code + ";")

        songInfo = getSoundtrackData(title, code)
        for song in songInfo:
            file.write(song[0] + "=" + song[1] + "%")
        file.write("\n")

    file.close()

def getSoundtrackData(title, code):
    output = []
    soundtrackUrl = baseUrl + code + "soundtrack/"
    page = requests.get(soundtrackUrl)
    soup = BeautifulSoup(page.text, 'html.parser')
    songs = soup.find(id="soundtracks_content").find("div").find_all("div")
    for song in songs:
        asong = song.text
        songData = asong.splitlines()
        songTitle = songData[0]
        songArtists = ''.join(songData[1:])
        print(songTitle)
        print(songArtists)
        print()
        output.append([songTitle, songArtists])
    return output
        


getTop100()