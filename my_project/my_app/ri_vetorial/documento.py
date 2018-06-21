#!/usr/bin/env python3
# -*- coding: utf-8 -*-
try:
    from .frequency import term_frequency as tf_class
    from .frequency import inverse_frequency as idf_class
    from .frequency import tf_idf as tfidf_class

    from .tokens.lex import tokenize
    from .tokens.archive import remove_stopwords, get_frequency
    from .termo import TermoColecao, Termo
except ImportError:
    from tokens.lex import tokenize
    from tokens.archive import remove_stopwords, get_frequency
    from termo import TermoColecao, Termo


class Documento(object):
    def __init__(self, nome, texto):
        self.nome = nome
        self.text = texto

        self.qtWord = 0
        self.qtWordTotal = 0
        self.qtStopword = 0
        self.qtStopwordTotal = 0
        self.qtAdverbio = 0
        self.qtAdverbioTotal = 0

        self.termoMaiorFrequencia = 0
        self.listTermosProcessados = []
        self.listaTermos = []
        self.tokens = {}
        self.tf = {}

    def get_tokens(self, language='portuguese'):
        return tokenize(self.text, language)

    def remove_stopwords(self):
        result = remove_stopwords(get_frequency(self.get_tokens()))
        print('result', result)
        self.qtWord = result['qt_tok'] - result['qt_stopwords'] - result['qt_adverbios']
        self.qtWordTotal = result['qt_tok_total'] - result['qt_stopwords'] - result['qt_stopwords_total']
        self.qtStopword = result['qt_stopwords']
        self.qtStopwordTotal = result['qt_stopwords_total']
        self.qtAdverbio = result['qt_adverbios']
        self.qtAdverbioTotal = result['qt_adverbios_total']

        self.termoMaiorFrequencia = result['max']

        self.tokens = result['tokens']
        self.listaTermos = sorted(list(self.tokens.keys()))

    def processar(self, colecao):
        strategyTF = self.instanciar(tf_class, colecao.algoritmo['tf'])
        # strategyIDF = self.instanciar(idf_class, strategyIDF)
        # strategyTFIDF = self.instanciar(tfidf_class, strategyTFIDF)
        print(self.tokens)
        for word in self.tokens:
            # termo = Termo()
            self.word = word
            frequency = self.tokens[word]
            # termo.tf = strategyTF.calcularPeso(termo, self)
            # termo.idf = idf = strategyIDF.calcularPeso(termo, listaDocumentos)
            # termo.tfIdf = termo.tf * termo.idf

            self.tf[word] = strategyTF.calcPeso(frequency, self)

            if (word in colecao.qtTermoDocumento):
                colecao.qtTermoDocumento[word] += 1
            else:
                colecao.qtTermoDocumento[word] = 1

            if not (word in colecao.listTermosColecao):
                colecao.listTermosColecao.append(word)

            # self.listTermosProcessados.append(termo)
        print(self.tf)

    def instanciar(self, origem, strategy):
        try:
            return getattr(origem, strategy)()
        except AttributeError:
            print('Error, a classe %s não existe' % (strategy))
    # def retirarStopWords()
    # def buscarTermo()
