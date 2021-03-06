#!/usr/bin/python

import numpy as np
import random
import sys
from pyeasyga import pyeasyga
import argparse
import sys

def gerar_vetor_probabilidade(num_genes):
    return [0.5] * num_genes

def competir_candidatos(c1, c2, self):
    if self.fitness_function(c1) > self.fitness_function(c2):
        return c1, c2
    else:
        return c2, c1

def atualizar_vetor_probabilidade(vetor_probabilidade, melhor, pior, tam_pop):
    for i in range(len(vetor_probabilidade)):
        if melhor[i] != pior[i]:
            if melhor[i] == '1':
                vetor_probabilidade[i] += 1.0 / float(tam_pop)
            else:
                vetor_probabilidade[i] -= 1.0 / float(tam_pop)

def gerar_idividuo(vetor_probabilidade):
    individuo = []
    for prob in vetor_probabilidade:
        gene = 1 if random.uniform(0, 1) < prob else 0
        individuo.append(gene)
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
        Para usar o pacote pyeasyga devemos redefinir o
        método run() do pacote implementando
        '''

        vetor_probabilidade = gerar_vetor_probabilidade(num_genes)
        data = [0] * num_genes
        self.seed_data = data
        self.create_first_generation()

        for _ in range(self.generations):
            #competição dos candidatos:
            c1 = gerar_idividuo(vetor_probabilidade)
            c2 = gerar_idividuo(vetor_probabilidade)
            melhor, pior = competir_candidatos(c1, c2, self)

            atualizar_vetor_probabilidade(vetor_probabilidade, melhor, pior, self.population_size)
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
        return ga.best_individual()[0], ga.generations, ga.mat_cov, ga.current_generation
    except ErroCGA:
        print('Erro na execução do CGA.')
        exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])
