"""
Este script descarga información financiera de ciertas acciones y criptomonedas
utilizando la librería yfinance. Luego, genera un archivo CSV con la fecha del día
en el nombre, almacenando datos clave como precio actual, volumen, ROA, ROE, etc.

Requisitos:
- Instalar dependencias antes de ejecutar: `pip install -r requirements.txt`
"""

import yfinance as yf
import csv
import os
from datetime import datetime
from tqdm import tqdm

# Obtén la fecha actual en formato YYYY-MM-DD
fecha_hoy = datetime.now().strftime('%Y-%m-%d')

# Define el nombre del archivo CSV de salida
nombre_archivo = f"{fecha_hoy}-stocks.csv"

# Lista de símbolos a analizar
symbols = [
    "AAPL",    # Apple
    "MSFT",    # Microsoft
    "GOOGL",   # Alphabet (Google)
    "TSLA",    # Tesla
    "AMZN",    # Amazon
    "NFLX",    # Netflix
    "NVDA",    # NVIDIA
    "BTC-USD", # Bitcoin
    "ETH-USD"  # Ethereum
]

# Encabezados del archivo CSV
headers = [
    "Símbolo", "Tipo", "Precio Actual", "Máximo Diario", "Mínimo Diario", 
    "Volumen", "ROA", "ROE", "Market Cap", "Beta", "P/E Ratio"
]

def obtener_datos_financieros(symbol):
    """
    Obtiene los datos financieros de un símbolo desde Yahoo Finance.
    Devuelve una lista con la información ordenada acorde a los 'headers'.
    """
    try:
        stock = yf.Ticker(symbol)
        data = stock.info

        # Determina si es una acción o criptomoneda
        tipo = "Acción" if symbol.isupper() else "Criptomoneda"

        return [
            symbol, tipo,
            data.get('currentPrice', 'N/A'),
            data.get('dayHigh', 'N/A'),
            data.get('dayLow', 'N/A'),
            data.get('volume', 'N/A'),
            data.get('returnOnAssets', 'N/A'),
            data.get('returnOnEquity', 'N/A'),
            data.get('marketCap', 'N/A'),
            data.get('beta', 'N/A'),
            data.get('trailingPE', 'N/A')
        ]
    except Exception as e:
        print(f"⚠️ Error al obtener datos de {symbol}: {e}")
        return [symbol, "N/A"] + ["N/A"] * (len(headers) - 2)

def main():
    """
    Crea un archivo CSV y guarda los datos de cada símbolo en él.
    """
    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Escribir encabezados

        # Iterar los símbolos con tqdm para mostrar barra de progreso
        for symbol in tqdm(symbols, desc="📊 Procesando símbolos", unit="símbolo"):
            datos = obtener_datos_financieros(symbol)
            writer.writerow(datos)  

    print(f"\n✅ Datos guardados en {nombre_archivo}")

if __name__ == "__main__":
    main()
