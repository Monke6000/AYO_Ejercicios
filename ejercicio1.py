import multiprocessing as mp
import time
import random
import os
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTADOS_DIR = os.path.join(SCRIPT_DIR, '..', 'resultados')
os.makedirs(RESULTADOS_DIR, exist_ok=True)

# Función que calcula puntos dentro de un círculo para estimar Pi
def monte_carlo_pi(n):
    dentro = 0
    for _ in range(n):
        x, y = random.random(), random.random()
        if x*x + y*y <= 1.0:
            dentro += 1
    return dentro

def estimate_pi(n_total, n_procesos):
    n_por_proceso = n_total // n_procesos
    pool = mp.Pool(processes=n_procesos)
    
    inicio = time.time()
    # Mapeamos la tarea a los procesos
    resultados = pool.map(monte_carlo_pi, [n_por_proceso] * n_procesos)
    pool.close()
    pool.join()
    fin = time.time()
    
    return fin - inicio

if __name__ == '__main__':
    puntos_totales = 10_000_000 # 10 millones de puntos
    procesos = [1, 2, 4, 8]
    tiempos = []

    print("--- Iniciando Ejercicio 1 ---")
    for p in procesos:
        print(f"Calculando con {p} proceso(s)...")
        t = estimate_pi(puntos_totales, p)
        tiempos.append(t)

    # Calcular speedup (Aceleración = Tiempo_1_proceso / Tiempo_N_procesos)
    speedup = [tiempos[0] / t for t in tiempos]

    # Graficar
    plt.figure(figsize=(8, 5))
    plt.plot(procesos, speedup, marker='o', label='Speedup Real', color='blue', linewidth=2)
    plt.plot(procesos, procesos, linestyle='--', color='red', label='Speedup Ideal')
    plt.xlabel('Número de Procesos')
    plt.ylabel('Aceleración (Speedup)')
    plt.title('Aceleración Paralela vs Procesos')
    plt.legend()
    plt.grid(True)
    
    # Guardado seguro
    ruta_guardado = os.path.join(RESULTADOS_DIR, 'ejercicio1_speedup.png')
    plt.savefig(ruta_guardado)
    print(f"Gráfica guardada en: {ruta_guardado}")
    plt.show()