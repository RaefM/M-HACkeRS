import requests
import json
import base64
from ratelimiter import RateLimiter

clientID = "c459297433c54d9e8c8412668d2a9c0a"
clientSecret = "ddc2b4261f604e22bb727d406074f12e"

def getOAuth():
    # request token from the spotify API to perform requests with our clientID and secret
    requestTokenEndpoint = "https://accounts.spotify.com/api/token"
    """
    Authorization
      Base 64 encoded string that contains the client ID and client secret key. 
      The field must have the format: Authorization: Basic <base64 encoded client_id:client_secret>
    Content-Type
      Set to application/x-www-form-urlencoded.
    """
    
    # auth_bytes = ("Basic " + clientID + ":" + clientSecret).encode('ascii')
    # # auth_bytes_base64 = base64.encodebytes(auth_bytes)
    # auth_bytes_base64 = base64.b64encode(auth_bytes)

    message = f"{clientID}:{clientSecret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = "Basic " + base64Bytes.decode('ascii')

    r = requests.post(requestTokenEndpoint, headers={
      "Authorization": base64Message,
      "Content-Type": "application/x-www-form-urlencoded",
    }, data = {
      "grant_type": "client_credentials"
    }, json=True)

    token_dict = r.json()
    
    return token_dict["access_token"]

@RateLimiter(max_calls=10, period=1)
def getTrackID(oathToken, songName):
    # search for tracks matching each song name (only tracks); take the first element of the 
    # items array in the tracks object, and access the uri, which containts the track id
    searchEndpoint = "https://api.spotify.com/v1/search"

    r = requests.get(
      searchEndpoint,
      params={
        "q": songName,
        "type": "track"
      },
      headers={
        "Authorization": "Bearer " + oathToken,
        "Content-Type": "application/json",
        "Accept": "application/json"
      }
    )

    if (r.status_code == 401):
        access_token = getOAuth()
        getTrackID(access_token, songName)
        
    if (len(r.json()["tracks"]["items"]) == 0):
        print(f"WARNING: {songName} not found in Spotify; omitted from training data")
        return None
    
    return r.json()["tracks"]["items"][0]["uri"].split(':')[2]

@RateLimiter(max_calls=10, period=1)
def getPitchAnalysis(oathToken, trackID):
    """
    curl --request GET
    --url https://api.spotify.com/v1/audio-analysis/id
    --header 'Authorization: '
    --header 'Content-Type: application/json'
    """

    if (trackID is None):
        return None

    # request the analysis data on the track id and extract the pitch vector
    analysisEndpoint = f"https://api.spotify.com/v1/audio-analysis/{trackID}"

    r = requests.get(
      analysisEndpoint,
      headers={
        "Authorization": "Bearer " + oathToken,
        "Content-Type": "application/json",
        "Accept": "application/json"
      }
    )

    if (r.status_code == 401):
        access_token = getOAuth()
        getPitchAnalysis(access_token, trackID)

    return r.json()["segments"]

def getSpotifyPitchData(songNames):
    oathToken = getOAuth()

    allSegments = []

    for songName in songNames:
        spotifyTrackID = getTrackID(oathToken, songName)
        allSegments.append(getPitchAnalysis(oathToken, spotifyTrackID))
        # print(getPitchVector)

    return allSegments

#Convert the song list from the database to a python list
def grabSongs():
    f = open("441_DB_Songs.json")
    data = json.load(f)
    songList = []
    for i in data['songs']:
        songList.append(i[1])
    return songList


if __name__ == "__main__":
    songList = grabSongs()
    getSpotifyPitchData(songList)