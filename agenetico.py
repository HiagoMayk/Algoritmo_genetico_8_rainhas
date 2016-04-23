#!/usr/bin/env python
# -*- coding: utf-8 -*-

#tabuleiro.py

from random import randint

class AGenetico(object):

    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.populacao = []
        self.diagonalPositiva = []
        self.diagonalNegativa = []
        self.resultFObjetivo = []


    #Cria a populacao inicial
    def criaPopulacao(self, quantidade):
        for i in range(quantidade):
            pop = []
            gerados = []

            for j in range(self.tamanho):
                r = randint(0, self.tamanho-1)

                while(r in gerados):
                    r = randint(0, self.tamanho-1)

                gerados.append(r)
                pop.append(r)

            self.populacao.append(pop)


    def calculaColisoesDPositiva(self, pop):
        colisoes = 0
        verificados = []
        for i in range(len(pop)):
            if(self.diagonalPositiva[i][pop[i]] in verificados):
                 colisoes = colisoes + 1
            else:
                verificados.append(self.diagonalPositiva[i][pop[i]])

        return colisoes


    def calculaColisoesDNegativa(self, pop):
        colisoes = 0
        verificados = []
        for i in range(len(pop)):
            if(self.diagonalNegativa[i][pop[i]] in verificados):
                 colisoes = colisoes + 1
            else:
                verificados.append(self.diagonalNegativa[i][pop[i]])

        return colisoes


    def funcaoObjetivo(self, pop):
        return (self.calculaColisoesDPositiva(pop) + self.calculaColisoesDNegativa(pop))


    # Selecao por torneio
    def seleciona(self):
        i = randint(0, self.tamanho-1)
        j = randint(0, self.tamanho-1)
        escolhido1 = 0
        escolhido2 = 0

        # Evita escolher um cara que ja seja solucao
        while(i == j or self.funcaoObjetivo(self.populacao[j]) == 0):
            j = randint(0, self.tamanho-1)

        if self.funcaoObjetivo(self.populacao[i]) < self.funcaoObjetivo(self.populacao[j]):
            escolhido1 = i
        else:
            escolhido1 = j

        i = randint(0, self.tamanho-1)

        while(escolhido1  == i):
            i = randint(0, self.tamanho-1)

        j = randint(0, self.tamanho-1)

        # Evita escolher um cara que ja seja solução otima
        while(i == j or escolhido1 == j or self.funcaoObjetivo(self.populacao[j]) == 0):
            j = randint(0, self.tamanho-1)

        if self.funcaoObjetivo(self.populacao[i]) < self.funcaoObjetivo(self.populacao[j]):
            escolhido2 = i
        else:
            escolhido2 = j

        return ((escolhido1, self.populacao[escolhido1]), (escolhido2, self.populacao[escolhido2]))


    # Partialy-mapped crossover (PMX)
    # Extensao da combinação apresentada no artigo
    def recombincaoPMX(self, taxa):
        rand = faixa = randint(1, 101)

        if rand <= taxa:
            faixa = randint(1, self.tamanho-1)
            inicio = randint(0, (self.tamanho-1)-faixa)

            # Selecao por torneio
            escolhido1, escolhido2 = self.seleciona()

            # Observe a troca nos cromossomos
            descendente1 = self.populacao[escolhido2[0]][inicio:(inicio+faixa)]
            descendente2 = self.populacao[escolhido1[0]][inicio:(inicio+faixa)]

            relacao = []
            for i in range(len(descendente1)):
                relacao.append([descendente1[i], descendente2[i]])

            flag = True
            while(flag):
                flag = False
                for rel in relacao:
                    for relAux in relacao:
                        if rel[1] == relAux[0]:
                            rel[1] = relAux[1]
                            relacao.remove(relAux)
                            flag = True

            p1 = self.populacao[escolhido1[0]][:inicio]
            p2 = self.populacao[escolhido2[0]][:inicio]
            for rel in relacao:
                if rel[0] in p1:
                    for i in range(len(p1)):
                        if p1[i] == rel[0]:
                            p1[i]  = rel[1]

            for rel in relacao:
                if rel[1] in p2:
                    for i in range(len(p2)):
                        if p2[i] == rel[1]:
                            p2[i]  = rel[0]

            f1 = self.populacao[escolhido1[0]][inicio+faixa:]
            f2 = self.populacao[escolhido2[0]][inicio+faixa:]
            for rel in relacao:
                if rel[0] in f1:
                    for i in range(len(f1)):
                        if f1[i] == rel[0]:
                            f1[i]  = rel[1]

            for rel in relacao:
                if rel[1] in f2:
                    for i in range(len(f2)):
                        if f2[i] == rel[1]:
                            f2[i]  = rel[0]

            descendente1 = p1+ descendente1 + f1
            descendente2 = p2 + descendente2 + f2
            if self.funcaoObjetivo(descendente1) <  self.funcaoObjetivo(descendente2):
                return descendente1
            else:
                return descendente2

        else:
            # Selecçao por torneio
            escolhido1, escolhido2 = self.seleciona()

            # Observe a troca nos cromossomos
            descendente1 = self.populacao[escolhido1[0]]
            descendente2 = self.populacao[escolhido2[0]]

            if self.funcaoObjetivo(descendente1) <  self.funcaoObjetivo(descendente2):
                return descendente1
            else:
                return descendente2


    def melhoraPopulacao(self, taxa):
        rand = randint(1, 101)

        if rand <= taxa:
            melhorada = []
            for pop in self.populacao:
                i = randint(0, self.tamanho-1)
                j = randint(0, self.tamanho-1)

                newPop = pop[:]
                newPop[i], newPop[j] = newPop[j], newPop[i]

                if self.funcaoObjetivo(newPop) < self.funcaoObjetivo(pop) and newPop not in self.populacao:
                    melhorada.append(newPop)
                else:
                    melhorada.append(pop)

                self.populacao = melhorada[:]


    def obterMaior(self):
        maior  = (0, self.funcaoObjetivo(self.populacao[0]))

        for i in range(len(self.populacao)):
            if maior[1] < self.funcaoObjetivo(self.populacao[i]):
                    maior = (i, self.funcaoObjetivo(self.populacao[i]))

        return maior


    def substituirPopulacao(self, escolha):
        maior = self.obterMaior()
        if escolha not in self.populacao:
            if self.funcaoObjetivo(escolha) <= maior[1]:
                self.populacao[maior[0]] = escolha[:]


    def calculaDiagonais(self):
         for i in range(self.tamanho):
            positiva = []
            negativa = []
            for j in range(self.tamanho):
                positiva.append(i - j)
                negativa.append(i + j)

            self.diagonalPositiva.append(positiva)
            self.diagonalNegativa.append(negativa)


    def printPopulacao(self):
        for pop in self.populacao:
            print(self.funcaoObjetivo(pop), pop)


    def printDiagonalPositiva(self):
        for dp in self.diagonalPositiva:
            print(dp)


    def printDiagonalNegativa(self):
        for dn in self.diagonalNegativa:
            print(dn)


    def qtdSolucoesOtimas(self):
        cont = 0
        for pop in self.populacao:
            func = self.funcaoObjetivo(pop)
            if func == 0:
                cont = cont + 1

        return cont


    def printSolucoesOtimas(self):
        for pop in self.populacao:
            func = self.funcaoObjetivo(pop)
            if func == 0:
                print(func, pop)

