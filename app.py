from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

# Coloque suas credenciais do banco de dados aqui
DATABASE_URL = os.getenv("DB_STRING")

# Simula um banco de dados com dados de árvores
query = "SELECT * FROM reflorestation_trees;"
df = pd.read_sql_query(query, DATABASE_URL)
scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df[['grow_space', 'germination_time', 'time_to_adulthood', 'gas_ch4_reduction', 'ideal_soil_moisture', 'gas_c02_reduction']]), columns=[
                         'grow_space', 'germination_time', 'time_to_adulthood', 'gas_ch4_reduction', 'ideal_soil_moisture', 'gas_c02_reduction'])

# Escolha o número de clusters
num_clusters = 1

# Aplicar o algoritmo KMeans
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(df_scaled)


class Region(BaseModel):
    region_size: int
    region_soil_moisture: int


@app.post("/recommend-trees")
async def recommend_trees(region: Region):
    # Normalizar o tamanho da região e umidade do solo
    region_data_scaled = scaler.transform(
        [[region.region_size, 0, 0, 0, region.region_soil_moisture, 0]])

    # Prever o cluster da região
    cluster = kmeans.predict(region_data_scaled)[0]

    # Filtrar as árvores no mesmo cluster e com umidade do solo semelhante
    cluster_trees = df[(df['cluster'] == cluster) & (df['ideal_soil_moisture'] >=
                                                     region.region_soil_moisture - 5) & (df['ideal_soil_moisture'] <= region.region_soil_moisture + 5)]

    # Calcular a quantidade ideal de árvores com base no tamanho da região
    cluster_trees['recommended_quantity'] = np.round(
        region.region_size / cluster_trees['grow_space']).astype(int)

    # Ordenar as recomendações com base em critérios diversos (por exemplo, grow_space e umidade do solo)
    cluster_trees = cluster_trees.sort_values(
        by=['grow_space', 'ideal_soil_moisture'])

    return cluster_trees[['name', 'type', 'recommended_quantity']].to_dict(orient='records')
