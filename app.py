from flask import Flask, request, jsonify
import pandas as pd
import psycopg2
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

# Consulta SQL para obter os dados
query = "SELECT * FROM reflorestation_trees;"

# Criar DataFrame a partir dos resultados da consulta
df = pd.read_sql_query(query, conn)

# Normalizar os dados, se necessário
scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df[['grow_space', 'germination_time', 'time_to_adulthood', 'gas_ch4_reduction', 'ideal_soil_moisture', 'gas_c02_reduction']]), columns=[
                         'grow_space', 'germination_time', 'time_to_adulthood', 'gas_ch4_reduction', 'ideal_soil_moisture', 'gas_c02_reduction'])

conn.close()

# Escolher o número de clusters
num_clusters = 1

# Aplicar o algoritmo KMeans
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(df_scaled)


def recommend_trees(region_size, region_soil_moisture):
    # Normalizar o tamanho da região e umidade do solo
    region_data_scaled = scaler.transform(
        [[region_size, 0, 0, 0, region_soil_moisture, 0]])

    # Prever o cluster da região
    cluster = kmeans.predict(region_data_scaled)[0]

    # Filtrar as árvores no mesmo cluster e com umidade do solo semelhante
    cluster_trees = df[(df['cluster'] == cluster) & (df['ideal_soil_moisture'] >=
                                                     region_soil_moisture - 5) & (df['ideal_soil_moisture'] <= region_soil_moisture + 5)]

    # Calcular a quantidade ideal de árvores com base no tamanho da região
    cluster_trees['recommended_quantity'] = np.round(
        region_size / cluster_trees['grow_space']).astype(int)

    # Ordenar as recomendações com base em critérios diversos (por exemplo, grow_space e umidade do solo)
    cluster_trees = cluster_trees.sort_values(
        by=['grow_space', 'ideal_soil_moisture'])

    return cluster_trees


@app.route('/recommend-trees', methods=['POST'])
def recommend_trees_endpoint():
    data = request.get_json()

    # Verifica se os parâmetros necessários estão presentes no corpo da solicitação
    if 'region_size' not in data or 'region_soil_moisture' not in data:
        return jsonify({'error': 'Parâmetros ausentes'}), 400

    # Obtém os parâmetros da solicitação
    region_size = data['region_size']
    region_soil_moisture = data['region_soil_moisture']

    # Obtém a recomendação
    recommendation = recommend_trees(region_size, region_soil_moisture)

    # Retorna a recomendação como JSON
    return jsonify(recommendation.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)
