import yfinance as yf
import gspread
from google.oauth2.service_account import Credentials

# Función para obtener los datos financieros usando Yahoo Finance
def obtener_datos_financieros(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.info
        return {
            "Tipo": "Acción" if symbol.isupper() else "Criptomoneda",
            "Precio Actual": data.get('currentPrice', 'not found'),
            "Máximo Histórico": data.get('dayHigh', 'not found'),
            "Mínimo Histórico": data.get('dayLow', 'not found'),
            "Volumen": data.get('volume', 'not found'),
            "Promedio Móvil de 50 días": data.get('fiftyDayAverage', 'not found'),
            "Promedio Móvil de 200 días": data.get('twoHundredDayAverage', 'not found'),
            "Ratio P/E": data.get('trailingPE', 'not found'),
            "Valor de Mercado Actual": data.get('marketCap', 'not found'),
            "Dividendo por Acción": data.get('dividendRate', 'not found'),
            "Rendimiento del Dividendo": data.get('dividendYield', 'not found'),
            "Beta": data.get('beta', 'not found'),
            "Promedio de Volumen de 10 días": data.get('averageVolume10days', 'not found'),
            "Número de Acciones Totales": data.get('sharesOutstanding', 'not found'),
            "Acciones Flotantes": data.get('floatShares', 'not found'),
            "EPS": data.get('trailingEps', 'not found'),
            "Book Value": data.get('bookValue', 'not found'),
            "PEG Ratio": data.get('pegRatio', 'not found'),
            "Price/Sales": data.get('priceToSalesTrailing12Months', 'not found'),
            "Price/Book": data.get('priceToBook', 'not found'),
            "ROA": data.get('returnOnAssets', 'not found'),
            "ROE": data.get('returnOnEquity', 'not found'),
            "Debt/Equity": data.get('debtToEquity', 'not found'),
            "Operating Margins": data.get('operatingMargins', 'not found'),
            "Revenue Growth": data.get('revenueGrowth', 'not found'),
            "Dividend Payout Ratio": data.get('payoutRatio', 'not found'),
            "Forward Dividend Yield": data.get('forwardPE', 'not found'),  # Puede que necesites ajustar este campo
            "Recommendation Key": data.get('recommendationKey', 'not found'),
            "Target Mean Price": data.get('targetMeanPrice', 'not found'),
            "Cash Flow": data.get('freeCashflow', 'not found'),
            "Sector & Industry": f"{data.get('sector', 'not found')} - {data.get('industry', 'not found')}",
        }
    except Exception as e:
        print(f"No se encontraron datos para {symbol}: {e}")
        return {key: 'not found' for key in headers[1:]}

# Autenticación con Google Sheets
creds_json_path = 'pdx-web-prd-a85fc8803a70.json'  # Asegúrate de que la ruta esté correcta
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(creds_json_path, scopes=scope)
client = gspread.authorize(creds)

# Acceder a la hoja de Google Sheets
sheet_id = '1DNWdVa_fKZAU87FEnzgPYZ3C-gnP3vx3GyGCVBzz-Y8'
sheet_name = 'Acciones'
sheet = client.open_by_key(sheet_id).worksheet(sheet_name)

# Encabezados para análisis de acciones
headers = [
    "Tipo", "Precio Actual", "Máximo Histórico", "Mínimo Histórico", "Volumen",
    "Promedio Móvil de 50 días", "Promedio Móvil de 200 días", "Ratio P/E",
    "Valor de Mercado Actual", "Dividendo por Acción", "Rendimiento del Dividendo",
    "Beta", "Promedio de Volumen de 10 días", "Número de Acciones Totales",
    "Acciones Flotantes", "EPS", "Book Value", "PEG Ratio", "Price/Sales",
    "Price/Book", "ROA", "ROE", "Debt/Equity", "Operating Margins", "Revenue Growth",
    "Dividend Payout Ratio", "Forward Dividend Yield", "Recommendation Key",
    "Target Mean Price", "Cash Flow", "Sector & Industry"
]

# Obtener todas las siglas de acciones de la columna B (excepto el encabezado)
symbols = sheet.col_values(2)[1:]  # Comienza después del encabezado

# Procesamiento de símbolos
total_symbols = len(symbols)
symbols_processed = 0
symbols_failed = 0

print("Procesando símbolos...")

for i, symbol in enumerate(symbols, start=2):  # Comienza en la segunda fila
    print(f"Procesando {symbol}...")
    datos_financieros = obtener_datos_financieros(symbol)
    if datos_financieros['Precio Actual'] != 'not found':
        # La lista de datos a actualizar en la hoja
        row_values = [datos_financieros['Tipo']] + list(datos_financieros.values())[1:]
        sheet.update(f'C{i}:AG{i}', [row_values], value_input_option='USER_ENTERED')
        symbols_processed += 1
    else:
        sheet.update(f'C{i}:AG{i}', [['not found'] * len(headers)], value_input_option='USER_ENTERED')
        symbols_failed += 1

# Resumen de resultados
print("\nProcesamiento completado.")
print(f"Total de símbolos: {total_symbols}")
print(f"Símbolos actualizados con éxito: {symbols_processed}")
print(f"Errores en símbolos: {symbols_failed}")
