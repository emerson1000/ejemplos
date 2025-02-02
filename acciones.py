import yfinance as yf
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import alpaca_trade_api as tradeapi

# Configuración de Alpaca
API_KEY = 'tu_api_key_id'
API_SECRET = 'tu_secret_key'
BASE_URL = 'https://paper-api.alpaca.markets'  # Usa paper trading para pruebas

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# 1. Obtener datos de acciones
def obtener_datos_acciones(simbolos, inicio='2024-01-01', fin='2025-02-02'):
    datos = yf.download(simbolos, start=inicio, end=fin)['Adj Close']
    return datos

# 2. Filtrar acciones
def filtrar_acciones_dividendarias(simbolos, umbral_dividendo=0.03):
    acciones_dividendarias = []
    for simbolo in simbolos:
        accion = yf.Ticker(simbolo)
        if accion.info.get('dividendYield') is not None and accion.info['dividendYield'] >= umbral_dividendo:
            acciones_dividendarias.append(simbolo)
    return acciones_dividendarias

def filtrar_acciones_crecimiento(simbolos, beta_min=0.8, beta_max=1.5):
    acciones_crecimiento = []
    for simbolo in simbolos:
        accion = yf.Ticker(simbolo)
        if accion.info.get('beta') is not None and beta_min <= accion.info['beta'] <= beta_max:
            acciones_crecimiento.append(simbolo)
    return acciones_crecimiento

# 3. Calcular métricas financieras
def calcular_metricas(datos):
    retornos = datos.pct_change().dropna()
    rentabilidad_esperada = retornos.mean() * 252
    matriz_covarianza = retornos.cov() * 252
    return rentabilidad_esperada, matriz_covarianza

# 4. Optimización de cartera (Markowitz)
def optimizar_cartera(rentabilidad_esperada, matriz_covarianza, capital=10000):
    num_activos = len(rentabilidad_esperada)
    args = (rentabilidad_esperada, matriz_covarianza)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_activos))
    resultado = minimize(fun=calcular_riesgo, x0=np.array(num_activos * [1. / num_activos]),
                         args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    pesos_optimos = resultado.x
    return pesos_optimos

def calcular_riesgo(pesos, rentabilidad_esperada, matriz_covarianza):
    return np.sqrt(np.dot(pesos.T, np.dot(matriz_covarianza, pesos)))

# 5. Ejecutar órdenes en Alpaca
def ejecutar_ordenes(cartera, pesos_optimos, capital):
    for simbolo, peso in zip(cartera, pesos_optimos):
        if peso > 0:  # Solo ejecutar órdenes para pesos positivos
            monto_inversion = capital * peso
            try:
                # Obtener el precio actual de la acción
                precio_actual = api.get_latest_trade(simbolo).price
                cantidad = int(monto_inversion / precio_actual)  # Calcular la cantidad de acciones
                if cantidad > 0:
                    # Ejecutar orden de compra
                    api.submit_order(
                        symbol=simbolo,
                        qty=cantidad,
                        side='buy',
                        type='market',
                        time_in_force='day'
                    )
                    print(f"Orden de compra ejecutada: {cantidad} acciones de {simbolo} por ${monto_inversion:.2f}")
            except Exception as e:
                print(f"Error al ejecutar orden para {simbolo}: {e}")

# 6. Ejecutar el programa
def ejecutar_programa():
    # Lista de símbolos de acciones (ejemplo: S&P 500)
    simbolos = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'JNJ', 'PG', 'V', 'WMT', 'DIS']
    
    # Filtrar acciones
    acciones_dividendarias = filtrar_acciones_dividendarias(simbolos)
    acciones_crecimiento = filtrar_acciones_crecimiento(simbolos)
    
    # Combinar acciones
    cartera = acciones_dividendarias[:int(0.7 * len(acciones_dividendarias))] + \
              acciones_crecimiento[:int(0.3 * len(acciones_crecimiento))]
    
    # Obtener datos
    datos = obtener_datos_acciones(cartera)
    
    # Calcular métricas
    rentabilidad_esperada, matriz_covarianza = calcular_metricas(datos)
    
    # Optimizar cartera
    pesos_optimos = optimizar_cartera(rentabilidad_esperada, matriz_covarianza)
    
    # Mostrar resultados
    print("Pesos óptimos de la cartera:")
    for simbolo, peso in zip(cartera, pesos_optimos):
        print(f"{simbolo}: {peso * 100:.2f}%")
    
    # Ejecutar órdenes en Alpaca
    capital = 10000  # Capital inicial
    ejecutar_ordenes(cartera, pesos_optimos, capital)

# Ejecutar el programa
ejecutar_programa()