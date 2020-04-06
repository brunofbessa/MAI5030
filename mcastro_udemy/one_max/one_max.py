import random
import sys

def gerar_idividuo(num_genes):
    individuo = ''
    for _ in range(num_genes):
        individuo += str(random.randint(0, 1))
    return individuo

def gerar_populacao(tam_pop, num_genes):
    populacao = []
    for _ in range(tam_pop):
        populacao.append(gerar_idividuo(num_genes))
    return populacao

def fitness(individuo):
    return sum(int(gene) for gene in individuo)

def selecionar_pais(populacao, tam_pop, K=3):
    pais = []

    for torneio in range(tam_pop):
        competidores = []

        for _ in range (K):
            indice = random.randint(0, tam_pop-1)
            competidores.append(populacao[indice])

        maior_avaliacao = fitness(competidores[0])
        vencedor = competidores[0]
        for _ in range(1, K):
            avaliacao = fitness(competidores[_])
            if avaliacao > maior_avaliacao:
                maior_avaliacao = avaliacao
                vencedor = competidores[_]

        pais.append(vencedor)
    return pais

def gerar_filhos(pais, tam_pop, taxa_crossover=-0.7):
    nova_populacao = []

    for _ in range(tam_pop//2):
        pai1 = random.choice(pais)
        pai2 = random.choice(pais)

        if random.random() < taxa_crossover:
            corte = random.randint(1, len(pai1)-1)
            filho1 = pai1[0:corte] + pai2[corte:]
            filho2 = pai2[0:corte] + pai1[corte:]
            nova_populacao.append(filho1)
            nova_populacao.append(filho2)
        else:
            nova_populacao.append(pai1)
            nova_populacao.append(pai2)

    return(nova_populacao)

def mutacao(populacao, tam_pop, num_genes, taxa_mutacao=0.005):
    nova_populacao = []

    for _ in range(tam_pop):
        individuo = ''
        for gene in range(num_genes):
            if random.random() < taxa_mutacao:
                if populacao[_][gene] == '0':
                    individuo += '1'
                else:
                    individuo += '0'
            else:
                individuo += populacao[_][gene]
        nova_populacao.append(individuo)
    return nova_populacao

def melhor_individuo(populacao, tam_pop):
    melhor_avaliacao = fitness(populacao[0])
    indice_melhor = 0

    for i in range(1, tam_pop):
        avaliacao = fitness(populacao[i])
        if avaliacao > melhor_avaliacao:
            melhor_avaliacao = avaliacao
            infice_melhor = i
    return populacao[indice_melhor]

def main():

    tam_pop = int(sys.argv[1])
    num_genes = int(sys.argv[2])
    taxa_crossover = float(sys.argv[3])
    taxa_mutacao = float(sys.argv[4])
    num_geracoes = int(sys.argv[5])

    populacao = gerar_populacao(tam_pop, num_genes)

    for geracao in range(num_geracoes):
        pais = selecionar_pais(populacao, tam_pop)
        nova_populacao = gerar_filhos(pais, tam_pop)
        populacao = mutacao(nova_populacao, tam_pop, num_genes, taxa_mutacao)


    melhor = melhor_individuo(populacao, tam_pop)
    print('Melhor indivíduo: ', melhor)
    print('Melhor avaliação: ', fitness(melhor))

if __name__ == '__main__':
    main()
