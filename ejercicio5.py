import os
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from itertools import permutations
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTADOS_DIR = os.path.join(SCRIPT_DIR, '..', 'resultados')
os.makedirs(RESULTADOS_DIR, exist_ok=True)

def eval_tsp():
    print("--- Procesando Ejercicio 5 (Esto puede tardar unos 10-15 segundos) ---")
    razones = []
    costos_mst, costos_mst2opt, costos_local, costos_sa = [], [], [], []
    
    for k in range(100):
        if k % 20 == 0: print(f"Procesando instancia {k}/100...")
        
        pts = np.random.rand(9, 2)
        dist = lambda r: sum(np.linalg.norm(pts[r[i]] - pts[r[(i+1)%9]]) for i in range(9))
        
        # 1. ÓPTIMO REAL (Fuerza bruta fijando el inicio en 0 para rapidez)
        optimo = float('inf')
        for p in permutations(range(1, 9)):
            c = dist([0] + list(p))
            if c < optimo: optimo = c
            
        # 2. MST PURO
        G = nx.complete_graph(9)
        for u, v in G.edges():
            G[u][v]['weight'] = np.linalg.norm(pts[u] - pts[v])
        mst = nx.minimum_spanning_tree(G)
        ruta_mst = list(nx.dfs_preorder_nodes(mst, source=0))
        costos_mst.append(dist(ruta_mst))
        
        # 3. MST + 2-opt
        ruta_2 = ruta_mst.copy()
        for i in range(1, 7):
            for j in range(i+1, 9):
                n = ruta_2[:i] + ruta_2[i:j][::-1] + ruta_2[j:]
                if dist(n) < dist(ruta_2): ruta_2 = n
        costos_mst2opt.append(dist(ruta_2))
        
        # 4. BÚSQUEDA LOCAL (Aleatorio + 2-opt)
        ruta_loc = list(range(9)); random.shuffle(ruta_loc)
        for i in range(1, 7):
            for j in range(i+1, 9):
                n = ruta_loc[:i] + ruta_loc[i:j][::-1] + ruta_loc[j:]
                if dist(n) < dist(ruta_loc): ruta_loc = n
        costos_local.append(dist(ruta_loc))
        
        # 5. RECOCIDO SIMULADO (Muy rápido por ser 9 ciudades)
        ruta_sa = list(range(9)); random.shuffle(ruta_sa)
        c_sa = dist(ruta_sa); T = 10
        for _ in range(50):
            i, j = sorted(random.sample(range(9), 2))
            n = ruta_sa[:i] + ruta_sa[i:j][::-1] + ruta_sa[j:]
            nc = dist(n)
            if nc < c_sa: # Solo aceptamos mejoras para ir rápido
                ruta_sa = n; c_sa = nc
        costos_sa.append(c_sa)
        
        # Calcular Razón (Costo MST / Costo Óptimo)
        razones.append(costos_mst[-1] / optimo)

    # Gráfica 1: Histograma Razón de Aproximación
    plt.figure(figsize=(7, 5))
    plt.hist(razones, bins=15, color='purple', alpha=0.7, edgecolor='black')
    plt.axvline(x=2.0, color='red', linestyle='--', linewidth=2, label='Límite Teórico (2.0)')
    plt.xlabel('Razón (Costo MST / Costo Óptimo)')
    plt.ylabel('Frecuencia (Instancias)')
    plt.title('Razón de Aproximación del algoritmo basado en MST')
    plt.legend()
    ruta_hist = os.path.join(RESULTADOS_DIR, 'ejercicio5_histograma.png')
    plt.savefig(ruta_hist)
    plt.show()

    # Gráfica 2: Comparativa de TODOS los métodos (Boxplot)
    plt.figure(figsize=(9, 5))
    plt.boxplot([costos_mst, costos_mst2opt, costos_local, costos_sa], 
                tick_labels=['MST Puro', 'MST + 2-opt', 'Búsq. Local', 'Recocido S.'])
    plt.title('Comparativa de Costos Finales entre Métodos (9 Ciudades)')
    plt.ylabel('Costo de la Ruta (Menor es mejor)')
    ruta_box = os.path.join(RESULTADOS_DIR, 'ejercicio5_comparativa.png')
    plt.savefig(ruta_box)
    plt.show()

if __name__ == '__main__':
    eval_tsp()