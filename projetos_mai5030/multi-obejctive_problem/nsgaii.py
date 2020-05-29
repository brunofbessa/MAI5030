#!/usr/bin/python

import numpy as np
import random
import sys
from pyeasyga import pyeasyga
import argparse
import sys
import math

MIN_X = -100
MAX_X = 100

def gerar_individuo(seed_data=None):
    return MAX_X + (MAX_X - MIN_X) * random.random()

def gerar_populacao(tam_pop):
    populacao = []
    for i in range(0, tam_pop):
        populacao.append(gerar_individuo())
    return populacao

def fitness1(x, data=None):
    return -1 * pow(x,2)

def fitness2(x, data=None):
    return -1 * pow(x-2, 2)

def retornar_indice(val, lista):
    for i in range(0, len(lista)):
        if lista[i] == val:
            return i
    return -1

def ordenar_listas(lista, valores):
    lista_ordenada = []
    while(len(lista_ordenada)!=len(lista)):
        if retornar_indice(min(valores), valores) in lista:
            lista_ordenada.append(retornar_indice(min(valores), valores))
        valores[retornar_indice(min(valores), valores)] = math.inf
    return lista_ordenada

def otimo_pareto(valores1, valores2):
    S=[[] for i in range(0,len(valores1))]
    fronteira = [[]]
    n=[0 for i in range(0,len(valores1))]
    rank = [0 for i in range(0, len(valores1))]

    for p in range(0,len(valores1)):
        S[p]=[]
        n[p]=0
        for q in range(0, len(valores1)):
            if (valores1[p] > valores1[q] and valores2[p] > valores2[q]) or (valores1[p] >= valores1[q] and valores2[p] > valores2[q]) or (valores1[p] > valores1[q] and valores2[p] >= valores2[q]):
                if q not in S[p]:
                    S[p].append(q)
            elif (valores1[q] > valores1[p] and valores2[q] > valores2[p]) or (valores1[q] >= valores1[p] and valores2[q] > valores2[p]) or (valores1[q] > valores1[p] and valores2[q] >= valores2[p]):
                n[p] = n[p] + 1
        if n[p]==0:
            rank[p] = 0
            if p not in fronteira[0]:
                fronteira[0].append(p)

    i = 0
    while(fronteira[i] != []):
        Q=[]
        for p in fronteira[i]:
            for q in S[p]:
                n[q] =n[q] - 1
                if( n[q]==0):
                    rank[q]=i+1
                    if q not in Q:
                        Q.append(q)
        i = i+1
        fronteira.append(Q)
    del fronteira[len(fronteira)-1]

    return fronteira

def crowding_distance(valores1, valores2, fronteira):
    distancia = [0 for i in range(0, len(fronteira))]
    ordenado1 = ordenar_listas(fronteira, valores1[:])
    ordenado2 = ordenar_listas(fronteira, valores2[:])
    distancia[0] = 10000000000
    distancia[len(fronteira) - 1] = 10000000000

    for k in range(1,len(fronteira)-1):
        distancia[k] = distancia[k]+ (valores1[ordenado1[k+1]] - valores2[ordenado1[k-1]])/(max(valores1)-min(valores1))
    for k in range(1,len(fronteira)-1):
        distancia[k] = distancia[k]+ (valores2[ordenado2[k+1]] - valores1[ordenado2[k-1]])/(max(valores2)-min(valores2))
    return distancia

#Function to carry out the crossover
def crossover(pai1, pai2, taxa_crossover, taxa_mutacao):
    if random.random() > taxa_crossover:
        return mutacao((pai1 + pai2)/2, taxa_mutacao)
    else:
        return mutacao((pai1 - pai2)/2, taxa_mutacao)

#Function to carry out the mutation operator
def mutacao(individuo, taxa_mutacao):
    if random.random() > taxa_mutacao:
        individuo = MIN_X+(MAX_X-MIN_X) * random.random()
    return individuo

def main(args):

    num_genes = int(args[0])
    tam_pop = int(args[1])
    num_geracoes = int(args[2])
    taxa_crossover = float(args[3])
    taxa_mutacao = float(args[4])

    data = [0] * num_genes
    ga = pyeasyga.GeneticAlgorithm(
        data,
        population_size = tam_pop,
        generations = num_geracoes,
        crossover_probability = taxa_crossover,
        mutation_probability = taxa_mutacao,
        elitism = True,
        maximise_fitness = True)
    ga.create_individual = gerar_individuo
    ga.valores_fitness1 = None
    ga.valores_fitness2 = None
    ga.mutacao = mutacao

    def run(self):
        '''
        Para usar o pacote pyeasyga devemos redefinir o
        método run() do pacote implementando
        '''

        # Primeira geração a partir do indivíduo gerado acima
        data = [0] * num_genes
        self.seed_data = data
#        self.create_first_generation()
        solucao = gerar_populacao(tam_pop)

        gen = 0
        while(gen < num_geracoes):
            #print('len solucao: ', len(solucao), ' gen: ', gen)
            #print('solucao: ', solucao)
            valores_fitness1 = [fitness1(solucao[i]) for i in range(0, tam_pop)]
            valores_fitness2 = [fitness2(solucao[i]) for i in range(0, tam_pop)]
            fronteira_otimo_pareto = otimo_pareto(valores_fitness1[:], valores_fitness1[:])

            crowding_distance_v = []
            for i in range(0, len(fronteira_otimo_pareto)):
                crowding_distance_v.append(crowding_distance(valores_fitness1[:], valores_fitness2[:], fronteira_otimo_pareto[i][:]))
            solucao2 = solucao[:]

            # Descendentes
            while(len(solucao2) != 2*tam_pop):
                pai1 = random.randint(0, tam_pop-1)
                pai2 = random.randint(0, tam_pop-1)
                solucao2.append(crossover(solucao[pai1], solucao[pai2], taxa_crossover, taxa_mutacao))
            valores_fitness1_2 = [fitness1(solucao2[i]) for i in range(0, 2*tam_pop)]
            valores_fitness2_2 = [fitness2(solucao2[i]) for i in range(0, 2*tam_pop)]
            fronteira_otimo_pareto2 = otimo_pareto(valores_fitness1_2[:], valores_fitness2_2[:])

            crowding_distance_v2=[]
            for i in range(0, len(fronteira_otimo_pareto2)):
                crowding_distance_v2.append(crowding_distance(valores_fitness1_2[:], valores_fitness2_2[:], fronteira_otimo_pareto2[i][:]))

            filho= []
            for i in range(0, len(fronteira_otimo_pareto2)):
                fronteira_otimo_pareto2_1 = [retornar_indice(fronteira_otimo_pareto2[i][j],fronteira_otimo_pareto2[i] ) for j in range(0, len(fronteira_otimo_pareto2[i]))]

                fronteira_aux = ordenar_listas(fronteira_otimo_pareto2_1[:], crowding_distance_v2[i][:])
                fronteira = [fronteira_otimo_pareto2[i][fronteira_aux[j]] for j in range(0, len(fronteira_otimo_pareto2[i]))]
                fronteira.reverse()

                for v in fronteira:
                    filho.append(v)
                    if(len(filho) == tam_pop):
                        break
                if (len(filho) == tam_pop):
                    break


            solucao = [solucao2[i] for i in filho]

            gen += 1

        self.valores_fitness1 = valores_fitness1
        self.valores_fitness2 = valores_fitness2


    ga.run = run

    try:
        ga.run(ga)
        return ga.valores_fitness1, ga.valores_fitness2

    except ErroSGA:
        print('Erro na execução do SGA.')
        exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])
