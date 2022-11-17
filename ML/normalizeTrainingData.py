import numpy
import json
import math
"""
1. convert vectors associated with any time range to vectors in a 10 second time range

W. 
X. Disjoint 10 second time slice pitch vectors
Y. Do a pass on the previous set and make intermediate vectors that share half with each neighbor
Z. A pitch vector for every 10 second time slice from each song; Each pitch vector will overlap with another for 5 seconds
"""

def run_it_all(songs):
  normalizedData = {}
  songNumber = 1
  for songName, songData in songs.items():
    if songData is None:
      continue

    endOfSong = songData[-1]["start"] + songData[-1]["duration"]

    print(f"Song: {songName}, Number: {songNumber}")
    # Get the end time of the last segment padded to be divisible by 10
    #paddedEnd = int(endOfSong // 10)

    # get a vector of the start times for each time slice
    ranges = range(0, math.ceil(endOfSong), 10)

    # A vector of the time slices we want, each of length 10 seconds
    timeSlices = []
    for rangeI in ranges:
      timeSlices.append([rangeI, rangeI + 10])

    # initialize a running average of every time slice's pitch data at 0
    pitchAveragesOfTimeSlices = numpy.zeros((len(timeSlices), 12))

    currPitchVectorIndex = 0
    timeSliceIndex = 0

    
    # so long as not every time slice has been assessed
    while timeSliceIndex < len(timeSlices) and currPitchVectorIndex < len(songData):
      # get the data associated with the current pitch vector
      #print(currPitchVectorIndex)
      currPitchVector = songData[currPitchVectorIndex]
      currPitchVectorBeginning = currPitchVector["start"]
      currPitchVectorEnd = currPitchVectorBeginning + currPitchVector["duration"]

      # calculate the weight of the pitch vector based on how much of it is in the time slice
      lowerBoundOfPitchVec = max(timeSlices[timeSliceIndex][0], currPitchVectorBeginning)
      upperBoundOfPitchVec = min(timeSlices[timeSliceIndex][1], currPitchVectorEnd)
      weightOfPitchVec = (upperBoundOfPitchVec - lowerBoundOfPitchVec) / 10
      
      # avg += wi * pi
      # update the average by adding the pitch vector weighted by the amount of it contained in the time slice
      pitchAveragesOfTimeSlices[timeSliceIndex] += weightOfPitchVec * numpy.asarray(songData[currPitchVectorIndex]["pitches"])

      # if the current pitch vector crosses the end of the time slice, go to the next time slice and complete the current one's average
      if (currPitchVectorEnd > timeSlices[timeSliceIndex][1]):
        timeSliceIndex += 1
      # otherwise, evaluate the next pitch vector to continue calculating this slice's average
      else:
        currPitchVectorIndex += 1

    normalizedData[songName] = pitchAveragesOfTimeSlices.tolist()
    
    songNumber += 1

  return normalizedData  

def writeJSON(normalizedData):
  json_object = json.dumps(normalizedData, indent=4)
  with open("normalizedPitchVectors.json", "w") as outfile:
      outfile.write(json_object)

def openJSON():
  f = open("pitchVectors.json")
  return json.load(f)

def debuggingRunner(pitchVectors):
  i = 1
  #print(len(pitchVectors.items()))
  for songName, songData in pitchVectors.items():
    if i == 7:
      #print(songName)
      #print(songData)
      #print(songData[-1]["start"])
      #print(songData[-1]["duration"])
      #print(songData[-1]["start"] + songData[-1]["duration"])
      break
    i += 1

if __name__ == "__main__":
  pitchVectors = openJSON()
  #debuggingRunner(pitchVectors)
  normalizedPitchVectors = run_it_all(pitchVectors)
  writeJSON(normalizedPitchVectors)