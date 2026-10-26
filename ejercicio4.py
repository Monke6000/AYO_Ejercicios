import os
import numpy as np
import matplotlib.pyplot as plt
import random, math, time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTADOS_DIR = os.path.join(SCRIPT_DIR, '..', 'resultados')
os.makedirs(RESULTADOS_DIR, exist_ok=True)

np.random.seed(42)
ciudades = np.random.rand(20, 2)

def distancia(ruta):
    return sum(np.linalg.norm(ciudades[ruta[i]] - ciudades[ruta[(i+1)%20]]) for i in range(20))

def vecino_2opt_aleatorio(ruta):
    i, j = sorted(random.sample(range(20), 2))
    nueva = ruta[:i] + ruta[i:j][::-1] + ruta[j:]
    return nueva

def recocido_simulado(esquema):
    ruta_actual = list(range(20))
    random.shuffle(ruta_actual)
    costo_actual = distancia(ruta_actual)
    mejor_costo = costo_actual
    
    T = 100
    T_min = 0.01
    historial_costos = []
    
    inicio = time.time()
    while T > T_min:
        nueva_ruta = vecino_2opt_aleatorio(ruta_actual)
        nuevo_costo = distancia(nueva_ruta)
        
        # Criterio de aceptación
        if nuevo_costo < costo_actual or random.random() < math.exp((costo_actual - nuevo_costo) / T):
            ruta_actual = nueva_ruta
            costo_actual = nuevo_costo
            if costo_actual < mejor_costo:
                mejor_costo = costo_actual
                
        historial_costos.append(costo_actual)
        
        # Enfriamiento
        if esquema == 'lineal':
            T -= 0.02
        elif esquema == 'exponencial':
            T *= 0.999
            
    fin = time.time()
    return historial_costos, mejor_costo, fin - inicio

print("--- Procesando Ejercicio 4 (Recocido Simulado) ---")
# Ejecutamos ambos esquemas
costos_lin, mejor_lin, tiempo_lin = recocido_simulado('lineal')
costos_exp, mejor_exp, tiempo_exp = recocido_simulado('exponencial')

# 1. Gráfica de Convergencia
plt.figure(figsize=(8, 5))
plt.plot(costos_lin, label='Lineal (T -= 0.02)', alpha=0.8)
plt.plot(costos_exp, label='Exponencial (T *= 0.999)', alpha=0.8)
plt.xlabel('Iteraciones')
plt.ylabel('Costo de la ruta (Distancia)')
plt.title('Curvas de Convergencia (Recocido Simulado)')
plt.legend()
ruta_conv = os.path.join(RESULTADOS_DIR, 'ejercicio4_convergencia.png')
plt.savefig(ruta_conv)
plt.show()

# 2. Gráfica Comparativa (Tiempo vs Calidad)
plt.figure(figsize=(7, 5))
plt.scatter([tiempo_lin], [mejor_lin], color='blue', label='Lineal', s=150, zorder=5)
plt.scatter([tiempo_exp], [mejor_exp], color='orange', label='Exponencial', s=150, zorder=5)
plt.xlabel('Tiempo de Cómputo (segundos)')
plt.ylabel('Costo Final (Menor es mejor)')
plt.title('Trade-off: Tiempo vs Calidad')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
ruta_tiempo = os.path.join(RESULTADOS_DIR, 'ejercicio4_tiempocalidad.png')
plt.savefig(ruta_tiempo)
plt.show()