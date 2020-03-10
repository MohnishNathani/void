import pyaudio
import wave
import os
import pickle
import time
from scipy.io.wavfile import read
from IPython.display import Audio, display, clear_output

from main_functions import *

def recognize():
    # Voice Authentication
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 10
    FILENAME = "./test.wav"


    modelpath = "./gmm_models/"

    gmm_files = [os.path.join(modelpath,fname) for fname in
                os.listdir(modelpath) if fname.endswith('.gmm')]

    models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]

    speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname
                in gmm_files]

    if len(models) == 0:
        print("No Users in the Database!")
        return

    #read test file
    sr,audio = read(FILENAME)

    # extract mfcc features
    vector = extract_features(audio,sr)
    log_likelihood = np.zeros(len(models))
    diff=np.zeros(len(models))
    #checking with each model one by one
    for i in range(len(models)):
        gmm = models[i]
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()
        print("Score for ",speakers[i]," is:",log_likelihood[i])

    pred = np.argmax(log_likelihood)
    identity = speakers[pred]
    print(log_likelihood[pred])
    count=0
    for i in range(len(models)):
        diff[i]=log_likelihood[pred]-log_likelihood[i]
        if diff[i]>0.75:
            count=count+1
    print(diff)
    print(count)
    # if voice not recognized than terminate the process
    if identity == 'unknown' or identity == 'unknown2' or identity == 'unknown3' or identity == 'unknown4' or identity == 'unknown5':
            print("Not Recognized! Try again...")
            return "Not identified"
    else:
        if count==len(models)-1:
            print( "Recognized as - ", identity)
            return identity
        else:
            print( "Not recognised try again")
            return "Not Identified"

if __name__ == '__main__':
    recognize()
