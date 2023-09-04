import pandas as pd
from fastapi import FastAPI

df_steam = pd.read_csv('./Data/steam_games.csv')

# Realiza la conversión de precio en df_steam
df_steam['price'] = df_steam['price'].apply(lambda x: float(x.replace('$', '').replace(',', '')) if isinstance(x, str) and x.replace('$', '').replace(',', '').replace('.', '').isdigit() else 0.0)

# Otras lecturas de datos...

app = FastAPI()

@app.get("/userdata/{user_id}")
async def userdata(user_id: str):
    try:
        money_spent = 0
        recommend_count = 0
        total_reviews = 0
        item_ids = set()

        # Configura el tamaño del lote para la lectura de reseñas
        chunk_size = 100000
        user_reviews_generator = pd.read_csv('./Data/reviews.csv', chunksize=chunk_size)

        for chunk in user_reviews_generator:
            user_reviews = chunk[chunk['user_id'] == user_id]

            # Procesa los datos del lote actual
            money_spent += user_reviews.merge(df_steam[['id', 'price']], left_on='item_id', right_on='id', how='inner')['price'].sum()
            recommend_count += user_reviews['recommend'].sum()
            total_reviews += len(user_reviews)
            item_ids.update(user_reviews['item_id'].unique())

        if total_reviews > 0:
            recommend_percentage = (recommend_count / total_reviews) * 100
        else:
            recommend_percentage = 0

        num_items = len(item_ids)

        user_data = {
            "money_spent": money_spent,
            "recommend_percentage": recommend_percentage,
            "num_items": num_items
        }

        return user_data

    except Exception as e:
        return {"message": f"Error: {str(e)}"}
import psutil


