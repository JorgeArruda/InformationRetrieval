#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Termo(object):
    def __init__(self):
        self.word = ''
        self.frequency = 0
        self.tf = 0.0
        self.idf = 0.0
        self.tfIdf = 0.0
        self.maiorFrequency = 0

    def incFrequency(self):
        self.frequency += 1
        if self.frequency > self.maiorFrequency:
            self.maiorFrequency = self.frequency


class TermoColecao(object):
    def __init__(self, word, idf):
        self.word = word
        self.idf = idf
