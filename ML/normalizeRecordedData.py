import sys
import librosa
import numpy
import audioread
import soundfile as sf
'''
1. Grab audio file
2. Convert to librosa wave format (https://librosa.org/doc/main/generated/librosa.load.html)
3. Call librosa.chroma_stft (https://librosa.org/doc/main/generated/librosa.feature.chroma_stft.html) to convert to pitch vec
4. find average value over entire returned stft and return it as a 12d vector


TODO:
Get a test PCM file from the front end

'''

'''
INPUTS: Audio file path
RETURNS: A librosa floating point time series and sampling rate
'''
def read_and_convert_audio(audioPath):
    # Assumes that spotify audio analysis was done in mono; this is true if the track obj returned by the analysis endpoint contains
    # analysis_channels: 1
    # filename = librosa.util.example_audio_file()

    # pcm version
    # data, samplerate = sf.read(audioPath, dtype='float32')
    # data = data.T
    # return librosa.resample(data, samplerate, 48000)

    # mp3 version
    with audioread.audio_open(audioPath) as f:
      return librosa.load(path=f, sr=48000, duration=10, mono=True, )

def generate_avg_chroma(y, sr):
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    return numpy.average(a=chroma, axis=1)

if __name__ == "__main__":
    # if len(sys.argv) > 1:
    #     audioFilePath = sys.argv[1]
    # else:
    #     print("No file path given")
    #     exit()
    y, sr = read_and_convert_audio("test1.mp3")
    print(generate_avg_chroma(y, sr))

