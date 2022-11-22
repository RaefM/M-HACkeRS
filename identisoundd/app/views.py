from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import json
import string
import uuid
import pathlib
import base64

from django.core.files.storage import FileSystemStorage

def cleanse_data(text):
    """Cleanse data by removing puncation and lowercase."""
    return text.translate(str.maketrans('','',string.punctuation)).lower()

def getmovies(request):
    if request.method != 'GET':
        return HttpResponse(status=404)

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM movies;')
    rows = cursor.fetchall()

    response = {}
    response['songs'] = rows
    return JsonResponse(response)

@csrf_exempt
def getsongs(request):
    if request.method != 'POST':
        return HttpResponse(status=404)

    json_data = json.loads(request.body)
    songName = json_data['songName']

    songName = cleanse_data(songName)
    
    cursor = connection.cursor()

    cursor.execute('SELECT s.id FROM songs s WHERE s.name =(%s);', (songName,))
    queryResp = cursor.fetchall()
    

    if(len(queryResp) == 0):
        return JsonResponse({"error":"song with name not found"})
    
    songId = queryResp[0][0]
    
    cursor.execute(
            "SELECT m.name, m.year, m.director, m.posterurl " +
            "FROM songs_to_movies sm " +
            "JOIN movies m ON sm.movieid = m.id " +
            "WHERE sm.songid = '%s';"
            , (songId,))  
    movieInfo = cursor.fetchall()
    if(len(movieInfo) == 0):
        return JsonResponse({"error":"No movies associated with song"})

    movieIDs = {}
    movieIDs['movies'] = movieInfo

    return JsonResponse(movieIDs)

@csrf_exempt
def postAudio(request):
    if request.method != 'POST':
        return HttpResponse(status=404)

    fileName = "./static/audiofiles/"+request.POST.get("fileName")

    if request.POST.get("file"):
        b64content = request.POST.get('file')
        content = base64.b64decode(b64content)

        fs = FileSystemStorage()
        filename = fs.save(fileName, content)
        fileurl = fs.url(filename)
    else:
        fileurl = None

    return JsonResponse({"status":"200", "fileurl":fileurl})


