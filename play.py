from music21 import *

if __name__ == "__main__":
    a = converter.parse(r'MyInput/follow_me.mid')
    b = a.getTimeSignatures()
    print(b[0].ratioString)