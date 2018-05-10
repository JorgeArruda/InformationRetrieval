#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Importando arquivos
import lex
import ocr
import frequency
import mysql

# archive = open("txt/exe01.txt", "r")
# documents = lex.tokenize(archive.read())
# print(documents)
# archive.close()

# archive = open("documents.txt", "w", encoding='utf-8')
# archive.write(json.dumps({"exe01.txt":documents}, ensure_ascii=False))
# archive.close()

# archive = open("documents.txt", "r", encoding='utf-8')
# text = json.loads(archive.read())
# archive.close()

# print('\n\ntext',text['exe01.txt'])

connection = mysql.connect()
# mysql.saveTokens(connection, 'documents.txt', json.dumps({"exe01.txt":documents}))
tokens = mysql.getTokens(connection, 'documents.txt')
print(json.loads(tokens)['exe01.txt'])
