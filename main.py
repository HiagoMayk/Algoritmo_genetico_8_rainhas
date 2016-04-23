#!/usr/bin/env python
# -*- coding: utf-8 -*-

#main.py

from agenetico import AGenetico
import time

print("Algoritmo Genetico: Oito Rainhas")
populacao = int(input("Digite o tamanho da populacao:"))
iteracoes =int(input("Digite a quantidade de iterações:"))
taxaMutacao = int(input("Digite a taxa de mutação:"))
taxaCruzamento = int(input("Digite a taxa de cruzamento:"))

# Passa o tamanho do tabuleiro
aGenetico = AGenetico(8)

# Inicia a contagem do tempo
inicio = time.time()

# Passa o tamanho da população
aGenetico.criaPopulacao(populacao)
aGenetico.calculaDiagonais()

for i in range(iteracoes):
    descendente =  aGenetico.recombincaoPMX(taxaCruzamento)
    aGenetico.melhoraPopulacao(taxaMutacao)
    aGenetico.substituirPopulacao(descendente)

# Finaliza a contagem do tempo
fim = time.time()
print
print("Tempo de excução: ", fim - inicio)
print("Quantidade de soluções ótimas encontradas: " + str(aGenetico.qtdSolucoesOtimas()))

#print "Sóluções ótimas:"
#aGenetico.printSolucoesOtimas()




