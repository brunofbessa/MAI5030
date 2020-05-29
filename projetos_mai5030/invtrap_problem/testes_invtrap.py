#!/usr/bin/python

import sga_invtrap
import cga_invtrap
import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer
from scipy import stats

'''
Abaixo definimos alguns parametros globais para os testes e comparações entre
 - Simple Genetic Algorithm
 - Compact Genetic Algorithm
'''
NUM_EXEC = 10
CONST_MAX_GERACOES = 100
CONST_TAM_POP = 50
num_genes = 5 # cromossomos/indivíduos com 100 genes binários
lista_tam_populacoes = [10, 25, 50, 75, 100]
lista_num_geracoes = [1, 25, 50, 75, 100]
taxa_crossover = 0.8
taxa_mutacao = 0.05


#args = [num_genes, tam_pop, lista_num_geracoes, taxa_crossover, taxa_mutacao]
#args = parser.parse_args([num_genes, tam_pop, num_geracoes, taxa_crossover, taxa_mutacao])

def calcular_lista_geracoes_ga(fun):
    '''
    Para cada número de gerações, calcula NUM_EXEC vezes o algoritmo genético.
    É retornada a média de NUM_EXEC execuções da função fitness do algoritmo em formato percentual.
    '''
    lista_fitness = []
    for geracao in lista_num_geracoes:
        lista_fitness_geracao = []
        for i in range(NUM_EXEC):
            args = [num_genes, CONST_TAM_POP, geracao, taxa_crossover, taxa_mutacao]
            lista_fitness_geracao.append(fun(args)[0])
        fitness_geracao = np.mean(lista_fitness_geracao) / num_genes * 100
        lista_fitness.append(fitness_geracao)
    return lista_fitness

def calcular_lista_populacoes_ga(fun):
    '''
    Para número fixo de gerações, calcula NUM_EXEC vezes o algoritmo genético.
    É retornada a média de NUM_EXEC execuções da função fitness do algoritmo em formato percentual.
    '''
    lista_fitness = []
    for tam_pop in lista_tam_populacoes:
        lista_fitness_geracao = []
        for i in range(NUM_EXEC):
            args = [num_genes, tam_pop, CONST_MAX_GERACOES, taxa_crossover, taxa_mutacao]
            lista_fitness_geracao.append(fun(args)[0])
        fitness_geracao = np.mean(lista_fitness_geracao) / num_genes * 100
        lista_fitness.append(fitness_geracao)
    return lista_fitness

def pop_ga(fun):
    args = [num_genes, CONST_TAM_POP, CONST_MAX_GERACOES, taxa_crossover, taxa_mutacao]
    gen_1 = fun(args)[3]
    pop = []
    for ind in gen_1:
        pop += ind.genes
    return pop

def compara_dist_mannwhitneyu(pop_1, pop_2):
	stat, p = stats.mannwhitneyu(pop_1, pop_2)

	# interpret
	alpha = 0.05
	if p > alpha:
		str_test = 'Mesma distribuição (não rejeita H0)'
	else:
		str_test = 'Distribuições diferentes (rejeita H0)'
	print('Estatística=%.3f, p=%.3f' % (stat, p), ' ', str_test)

def main():

    pop_sga = pop_ga(sga_invtrap.main)
    pop_cga = pop_ga(cga_invtrap.main)
    compara_dist_mannwhitneyu(pop_sga, pop_cga)

    fig, ax = plt.subplots(1, 2)

    start = timer()
    fitness_sga = calcular_lista_geracoes_ga(sga_invtrap.main)
    end = timer()
    tempo_sga = end - start

    start = timer()
    fitness_cga = calcular_lista_geracoes_ga(cga_invtrap.main)
    end = timer()
    tempo_cga = end - start
    ax[0].plot(lista_num_geracoes, fitness_sga, label='SGA ({:.2f}s)'.format(tempo_sga))
    ax[0].plot(lista_num_geracoes, fitness_cga, label='CGA ({:.2f}s)'.format(tempo_cga))
    ax[0].set_xlabel('Núm. de gerações/Func. Evaluations')
    ax[0].set_ylabel('Perc. Bits Corretos/Perc Correct Bits')
    ax[0].legend()
    ax[0].set_title('Num. Gen. X Fitness')

    start = timer()
    fitness_sga = calcular_lista_populacoes_ga(sga_invtrap.main)
    end = timer()
    tempo_sga = end - start
    start = timer()
    fitness_cga = calcular_lista_populacoes_ga(cga_invtrap.main)
    end = timer()
    tempo_cga = end - start
    ax[1].plot(lista_num_geracoes, fitness_sga, label='SGA ({:.2f}s)'.format(tempo_sga))
    ax[1].plot(lista_num_geracoes, fitness_cga, label='CGA ({:.2f}s)'.format(tempo_cga))
    ax[1].set_xlabel('Tamanho da População/Population Size')
    ax[1].set_ylabel('Perc. Bits Corretos/Perc Correct Bits')
    ax[1].legend()
    ax[1].set_title('Pop. X Fitness')

    plt.show()

if __name__ == '__main__':
    main()
