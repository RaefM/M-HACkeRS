from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from sklearn.preprocessing import StandardScaler
from sklearn.kernel_approximation import Nystroem
import pickle
import numpy as np
import json
import string
import uuid
import pathlib
import base64
import librosa
import wave
import os
import uuid
import datetime


from django.core.files.storage import FileSystemStorage
from io import StringIO

def cleanse_data(text):
    """Cleanse data by removing puncation and lowercase."""
    return text.translate(str.maketrans('','',string.punctuation)).lower()

def openJSON(fname):
    f = open(fname)
    return json.load(f)

def relativePathToAbsolute(path):
    module_dir = os.path.dirname(__file__)  # get current directory
    return os.path.join(module_dir, path)


def extract_training_data():
    labeledJson = openJSON(relativePathToAbsolute("normalizedPitchVectors.json"))

    xTrain = []
    yTrue = []

    for songName in labeledJson:
        for pitchVector in labeledJson[songName]:
            xTrain.append(pitchVector)
            yTrue.append(songName)

    return np.array(xTrain), np.array(yTrue)


def audio_file_to_pitch_vector(audioFileName, log):
    # pcm to wav
    with open(audioFileName, 'rb') as pcmfile:
        pcmdata = pcmfile.read()
        log.write("\tSAMPLE OF RECEIVED PCM CONTENT: " + str(pcmdata)[0:100] + '\n')

    with wave.open(audioFileName+'.wav', 'wb') as wavfile:
        # mono audio with a 48000 Hz sampling rate
        wavfile.setparams((1, 2, 48000, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcmdata)
    
    # load wav into time series
    time_series, sr = librosa.load(audioFileName+'.wav', sr=48000)

    # delete files
    fs = FileSystemStorage()
    fs.delete(audioFileName)
    fs.delete(audioFileName+'.wav')

    # convert time series to 12 chroma vector of pitch
    chroma =  librosa.feature.chroma_stft(y=time_series, sr=sr)
    return np.average(a=chroma, axis=1)

def normalize_vector(pitchVector, logFile):
    # Read in the data to instatiate the normalizer and the Nystroem random RBF feature mapping 
    # using the predetermined seed and hyperparameter values
    X, y = extract_training_data()

    # Normalize it
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X=X, y=y)

    twoDimPitchVec = np.array([list(pitchVector)])

    normalizedPitchVector = scaler.transform(twoDimPitchVec)

    logFile.write("\tNORMALIZED LINEAR PITCH VECTOR: " + str(normalizedPitchVector) + '\n')

    # Convert it using the RBFSampler projection stuff
    feature_map_nystroem = Nystroem(gamma=0.1, random_state=1, n_components=100)
    X_new = feature_map_nystroem.fit_transform(X=X, y=y)

    logFile.write("\tSAMPLE POINT FROM UNNORMALIZED TRAIN SET: " + str(X[0]) + '\n')
    logFile.write("\tSAMPLE POINT FROM NORMALIZED TRAIN SET: " + str(X_scaled[0]) + '\n')
    logFile.write("\tSAMPLE POINT FROM NYSTROEM TRAIN SET: " + str(X_new[0]) + '\n')

    return feature_map_nystroem.transform(normalizedPitchVector)


def predict(normalizedPitchVector):
    pickled_model = pickle.load(open(relativePathToAbsolute('modelRbfL2.pkl'), 'rb'))
    return pickled_model.predict(normalizedPitchVector)


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

    # json_data = json.loads(request.body)

    # fileName = "./static/audiofiles/"+str(uuid.uuid4())
    logFileName = "./static/logs/systemlog.txt"

    # b64content = json_data['file']
    # decodedStringContent = base64.b64decode(b64content).decode('utf-8')
    # content = StringIO(decodedStringContent)

    # content = StringIO(decodedStringContent)

    # fs = FileSystemStorage()
    # serverFilename = fs.save(fileName, content)

    if request.FILES.get("audio"):
        content = request.FILES['audio']
        filename = 'audio'+str(datetime.datetime.now())+".pcm"
        fs = FileSystemStorage()
        serverFileName = fs.save(filename, content)

        with open(logFileName, 'a+') as log:
            now = datetime.datetime.now()
            log.write("@NEW REQUEST " + str(now) + ": " + str(request) + '\n')
            pitchVector = audio_file_to_pitch_vector(serverFileName, log)
            log.write("\tGENERATED UNNORMALIZED CHROMA VECTOR OF PITCHES: " + str(pitchVector) + '\n')
            normalizedPitchVector = normalize_vector(pitchVector, log)
            log.write("\tNORMALIZED NYSTROEM RBF PITCH VECTOR: " + str(normalizedPitchVector) + '\n')
            prediction = predict(normalizedPitchVector)[0]
            log.write("\PREDICTION: " + str(prediction) + '\n')
            log.write('\n\n')
    
    # pitchVector = audio_file_to_pitch_vector(serverFilename)
    # normalizedPitchVector = normalize_vector(pitchVector)
    # prediction = predict(normalizedPitchVector)[0]

    return JsonResponse({"status":"200", "songName":prediction})
