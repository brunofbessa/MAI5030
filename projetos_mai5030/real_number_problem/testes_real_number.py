#!/usr/bin/python

import sga_real_number
import cga_real_number
import numpy as np
import seaborn as sns
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.pyplot as plt
from timeit import default_timer as timer

'''
Abaixo definimos alguns parametros globais para os testes e comparações entre
 - Simple Genetic Algorithm
 - Compact Genetic Algorithm
'''
NUM_EXEC = 10
CONST_MAX_GERACOES = 100
CONST_TAM_POP = 50
num_genes = 10 # cromossomos/indivíduos com 100 genes binários
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
    lista_mat_cov = []
    for geracao in lista_num_geracoes:
        lista_fitness_geracao = []
        for i in range(NUM_EXEC):
            args = [num_genes, CONST_TAM_POP, geracao, taxa_crossover, taxa_mutacao]
            _fitness, _generations, _mat_cov = fun(args)
            lista_fitness_geracao.append(_fitness)
            mat_cov = _mat_cov
        fitness_geracao = np.mean(lista_fitness_geracao)
        lista_fitness.append(fitness_geracao)
        lista_mat_cov.append(mat_cov)
    return lista_fitness, lista_mat_cov

def calcular_lista_populacoes_ga(fun):
    '''
    Para número fixo de gerações, calcula NUM_EXEC vezes o algoritmo genético.
    É retornada a média de NUM_EXEC execuções da função fitness do algoritmo em formato percentual.
    '''
    lista_fitness = []
    lista_mat_cov = []
    for tam_pop in lista_tam_populacoes:
        lista_fitness_geracao = []
        for i in range(NUM_EXEC):
            args = [num_genes, tam_pop, CONST_MAX_GERACOES, taxa_crossover, taxa_mutacao]
            _fitness, _generations, _mat_cov = fun(args)
            lista_fitness_geracao.append(_fitness)
            mat_cov = _mat_cov
        fitness_geracao = np.mean(lista_fitness_geracao)
        lista_fitness.append(fitness_geracao)
        lista_mat_cov.append(mat_cov)
    return lista_fitness, lista_mat_cov

def main():

    fig, ax = plt.subplots(1, 2)

    start = timer()
    exec_sga = calcular_lista_geracoes_ga(sga_real_number.main)
    fitness_sga = exec_sga[0]
    mat_cov_sga_g = exec_sga[1]
    end = timer()
    tempo_sga = end - start
    start = timer()
    exec_cga = calcular_lista_geracoes_ga(cga_real_number.main)
    fitness_cga = exec_cga[0]
    mat_cov_cga_g = exec_cga[1]
    end = timer()
    tempo_cga = end - start
    ax[0].plot(lista_num_geracoes, fitness_sga, label='SGA ({:.2f}s)'.format(tempo_sga))
    ax[0].plot(lista_num_geracoes, fitness_cga, label='CGA ({:.2f}s)'.format(tempo_cga))
    ax[0].set_xlabel('Núm. de gerações/Func. Evaluations')
    ax[0].set_ylabel('Fitness')
    ax[0].legend()
    ax[0].set_title('Num. Gen. X Fitness')

    start = timer()
    exec_sga = calcular_lista_geracoes_ga(sga_real_number.main)
    fitness_sga = exec_sga[0]
    mat_cov_sga_p = exec_sga[1]
    tempo_sga = end - start
    start = timer()
    exec_cga = calcular_lista_geracoes_ga(cga_real_number.main)
    fitness_cga = exec_cga[0]
    mat_cov_cga_p = exec_cga[1]
    end = timer()
    tempo_cga = end - start
    ax[1].plot(lista_num_geracoes, fitness_sga, label='SGA ({:.2f}s)'.format(tempo_sga))
    ax[1].plot(lista_num_geracoes, fitness_cga, label='CGA ({:.2f}s)'.format(tempo_cga))
    ax[1].set_xlabel('Tamanho da População/Population Size')
    ax[1].set_ylabel('Fitness')
    ax[1].legend()
    ax[1].set_title('Pop. X Fitness')
    ax[1].set_title('Num. Gen. X Fitness')

    plt.show()

    h7 = sns.heatmap(mat_cov_sga_p[-1], square=True,  cmap="YlGnBu")
    h7.set_title('Mat. Cov. SGA Pop=max')
    plt.show()

    h8 = sns.heatmap(mat_cov_cga_p[-1], square=True,  cmap="YlGnBu")
    h8.set_title('Mat. Cov. CGA Pop=max')
    plt.show()

if __name__ == '__main__':
    main()
