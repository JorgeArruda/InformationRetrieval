#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Termo(object):
    def __init__(self):
        self.word = ''
        self.frequency = 0
        self.tf = 0.0
        self.idf = 0.0
        self.tfIdf = 0.0


class TermoColecao(object):
    def __init__(self, word, idf):
        self.word = word
        self.idf = idf
