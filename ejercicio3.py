import os
import numpy as np
import matplotlib.pyplot as plt
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTADOS_DIR = os.path.join(SCRIPT_DIR, '..', 'resultados')
os.makedirs(RESULTADOS_DIR, exist_ok=True)

# 20 ciudades aleatorias
np.random.seed(42)
ciudades = np.random.rand(20, 2)

def distancia(ruta):
    dist = 0
    for i in range(len(ruta)):
        c1, c2 = ciudades[ruta[i]], ciudades[ruta[(i+1)%len(ruta)]]
        dist += np.linalg.norm(c1 - c2)
    return dist

def vecino_mas_cercano():
    no_visitadas = list(range(1, 20))
    ruta = [0] # Nodo inicial aleatorio (fijo en 0 para simplificar)
    while no_visitadas:
        ultima = ciudades[ruta[-1]]
        siguiente = min(no_visitadas, key=lambda c: np.linalg.norm(ultima - ciudades[c]))
        ruta.append(siguiente)
        no_visitadas.remove(siguiente)
    return ruta

def two_opt(ruta_inicial):
    ruta = ruta_inicial.copy()
    mejoras = 0
    mejorando = True
    while mejorando:
        mejorando = False
        for i in range(1, len(ruta) - 2):
            for j in range(i + 1, len(ruta)):
                if j - i == 1: continue
                # Intercambio 2-opt
                nueva_ruta = ruta[:i] + ruta[i:j][::-1] + ruta[j:]
                if distancia(nueva_ruta) < distancia(ruta):
                    ruta = nueva_ruta
                    mejoras += 1
                    mejorando = True
        if not mejorando: break
    return ruta, mejoras, distancia(ruta)

print("--- Procesando Ejercicio 3 (Búsqueda Local) ---")
mejoras_random, calidad_random = [], []
mejoras_nn, calidad_nn = [], []

for _ in range(50): # 50 experimentos para datos robustos
    # 1. Inicio Aleatorio
    ruta_rand = list(range(20))
    random.shuffle(ruta_rand)
    _, m_rand, c_rand = two_opt(ruta_rand)
    mejoras_random.append(m_rand)
    calidad_random.append(c_rand)
    
    # 2. Inicio Vecino Más Cercano
    ruta_nn = vecino_mas_cercano()
    _, m_nn, c_nn = two_opt(ruta_nn)
    mejoras_nn.append(m_nn)
    calidad_nn.append(c_nn)

# Crear figura con 2 subgráficas (Mejoras y Calidad)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Subgráfica 1: Número de Mejoras
axes[0].boxplot([mejoras_random, mejoras_nn], tick_labels=['Aleatorio', 'Vecino Cercano'])
axes[0].set_ylabel('Número de Mejoras aplicadas')
axes[0].set_title('Mejoras necesarias para converger')

# Subgráfica 2: Calidad Final (Distancia - menor es mejor)
axes[1].boxplot([calidad_random, calidad_nn], tick_labels=['Aleatorio', 'Vecino Cercano'])
axes[1].set_ylabel('Costo Final (Distancia)')
axes[1].set_title('Calidad del Óptimo Alcanzado')

plt.suptitle('Evaluación de Búsqueda Local (2-opt)', fontsize=14)
ruta_guardado = os.path.join(RESULTADOS_DIR, 'ejercicio3_2opt.png')
plt.savefig(ruta_guardado)
plt.show()