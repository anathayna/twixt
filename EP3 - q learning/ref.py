import numpy as np
import random

# Now we can define the MDP as a tuple (S, A, T, R, 𝛾).
  # Here, R(s, a) is the reward for taking action a in state s, P(s'|s, a) is the transition probability of reaching state s' given state s and action a, and 𝛾 is the discount factor.
class MDL:
  def __init__(
    self,
    problema,
    desconto = 0.90,
    tetha = 1e-6,
  ):
    self.problema = problema
    self.n_estados = len(problema.estados)
    self.n_acoes = len(problema.acoes)
    self.theta = tetha
    self.desconto = desconto
    # Interação por Valor
    self.V = np.zeros(self.n_estados)

  def calcular_valores(self, n_passos = 10000):
    ## Calculando as funções de Utilidade(S)
    passo = 0
    politica = np.zeros(self.n_estados, dtype=int) 
    while True or passo < n_passos:
      passo += 1 
      delta = 0
      for estado in range(self.n_estados):
        v_antigo = self.V[estado]
        valores_acoes = np.zeros(self.n_acoes)
        # Equação de Bellman
        # V(s) = max_a [R(s, a) + 𝛾 * Σ(P(s'|s, a) * V(s'))]
        for acao in range(self.n_acoes):
          for proximo_estado, probabilidade in self.problema.T(estado, acao):
            valores_acoes[acao] += probabilidade * (self.problema.R(estado, acao, proximo_estado) + self.desconto * self.V[proximo_estado])
        self.V[estado] = np.max(valores_acoes)
        # Iteração por política
        # π(s) = argmax_a [R(s, a) + 𝛾 * Σ(P(s'|s, a) * V(s'))]
        politica[estado] = np.argmax(valores_acoes)
        delta = max(delta, abs(v_antigo - self.V[estado]))
        
        if passo % 1000 == 0:
          V = self.V
          for i in range(0, 16, 4):
            print("%.2f|%.2f|%.2f|%.2f" % (V[i], V[i + 1], V[i + 2], V[i + 3]))
          print("\n")
        
      if delta < self.theta:
        break
    return self.V, politica

# Now we can define the MDP as a tuple (S, A, T, R, 𝛾).
  # Here, R(s, a) is the reward for taking action a in state s, P(s'|s, a) is the transition probability of reaching state s' given state s and action a, and 𝛾 is the discount factor.
class Qlearning:
  def __init__(
    self,
    problema,
    desconto = 0.90,
    tetha = 1e-6,
    alpha = 0.1
  ):
    self.problema = problema
    self.n_estados = len(problema.estados)
    self.n_acoes = len(problema.acoes)
    self.theta = tetha
    self.alpha = alpha
    self.desconto = desconto
    self.e = 0.4
    
    self.Q = np.zeros((self.n_estados, self.n_acoes))
    self.PI = np.zeros(self.n_estados, dtype=int) 

  def calcular_tabela_q(self, estado_inicial = 0, n_passos = 10000, limite_max = 10):
    passo = 0
    
    while passo < n_passos:
      if (passo % 10000 == 0): print("%s passos de %s" %(passo, n_passos))
      passo += 1
      estado = estado_inicial # estado inicial
      limite = 0
      while self.problema.estado_final(estado) == False and limite < limite_max:
        limite += 1
        # escolha da acao
        # random ou melhor da política baseado em uma taxa
        acao = self.sorteia_proxima_acao(estado)
        
        q_antigo = self.Q[estado][acao]
        q_seguinte = 0
        
        # Atualização da Q Table
        # Q(s,a) <= α(*Q(s,a) + (1-α)*Σ(s')( T(s, a, s') * [ R(s,a,s') +  𝛾 max(a) Q(s',a') ] )
        # Q(s,a) <= α(*Q(s,a) + (1-α)*amostra)
        
        # amostra = Σ(s') T(s, a, s') * [ R(s,a,s') +  𝛾 max(a) Q(s',a')
        for proximo_estado, probabilidade in self.problema.T(estado, acao):
          q_seguinte += self.novo_q(estado, acao, proximo_estado, probabilidade)
        # aqui acontece a atualização do Q(s,a)
        self.Q[estado][acao] = self.alpha * q_antigo + (1 - self.alpha) * q_seguinte
  
        # Iteração por política 
        # pega melhor ação para o estado S
        self.PI[estado] = np.argmax(self.Q[estado])
        
        # escolhe o proximo estado probabilisticamente
        estado = self.sorteia_proximo_estado(estado, acao)

    return self.Q, self.PI

  def novo_q(self, estado, acao, proximo_estado, probabilidade):
    max_a = np.max(self.Q[proximo_estado]) # max(a) Q(s',a')
    return probabilidade * (self.problema.R(estado, acao, proximo_estado) + self.desconto * max_a)
  
  # escolha da acao
  # random ou melhor da política baseado em uma taxa
  def sorteia_proxima_acao(self, estado):
    acao_random = random.randrange(self.n_acoes)
    acao_politica = self.PI[estado]
    return random.choices([acao_random, acao_politica], weights = [self.e, (1-self.e)])[0]

  # dado um estado e ação
  # sorteia o próximo estado baseado 
  # nas suas probabilidades de T(s,a, s')
  def sorteia_proximo_estado(self, estado, acao):
    prox_estados = self.problema.T(estado, acao)
    
    estados = []
    probs = []
    for (prox_estado, prob) in prox_estados:
      estados.append(prox_estado)
      probs.append(prob)
    #https://acervolima.com/metodo-random-choices-em-python/
    return random.choices(estados, weights=probs)[0]