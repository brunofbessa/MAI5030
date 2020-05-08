#!/usr/bin/python

import numpy as np
import random
import sys
from pyeasyga import pyeasyga
import argparse
import sys

def gerar_idividuo(seed_data):
    individuo = []
    for _ in seed_data:
        individuo.append(random.randint(0, 1))
    return individuo

def fitness(individuo, data=None):
    u = sum(individuo)
    if u < 5:
        return 4 - u
    else:
        return 5

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
    ga.fitness_function = fitness
    ga.create_individual = gerar_idividuo
    ga.mat_cov = None

    def run(self):
        '''
        Para usar o pacote pyeasyga no cálculo do sga de one max, devemos usar
        a matriz de covariância
        '''

        # Primeira geração a partir do indivíduo gerado acima
        data = [0] * num_genes
        self.seed_data = data
        self.create_first_generation()

        for _ in range(self.generations):
            # Autimatizar neste laço a criação das novas gerações
            #competição dos candidatos:
            self.create_next_generation()

        individuos_geracao = []
        for index_individuo in range(self.population_size):
            individuo = self.current_generation[index_individuo].genes
            individuos_geracao.append(individuo)

        self.mat_cov = np.cov(np.transpose(individuos_geracao))

    ga.run = run

    try:
        # somente o fitness obtido ao final do processo interessa no momento, descartando genes
        ga.run(ga)
        return ga.best_individual()[0], ga.generations, ga.mat_cov
    except ErroSGA:
        print('Erro na execução do SGA.')
        exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])
