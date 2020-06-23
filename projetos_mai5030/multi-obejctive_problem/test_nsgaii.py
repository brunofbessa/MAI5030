import nsgaii
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import os

NUM_EXEC = 100
CONST_MAX_GERACOES = 100
CONST_TAM_POP = 50

lista_tam_populacoes = [10, 25, 50, 75, 100]
lista_num_geracoes = [25, 50, 75, 100]
num_genes = 1
taxa_crossover = 0.5
lista_taxa_crossover = [0, 0.1, 0.25, 0.5, 0.75, 1]
taxa_mutacao = 0.05
args = [num_genes, CONST_TAM_POP, 100, taxa_crossover, taxa_mutacao]

# Hiper-volume
valores_fitness1, valores_fitness2 = nsgaii.main(args)

_f1, _f2 = nsgaii.main(args)

plt.xlabel('Fun. -(x)^2', fontsize=15)
plt.ylabel('Fun. -(x-2)ˆ2', fontsize=15)
plt.scatter(valores_fitness1, valores_fitness2)
# Plot não dominados
#plt.show()

def plot_eaf(runs=100, verbose=False):
	f1 = []
	f2 = []
	run = []

	args = [num_genes, CONST_TAM_POP, 100, taxa_crossover, taxa_mutacao]

	for r in range(runs):
		_f1, _f2 = nsgaii.main(args)
		for _ in range(len(_f1)):
			f1.append(_f1[_])
			f2.append(_f2[_])
			run.append(r)

		if verbose == True:
			print('Progresso: ' + str(r/runs))

	df = pd.DataFrame()
	df['f1'] = f1
	df['f2'] = f2
	df['run'] = run
	df.to_csv('nsgaii.csv', index=False)
	os.system('Rscript eaf.R')


plot_eaf(verbose=True)
