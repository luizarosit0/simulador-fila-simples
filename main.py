""" M4 - Simulador para uma fila """

""" Etapa 1 - Gerador de numeros pseudoaleatorios """


# Parametros do gerador
X0 = 12345
a = 16807
c = 0
M = 2**31 - 1

# Estado atual do gerador
X = X0

def NextRandom():
    global X
    global count

    # Metodo Congruente Linear
    X = (a * X + c) % M

    # Cada aleatorio solicitado consome uma unidade do contador
    count -= 1

    # Normalizacao intervalo 0, 1
    return X / M


""" Etapa 3 - Fila """

# Variaveis globais 
NUM_SERVIDORES = 1
K = 5 # capacidade total do sistema 

tempo_atual = 0.0
fila = [] 
servidores = [float('inf')] * NUM_SERVIDORES # tempo de saida de cada atendente (inf = livre)
prox_chegada = 3.0
clientes_perdidos = 0

times = [0.0] * (K + 1) # Etapa 4: tempo acumulado em cada estado (0..K)

def clientes_no_sistema():
    em_atendimento = sum(1 for s in servidores if s != float('inf'))
    return len(fila) + em_atendimento

def chegada():
    global prox_chegada
    global clientes_perdidos

    # Agenda proxima chegada
    intervalo_chegada = 2 + 3 * NextRandom()
    prox_chegada = tempo_atual + intervalo_chegada

    # Se o sistema esta cheio (fila + em atendimento)
    if clientes_no_sistema() >= K:
        clientes_perdidos += 1 # perde cliente
        return

    # Procura um servidor livre
    livre = None
    for i in range(NUM_SERVIDORES):
        if servidores[i] == float('inf'):
            livre = i
            break

    # Se ha servidor livre, atende direto
    if livre is not None:
        tempo_atendimento = 3 + 2 * NextRandom()
        servidores[livre] = tempo_atual + tempo_atendimento
    # Senao, entra na fila de espera
    else:
        fila.append(tempo_atual)

def saida():
    # Descobre qual servidor gerou esta saida
    idx = servidores.index(min(servidores))

    # Se existirem clientes esperando, o proximo entra em atendimento
    if len(fila) > 0:
        fila.pop(0)
        tempo_atendimento = 3 + 2 * NextRandom()
        servidores[idx] = tempo_atual + tempo_atendimento
    else:
        servidores[idx] = float('inf')


""" Etapa 2 - Loop """
count = 100000

while count > 0:
    prox_saida = min(servidores)

    if prox_chegada <= prox_saida:
        proximo_tempo = prox_chegada
        tipo_evento = "chegada"
    else:
        proximo_tempo = prox_saida
        tipo_evento = "saida"

    estado = clientes_no_sistema()
    times[estado] += (proximo_tempo - tempo_atual)

    tempo_atual = proximo_tempo

    if tipo_evento == "chegada":
        chegada()
    else:
        saida()

TempoGlobal = tempo_atual

""" Etapa 4 - Resultados """


print(f"Imprimindo resultados da simulacao G/G/{NUM_SERVIDORES}/{K}")

for i in range(K + 1):
    print(str(i) + ": " + str(times[i]) + " (" + str(100 * times[i] / TempoGlobal) + "%)")

print("Clientes perdidos: " + str(clientes_perdidos))
print("Tempo global da simulacao: " + str(TempoGlobal))