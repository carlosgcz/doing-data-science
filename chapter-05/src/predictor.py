# -*- coding: utf-8 -*-
import joblib
import pandas as pd
import json
import os
from typing import Dict, Union

# --- Configuración de Rutas ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Rutas relativas a la carpeta 'src'
MODEL_PATH = os.path.join(BASE_DIR, '../models/ctr_champion_model.joblib')
FEATURES_PATH = os.path.join(BASE_DIR, '../models/champion_model_features.json')
# Ruta a los datos originales (para prueba real)
DATA_PATH = os.path.join(BASE_DIR, '../data/raw/dds_ch5_binary-class-dataset.txt')

class CTRPredictor:
    def __init__(self):
        self.model = None
        self.features = None
        self._load_artifacts()

    def _load_artifacts(self):
        try:
            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError(f"No se encuentra el modelo en: {MODEL_PATH}")

            self.model = joblib.load(MODEL_PATH)
            with open(FEATURES_PATH, 'r') as f:
                self.features = json.load(f)
            print(" Sistema de Predicción Inicializado.")
        except Exception as e:
            print(f" Error fatal cargando modelo: {e}")

    def predict(self, user_data: Union[Dict, pd.DataFrame]) -> float:
        if not self.model: return -1.0

        try:
            # 1. Convertir a DataFrame si es diccionario
            if isinstance(user_data, dict):
                data = pd.DataFrame([user_data])
            else:
                data = user_data.copy()

            # 2. Validar columnas
            if not all(col in data.columns for col in self.features):
                missing = list(set(self.features) - set(data.columns))
                # Solo advertimos, no bloqueamos, para facilitar pruebas
                # (En producción estricta, aquí se retornaría error)
                # print(f"Advertencia: Faltan features: {missing}")
                pass

            # 3. Asegurar que solo pasamos las columnas que el modelo conoce
            # (Si el dataframe tiene 'y_buy' u otras extras, las ignora)
            data = data[self.features]

            # 4. Predecir
            prob = self.model.predict_proba(data)[:, 1][0]
            return float(prob)

        except Exception as e:
            print(f"Error en predicción: {e}")
            return -1.0

if __name__ == "__main__":
    # --- PRUEBA CON DATOS REALES DEL ARCHIVO ---
    print("---  INICIANDO PRUEBA CON DATOS REALES ---")

    predictor = CTRPredictor()

    if os.path.exists(DATA_PATH):
        print(f" Cargando datos desde: {DATA_PATH} ...")
        # Leemos el archivo real
        df_real = pd.read_csv(DATA_PATH, sep='	')

        # 1. Tomamos un usuario que REALMENTE HIZO CLIC (y_buy = 1)
        try:
            user_click = df_real[df_real['y_buy'] == 1].sample(1).to_dict(orient='records')[0]
            print("\n CASO 1: Usuario Real que HIZO CLICK (Target=1)")
            prob = predictor.predict(user_click)
            print(f"   -> Probabilidad Predicha: {prob:.4%} (Esperamos que sea ALTA)")
        except:
            print("No se encontraron usuarios con click en la muestra.")

        # 2. Tomamos un usuario que NO HIZO CLIC (y_buy = 0)
        try:
            user_no_click = df_real[df_real['y_buy'] == 0].sample(1).to_dict(orient='records')[0]
            print("\n CASO 2: Usuario Real que NO HIZO CLICK (Target=0)")
            prob = predictor.predict(user_no_click)
            print(f"   -> Probabilidad Predicha: {prob:.4%} (Esperamos que sea BAJA)")
        except:
            print("Error al muestrear usuario sin click.")

    else:
        print(f" No se encontró el archivo de datos en {DATA_PATH} para hacer la prueba real.")
