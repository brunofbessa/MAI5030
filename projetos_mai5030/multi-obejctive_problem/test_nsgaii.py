import nsgaii
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

NUM_EXEC = 100
CONST_MAX_GERACOES = 100
CONST_TAM_POP = 50

lista_tam_populacoes = [10, 25, 50, 75, 100]
lista_num_geracoes = [25, 50, 75, 100]
num_genes = 1
taxa_crossover = 0.5
taxa_mutacao = 0.05
#args = [num_genes, CONST_TAM_POP, 100, taxa_crossover, taxa_mutacao]

f1 = []
f2 = []
run = []

args = [num_genes, CONST_TAM_POP, CONST_MAX_GERACOES, taxa_crossover, taxa_mutacao]

for exec in range(0, NUM_EXEC):
	_f1, _f2 = nsgaii.main(args)
	for _i in _f1:
		run.append(exec+1)
	f1 += _f1
	f2 += _f2
	print(str(exec/NUM_EXEC) + '%')


df = pd.DataFrame()
df['f1'] = f1
df['f2'] = f2
df['run'] = run

df.to_csv('nsgaii.csv', index=False)

#print(df)


#plt.show()
