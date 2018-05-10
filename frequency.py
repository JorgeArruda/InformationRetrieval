#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def frequency(listTokens, listWord, frequencyWord):
        "Vare a lista de tokens do documento, retorna a frequência. Incrementa também a frequência global"

        frequencyDocument = [0]*len(listWord)
        for token in listTokens:
            frequencyWord[ listWord.index(token) ]+=1
            frequencyDocument[ listWord.index(token) ]+=1
        
        return (frequencyDocument, frequencyWord)