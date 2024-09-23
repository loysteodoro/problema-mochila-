import random

def avaliar_cromossomo(cromossomo, pesos_e_valores, peso_maximo):
    peso_total = sum(p * c for (p, _), c in zip(pesos_e_valores, cromossomo))
    valor_total = sum(v * c for (_, v), c in zip(pesos_e_valores, cromossomo))
    if peso_total > peso_maximo:
        return 0, 0
    return valor_total, peso_total

def criar_cromossomo(tamanho):
    return [random.randint(0, 1) for _ in range(tamanho)]

def selecionar_parents(populacao, pesos_e_valores, peso_maximo):
    selected = random.choices(populacao, k=2, weights=[avaliar_cromossomo(cromossomo, pesos_e_valores, peso_maximo)[0] for cromossomo in populacao])
    return selected

def crossover(parent1, parent2):
    ponto_corte = random.randint(1, len(parent1) - 1)
    return parent1[:ponto_corte] + parent2[ponto_corte:]

def mutar(cromossomo):
    for i in range(len(cromossomo)):
        if random.random() < 0.1:
            cromossomo[i] = 1 - cromossomo[i]
    return cromossomo

def algoritmo_genetico(pesos_e_valores, peso_maximo, numero_de_cromossomos, geracoes):
    tamanho = len(pesos_e_valores)
    populacao = [criar_cromossomo(tamanho) for _ in range(numero_de_cromossomos)]
    resultados = []

    for geracao in range(geracoes):
        nova_populacao = []
        for _ in range(numero_de_cromossomos // 2):
            parent1, parent2 = selecionar_parents(populacao, pesos_e_valores, peso_maximo)
            filho1 = crossover(parent1, parent2)
            filho2 = crossover(parent2, parent1)
            nova_populacao.append(mutar(filho1))
            nova_populacao.append(mutar(filho2))

        populacao = nova_populacao
        melhor_individuo = max(populacao, key=lambda c: avaliar_cromossomo(c, pesos_e_valores, peso_maximo)[0])
        melhor_valor, melhor_peso = avaliar_cromossomo(melhor_individuo, pesos_e_valores, peso_maximo)
        media_peso = melhor_peso / (sum(melhor_individuo) or 1)
        
        # Adiciona os resultados da geração
        resultados.append([geracao + 1, melhor_valor, media_peso, melhor_individuo])

    return resultados

if __name__ == "__main__":
    pesos_e_valores = [[2, 10], [4, 30], [6, 300], [8, 10], [8, 30], [8, 300], [12, 50], [25, 75], [50, 100], [100, 400]]
    peso_maximo = 100
    numero_de_cromossomos = 150
    geracoes = 50

    resultado = algoritmo_genetico(pesos_e_valores, peso_maximo, numero_de_cromossomos, geracoes)
    for geracao, valor, media, cromossomo in resultado:
        print(f"Geração: {geracao}, Valor: {valor:.2f}, Média de Peso: {media:.2f}, Cromossomo: {cromossomo}")
