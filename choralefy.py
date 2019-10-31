from music21 import *

import math

def generate_empty_part(input_melody):
    p = stream.Part()
    intPart = int(input_melody.duration.quarterLength)
    fracPart = input_melody.duration.quarterLength - intPart
    for i in range(intPart):
        r = note.Rest()
        p.insert(i, r)
    if (fracPart > 1e-6):
        r = note.Rest(quarterLength=fracPart)
        p.insert(intPart, r)
    return p

def choralefy(input_midi):
    input_melody = converter.parse(input_midi)
    num_parts_to_append = 4 - input_melody.parts.elementsLength
    for i in range(num_parts_to_append):
        p = generate_empty_part(input_melody)
        input_melody.insert(p)
    return input_melody
    
if __name__ == "__main__":
    a = choralefy('MyInput/follow_me.mid')
    a.show()