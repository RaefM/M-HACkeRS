import json
import os
import requests
from bs4 import BeautifulSoup

baseUrl = "https://www.imdb.com"

def getTop100():
    with open("movieData.txt", "r+") as file:
        file.truncate()
    with open("movieData.txt", "w") as file:
        file.write("Movie Title;IMdb Code;Soundtrack(Song Name=Artists%);Release Year;Director;Poster Url\n")
    topChartsUrl = baseUrl + "/chart/top/"
    page = requests.get(topChartsUrl)
    soup = BeautifulSoup(page.text, 'html.parser')
    movieList = soup.find("body").find(id="pagecontent").find("table").find("tbody").find_all("tr")
    file = open("movieData.txt", "a")
    for x in range(100):
        content = movieList[x].find_all("a")
        title = content[1].text
        code = content[1]['href']
        print(title)
        file.write(title + ";" + code + ";")

        songInfo = getSoundtrackData(code)
        for song in songInfo:
            file.write(song[0] + "=" + song[1] + "%")

        movieInfo = getMovieInfo(code)
        for item in movieInfo:
            file.write(";" + item)
        file.write("\n")

    file.close()

def getMovieInfo(code):
    output = []
    movieURL = baseUrl + code
    page = requests.get(movieURL)
    soup = BeautifulSoup(page.text, 'html.parser')

    releaseYear = soup.find('ul', {'data-testid': 'hero-title-block__metadata'}).find("li").find("a")
    output.append(releaseYear.text)

    director = soup.find('div', {'data-testid': 'title-pc-wide-screen'}).find("li").find("a")
    output.append(director.text)

    poster = soup.find('div', {'data-testid': 'hero-media__poster'}).find("img")
    output.append(poster["src"])

    return output

def getSoundtrackData(code):
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
        output.append([songTitle, songArtists])
    return output
        
getTop100()