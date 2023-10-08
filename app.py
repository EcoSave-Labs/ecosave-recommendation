from fastapi import FastAPI, HTTPException
import psycopg2
from pydantic import BaseModel
from typing import List, Union
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Create a FastAPI instance
app = FastAPI()

# Connect to the database
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

# SQL query to retrieve data from the 'reflorestation_trees' table
query = "SELECT * FROM reflorestation_trees;"

# Create a DataFrame from the query results
df = pd.read_sql_query(query, conn)

# Standardize numerical features using StandardScaler
scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df[['grow_space', 'germination_time', 'time_to_adulthood', 'gas_ch4_reduction', 'ideal_soil_moisture', 'gas_c02_reduction']]), columns=[
                         'grow_space', 'germination_time', 'time_to_adulthood', 'gas_ch4_reduction', 'ideal_soil_moisture', 'gas_c02_reduction'])

# Close the database connection
conn.close()

# Choose the number of clusters for KMeans
num_clusters = 1

# Apply the KMeans algorithm
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(df_scaled)

# Define the Pydantic model for a Tree


class Tree(BaseModel):
    name: str
    type: str
    recommended_quantity: int
    grow_space: float
    germination_time: int
    time_to_adulthood: int
    gas_ch4_reduction: float
    ideal_soil_moisture: float
    gas_c02_reduction: float

# Define the Pydantic model for a Region


class Region(BaseModel):
    region_size: int
    region_soil_moisture: int

# Endpoint to recommend trees based on a region

@app.get("/status")
async def recommend_trees_status():
    return 'ok'

@app.post("/recommend-trees", response_model=List[Tree])
async def recommend_trees(region: Region):
    # Normalize the region size and soil moisture
    region_data_scaled = scaler.transform(
        [[region.region_size, 0, 0, 0, region.region_soil_moisture, 0]])

    # Predict the cluster of the region
    cluster = kmeans.predict(region_data_scaled)[0]

    # Filter trees in the same cluster with similar soil moisture
    cluster_trees = df[(df['cluster'] == cluster) & (df['ideal_soil_moisture'] >=
                                                     region.region_soil_moisture - 5) & (df['ideal_soil_moisture'] <= region.region_soil_moisture + 5)]

    # Calculate the recommended quantity of trees based on the region size
    cluster_trees['recommended_quantity'] = np.round(
        region.region_size / cluster_trees['grow_space']).astype(int)

    # Sort the recommendations based on various criteria (e.g., grow_space and soil moisture)
    cluster_trees = cluster_trees.sort_values(
        by=['grow_space', 'ideal_soil_moisture'])

    # Convert the DataFrame to a list of dictionaries
    result_trees = cluster_trees.to_dict(orient='records')

    # Return the recommended trees
    return result_trees
