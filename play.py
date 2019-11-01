from music21 import *
import torch

def play_parse():
    a = converter.parse(r'MyInput/follow_me.mid')
    b = a.getTimeSignatures()
    print(b[0].ratioString)

if __name__ == "__main__":
    a = torch.load(r"DatasetManager/dataset_cache/datasets/ChoraleDataset([0, 1, 2, 3],bach_chorales,['fermata', 'tick', 'key'],8,4)")
    print(a)