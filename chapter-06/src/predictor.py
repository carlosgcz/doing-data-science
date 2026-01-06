import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.linear_model import Ridge  # <--- CAMBIO 1: Usamos Ridge
import joblib
import os
from datetime import datetime

class FinancialPredictor:
    def __init__(self, ticker="SPY", lags=2):
        self.ticker = ticker
        self.lags = lags
        # CAMBIO 2: Regularización. alpha=0.5 hace que el modelo sea 'escéptico' al ruido.
        self.model = Ridge(alpha=0.5) 
        self.data = None
        self.features = []
        self.model_path = f"models/{ticker}_ridge_model.joblib"
        os.makedirs("models", exist_ok=True)

    def fetch_data(self, start_date="2015-01-01"): # Usamos menos historia pero más reciente
        print(f"--> Descargando datos para {self.ticker}...")
        end_date = datetime.now().strftime('%Y-%m-%d')
        df = yf.download(self.ticker, start=start_date, end=end_date, progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        if 'Adj Close' not in df.columns:
             df['Adj Close'] = df['Close']
        self.data = df
        return self

    def preprocess(self):
        if self.data is None: raise ValueError("Data missing")
        df = self.data.copy()
        
        # Target
        df['log_ret'] = np.log(df['Adj Close'] / df['Adj Close'].shift(1))
        
        # Features Básicas (Lags)
        self.features = []
        for lag in range(1, self.lags + 1):
            col = f'lag_{lag}'
            df[col] = df['log_ret'].shift(lag)
            self.features.append(col)
            
        # CAMBIO 3: Feature Engineering (Tendencia y Volatilidad)
        # Promedio móvil de 5 días (Tendencia semanal)
        df['trend_5'] = df['log_ret'].rolling(window=5).mean().shift(1)
        self.features.append('trend_5')
        
        # Volatilidad de 5 días (Miedo en el mercado)
        df['vol_5'] = df['log_ret'].rolling(window=5).std().shift(1)
        self.features.append('vol_5')

        df.dropna(inplace=True)
        self.data = df
        return self

    def train(self):
        X = self.data[self.features]
        y = self.data['log_ret']
        
        print(f"--> Entrenando RIDGE con Features: {self.features}")
        self.model.fit(X, y)
        joblib.dump(self.model, self.model_path)
        
        print(f"   Intercepto: {self.model.intercept_:.6f}")
        print(f"   Coeficientes: {self.model.coef_}")
        return self

    def predict_tomorrow(self):
        # Para predecir mañana, necesitamos los datos de HOY
        last_row = self.data.iloc[-1]
        
        # Construimos el vector de entrada con las mismas features usadas en train
        input_data = []
        
        # 1. Lags: (Hoy es lag_1 para mañana, Ayer es lag_2...)
        # Truco: Tomamos los últimos 'lags' valores de log_ret y los invertimos
        current_lags = self.data['log_ret'].iloc[-self.lags:].values[::-1]
        input_data.extend(current_lags)
        
        # 2. Trend (El promedio de los últimos 5 días hasta hoy)
        input_data.append(self.data['log_ret'].iloc[-5:].mean())
        
        # 3. Vol (La std dev de los últimos 5 días hasta hoy)
        input_data.append(self.data['log_ret'].iloc[-5:].std())
        
        X_new = np.array(input_data).reshape(1, -1)
        
        pred = self.model.predict(X_new)[0]
        signal = "COMPRAR" if pred > 0 else "VENDER"
        
        print(f"\n=== PRONÓSTICO ROBUSTO ({self.ticker}) ===")
        print(f"Features: {self.features}")
        print(f"Valores de Entrada: {np.round(input_data, 5)}")
        print(f"Predicción (Log Return): {pred:.6f}")
        print(f"Señal: {signal}")
        print("==========================================")

if __name__ == "__main__":
    FinancialPredictor("SPY", lags=2).fetch_data().preprocess().train().predict_tomorrow()