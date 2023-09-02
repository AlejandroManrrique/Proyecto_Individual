
import pandas as pd
import ast

df_steam = pd.read_csv('./Data/steam_games.csv')

df_items = pd.read_parquet('./Data/items.parquet')

df_reviews = pd.read_csv('./Data/reviews.csv')

df_steam['id'].fillna(0, inplace=True)  # Llena los valores NaN con 0
df_steam['id'] = df_steam['id'].astype(int)  # Convierte a enteros

from fastapi import FastAPI
from typing import Dict

# Crea una instancia de FastAPI
app = FastAPI()




# Nueva función userdata
@app.get("/userdata/{user_id}")
async def userdata(user_id: str):
    try:
        # Filtra las revisiones del usuario específico
        user_reviews = df_reviews[df_reviews['user_id'] == user_id]

        # Filtra los juegos jugados por el usuario
        game_ids = user_reviews['item_id'].unique()
        user_steam_games = df_steam[df_steam['id'].astype(int).isin(game_ids)]

        # Calcula la cantidad de dinero gastado por el usuario
        user_steam_games['price'] = user_steam_games['price'].apply(lambda x: float(x.replace('$', '').replace(',', '')) if x.replace('$', '').replace(',', '').replace('.', '').isdigit() else None)
        money_spent = user_steam_games['price'].sum()

        # Calcula el porcentaje de recomendación promedio de los juegos jugados por el usuario
        user_reviews['recommend'] = user_reviews['recommend'].astype(bool)
        recommend_percentage = user_reviews['recommend'].mean() * 100

        # Calcula la cantidad de items que posee el usuario
        num_items = len(game_ids)

        # Crear un diccionario con los resultados
        user_data = {
            "money_spent": money_spent,
            "recommend_percentage": recommend_percentage,
            "num_items": num_items
        }

        return user_data
    except ValueError:
        # Si no se puede convertir a entero, manejar el caso de cadena
        # Buscar el user_id en el DataFrame para verificar su existencia
        if user_id in df_reviews['user_id'].values:
            # Realizar cálculos basados en el user_id encontrado
            user_reviews = df_reviews[df_reviews['user_id'] == user_id]

            # Filtra los juegos jugados por el usuario
            game_ids = user_reviews['item_id'].unique()
            user_steam_games = df_steam[df_steam['id'].astype(int).isin(game_ids)]

            # Calcula la cantidad de dinero gastado por el usuario
            user_steam_games['price'] = user_steam_games['price'].apply(lambda x: float(x.replace('$', '').replace(',', '')) if x.replace('$', '').replace(',', '').replace('.', '').isdigit() else None)
            money_spent = user_steam_games['price'].sum()

            # Calcula el porcentaje de recomendación promedio de los juegos jugados por el usuario
            user_reviews['recommend'] = user_reviews['recommend'].astype(bool)
            recommend_percentage = user_reviews['recommend'].mean() * 100

            # Calcula la cantidad de items que posee el usuario
            num_items = len(game_ids)

            # Crear un diccionario con los resultados
            user_data = {
                "money_spent": money_spent,
                "recommend_percentage": recommend_percentage,
                "num_items": num_items
            }

            return user_data
        else:
            return {"message": "Usuario no encontrado"}
