#!/usr/bin/env python3
# -*- coding: utf-8 -*-
try:
    from .frequency import term_frequency as tf_class
    from .frequency import inverse_frequency as idf_class
    from .frequency import tf_idf as tfidf_class

    from .tokens.lex import tokenize
    from .tokens.stopwords import Stop
    # from .termo import Termo
except ImportError:
    from tokens.lex import tokenize
    from tokens.stopwords import Stop
    # from termo import TermoColecao, Termo


class Consulta(object):
    def __init__(self, query=''):
        self.text = query
        self.qtWord = 0
        self.qtWordTotal = 0
        self.qtStopword = 0
        self.qtStopwordTotal = 0
        self.qtAdverbio = 0
        self.qtAdverbioTotal = 0
        self.vetor = []
        self.tokens = []

    def processar(self):
        strategyTF = tf_class.DoubleNormalization()
        print('\nprocessar      ', strategyTF, '\n')
        for word in self.tokens:
            # termo = Termo()
            self.word = word
            frequency = self.tokens[word]

            self.tf[word] = strategyTF.calcPeso(frequency, self)

            if (word in colecao.qtTermoDocumento):
                colecao.qtTermoDocumento[word] += 1
            else:
                colecao.qtTermoDocumento[word] = 1

            if not (word in colecao.listTermosColecao):
                colecao.listTermosColecao.append(word)

        # print(self.tf)

    def get_tokens(self, language='portuguese'):
        return tokenize(self.text, language)

    def get_frequency(self, listTokens):
        frequencyDocument = {}
        for token in listTokens:
            # print(token)
            if token in frequencyDocument:
                frequencyDocument[token] += 1
            else:
                frequencyDocument[token] = 1
        return frequencyDocument

    def remove_stopwords(self):
        # Frequency and Dados <- -Stopword -Adv <- Frequency <- Tokens <- Text
        result = self.clean(self.get_frequency(self.get_tokens()))
        # print('result', result)
        self.qtWord = result['qtWord'] - result['qtStopword'] - result['qtAdverbio']
        self.qtWordTotal = result['qtWordTotal'] - result['qtStopwordTotal'] - result['qtAdverbioTotal']
        self.qtStopword = result['qtStopword']
        self.qtStopwordTotal = result['qtStopwordTotal']
        self.qtAdverbio = result['qtAdverbio']
        self.qtAdverbioTotal = result['qtAdverbioTotal']

        self.termoMaiorFrequencia = result['max']

        self.tokens = result['tokens']
        self.listaTermos = sorted(list(self.tokens.keys()))

    def clean(self, tokens):
        "Remove stopwords e verifica a quantidade removida. Return {'tokens', \
        qtStopword', 'qtStopwordTotal', 'qtAdverbio', 'qtAdverbioTotal'}"
        qtStopword = qtStopwordTotal = 0
        qtAdverbio = qtAdverbioTotal = 0
        qtWordTotal = qtWord = 0

        max_f = 0
        new_tokens = {}

        if (not(type(tokens) != dict or len(tokens) == 0)):
            stopwords = Stop().stopwords
            adverbios = Stop().adverbios

            for key in tokens:
                qtWordTotal += tokens[key]
                qtWord += 1
                if (key in stopwords):
                    qtStopword += 1
                    qtStopwordTotal += tokens[key]
                    # tokens.pop(key)
                elif (key in adverbios):
                    qtAdverbio += 1
                    qtAdverbioTotal += tokens[key]
                    # tokens.pop(key)
                else:
                    if tokens[key] > max_f:
                        max_f = tokens[key]
                    new_tokens[key] = tokens[key]
        return {'tokens': new_tokens,
                'qtStopword': qtStopword, 'qtStopwordTotal': qtStopwordTotal,
                'qtAdverbio': qtAdverbio, 'qtAdverbioTotal': qtAdverbioTotal,
                'qtWord': qtWord, 'qtWordTotal': qtWordTotal, 'max': max_f}


def sort_dic(dic, indice=0):
    return sorted(dic.items(), key=itemgetter(indice))