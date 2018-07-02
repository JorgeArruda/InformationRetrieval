#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from colecao import Colecao
from documento import Documento
from consulta import Consulta


doc = {
    'aids': 'O Vírus da Imunodeficiência Humana (VIH) é um lentivirus (um retrovirus com um longo período de incubação) que está na origem da Síndrome da Imunodeficiência Adquirida,1 2 uma condição em seres humanos na qual a deterioração progressiva do sistema imunitário propicia o desenvolvimento de infeções oportunistas e cancros potencialmente mortais.',
    'oo': 'A orientação a objetos é um paradigma de análise, projeto e programação de sistemas de software baseado na composição e interação entre diversas unidades de software chamadas de objetos.',
    'sifilis': 'A sífilis pode ser transmitida de uma pessoa para outra durante o sexo sem camisinha com alguém infectado, por transfusão de sangue contaminado ou da mãe infectada para o bebê durante a gestação ou o parto. O uso da camisinha em todas as relações sexuais e o correto acompanhamento durante a gravidez são meios simples, confiáveis e baratos de prevenir-se contra a sífilis.'
}
col = Colecao()

for key in doc:
    documento = col.addDocumento(key, doc[key])
    print('Salvo ...', documento.nome)

print('\n...',col)

query = 'a objetos é um paradigma Vírus da Imunodeficiência Humana sífilis projeto e programação'

consulta = Consulta(query)
print(consulta.tokens)
print(consulta.listaTermos)
print(consulta.qtStopword)

def calcular_consulta(consulta, colecao):
    idf = colecao.idf
    docs = colecao.listDocuments
    words = colecao.listTermosColecao

    for doc in docs:
        sum_q = sum_d = similaridade = 0
        for termo in doc.tf:
            idff = 0
            if termo in idf:
                idff = idf[termo]
            sum_d += doc.tf[termo] * idff

        for termo in consulta.tokens:
            idff = 0
            if termo in idf:
                idff = idf[termo]
            sum_q += consulta.tokens[termo] * idff

        for word in consulta.tokens:
            doc_weight = 0
            if word in doc.listaTermos:
                doc_weight = doc.tf[word] * idf[word]
            idff = 0
            if word in idf:
                idff = idf[word]
            similaridade += consulta.tokens[word] * (idff * doc_weight)
        sum_q =  (sum_q**2)**(0.5)
        sum_d =  (sum_d**2)**(0.5)
        similaridade = similaridade / (sum_q * sum_d)
        print(doc.nome, ': ', similaridade)

calcular_consulta(consulta, col)
