import numpy as np

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