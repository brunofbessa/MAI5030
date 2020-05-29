import nsgaii
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

NUM_EXEC = 1
CONST_MAX_GERACOES = 10
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
i = 1
for num_geracoes in lista_num_geracoes:
	args = [num_genes, CONST_TAM_POP, num_geracoes, taxa_crossover, taxa_mutacao]
	_f1, _f2 = nsgaii.main(args)
	for _i in _f1:
		run.append(i)
	f1 += _f1
	f2 += _f2
	i += 1

df = pd.DataFrame()
df['f1'] = f1
df['f2'] = f2
df['run'] = run

df.to_csv('nsgaii.csv', index=False)

#print(df)


plt.xlabel('Fun. -(x)^2')
plt.ylabel('Fun. -(x-2)ˆ2')
plt.scatter(f1, f2)
print()
#plt.show()
