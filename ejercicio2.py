import os
import matplotlib.pyplot as plt
import pandas as pd


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTADOS_DIR = os.path.join(SCRIPT_DIR, '..', 'resultados')
os.makedirs(RESULTADOS_DIR, exist_ok=True)

# Instancia diseñada para que "menor peso" sea peor que "valor/peso"
objetos = [
    {"nombre": "A (Oro pesado)", "peso": 50, "valor": 100},
    {"nombre": "B (Piedra)", "peso": 10, "valor": 10},
    {"nombre": "C (Piedra)", "peso": 10, "valor": 10},
    {"nombre": "D (Piedra)", "peso": 10, "valor": 10},
    {"nombre": "E (Piedra)", "peso": 10, "valor": 10},
    {"nombre": "F (Piedra)", "peso": 10, "valor": 10}
]
capacidad = 50

def mochila_greedy(items, cap, criterio):
    if criterio == "menor_peso":
        items_ordenados = sorted(items, key=lambda x: x["peso"])
    elif criterio == "valor_peso":
        items_ordenados = sorted(items, key=lambda x: x["valor"]/x["peso"], reverse=True)
        
    peso_actual = 0
    valor_total = 0
    seleccionados = []
    
    for item in items_ordenados:
        if peso_actual + item["peso"] <= cap:
            peso_actual += item["peso"]
            valor_total += item["valor"]
            seleccionados.append(item["nombre"])
            
    return valor_total, peso_actual, seleccionados

# Ejecutar ambos métodos
val_peso, peso_usado_P, sel_P = mochila_greedy(objetos, capacidad, "menor_peso")
val_VP, peso_usado_VP, sel_VP = mochila_greedy(objetos, capacidad, "valor_peso")

print("--- Resultados Ejercicio 2 ---")
print(f"MÉTODO MENOR PESO: Valor = {val_peso} | Peso = {peso_usado_P} | Items: {sel_P}")
print(f"MÉTODO VALOR/PESO: Valor = {val_VP} | Peso = {peso_usado_VP} | Items: {sel_VP}")

# Gráfica
data = {'Método': ['Menor Peso Primero', 'Mayor Valor/Peso Primero'],
        'Valor Total': [val_peso, val_VP]}
df = pd.DataFrame(data)

plt.figure(figsize=(7, 5))
barras = plt.bar(df['Método'], df['Valor Total'], color=['#e74c3c', '#2ecc71'])
plt.title('Comparación de Criterios en la Mochila Greedy')
plt.ylabel('Valor Total Obtenido')

# Agregar valores arriba de las barras
for barra in barras:
    yval = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, yval + 2, f'Valor: {yval}', ha='center', va='bottom')

# Guardado seguro
ruta_guardado = os.path.join(RESULTADOS_DIR, 'ejercicio2_mochila.png')
plt.savefig(ruta_guardado)
plt.show()