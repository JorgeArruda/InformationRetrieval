#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import math


class InterfaceTF(ABC):

    @abstractmethod
    def calcPeso(self, frequency, documento):
        pass


class RawFrequency(InterfaceTF):
    def calcPeso(self, frequency, documento):
        return frequency


class DoubleNormalization(InterfaceTF):
    def __init__(self):
        self.constante = 0.5

    def calcPeso(self, frequency, documento):
        return self.constante + (1 - self.constante) * (frequency / documento.termoMaiorFrequencia)


class LogNormalization(InterfaceTF):
    def calcPeso(self, frequency, documento):
        return (1.0 + math.log(frequency, 2))

if __name__ == "__main__":
    pass
