#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ply.lex as lex
import nltk

tokens = (
  'WORD',
  'WORD2',
  'COMPOSTA',
)


def MyLexer():
    "Return a lexer from my environment"
    # Regular expression rules for simple tokens
    # t_WORD = r'[a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ|ç|0-9]+[a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ\ç|0-9][a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ|ç|0-9]*'
    # t_WORD2 = r'[a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ|ç|0-9]+[a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ\ç|0-9][a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ|ç|0-9]*[\'][a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ|ç|0-9]+'
    # t_COMPOSTA = r'[a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ|ç|0-9]+[a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ\ç|\'|0-9][a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ|ç|0-9|\']*[\-][a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ|ç|0-9|\']+'

    t_WORD = r'[a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ|ç]+[a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ\ç|0-9][a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ|ç|0-9]*'
    t_WORD2 = r'[a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ|ç]+[a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ\ç|0-9][a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ|ç|0-9]*[\'][a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ|ç|0-9]+'
    t_COMPOSTA = r'[a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ|ç]+[a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ\ç|\'|0-9][a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ|ç|0-9|\']*[\-][a-z|A-Z|é|ê|á|à|ã|â|ó|ô|õ|ç|0-9|\']+'

    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t+=*/(){},:[]'

    # Error handling rule
    def t_error(t):
        # print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer from my environment and return it
    return lex.lex()


def tokenize(text, language='portuguese'):
    "Tokenize -> remove stopwords -> returns tokens"

    # Get stopwords lib nltk. language == 'portuguese', 'english'...
    stopwords = nltk.corpus.stopwords.words(language)

    lexer = MyLexer()   # lex analize object
    lexer.input(text)

    listTokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        listTokens.append(tok.value.lower())
    print('Lex ... listTokens -- ', listTokens)
    return sorted(listTokens)
