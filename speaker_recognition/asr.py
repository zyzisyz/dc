#!/usr/bin/env python
# coding=utf-8

# *************************************************************************
#	> File Name: asr.py
#	> Author: Yang Zhang
#	> Mail: zyziszy@foxmail.com
#	> Created Time: Tue 02 Oct 2018 11:06:33 PM CST
# ************************************************************************/


from SpeechModel import ModelSpeech


def Get_PinYin(datapath):
    ms = ModelSpeech(datapath)
    ms.LoadModel('./Speech.model')
    r = ms.RecognizeSpeech_FromFile(datapath)
    return r


if __name__ == "__main__":
    while True:
        path = input("wavpath: ")
        if path == 'q' or path == "Q":
            break
        else:
            print(Get_PinYin(path))
