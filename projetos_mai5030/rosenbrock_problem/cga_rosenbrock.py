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
    med_vet_prob = np.mean(vetor_probabilidade)
    std_vet_prob = np.std(vetor_probabilidade)
    if std_vet_prob == 0:
        std_vet_prob = 1
    for _ in range(len(vetor_probabilidade)):
        # Distribuicao Normal Padrao N(0, 1)
        individuo.append(np.random.normal(med_vet_prob, std_vet_prob))
    return individuo

def fitness(individuo, data=None):
    x = np.array(individuo)
    return sum(100.0 * pow(x[1:]-x[:-1], 2) + pow((1-x[:-1]), 2.0))

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
        maximise_fitness = False)
    ga.fitness_function = fitness
    ga.create_individual = gerar_idividuo
    ga.mat_cov = None

    def run(self):
        '''
        Para usar o pacote pyeasyga devemos redefinir o
        método run() do pacote implementando
        '''

        vetor_probabilidade = gerar_vetor_probabilidade(num_genes)
        data = [0] * self.population_size
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
