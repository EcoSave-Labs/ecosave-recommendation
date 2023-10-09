# EcoSave Recommendation Tree
### Overview

This project leverages FastAPI, PostgreSQL, and machine learning techniques to provide a sustainable solution for reforestation efforts. The system recommends optimal tree species based on environmental conditions and monitors the growth and impact of these trees over time, integrating Internet of Things (IoT) devices.
Table of Contents

    Installation
    Usage
    Endpoints
    Technologies Used
    Acknowledgements

### Installation

    Clone the repository:

    bash

git clone https://github.com/EcoSave-Labs/ecosave-recommendation

Install dependencies:

bash

pip install -r requirements.txt

Create a .env file with the following variables:

### env

DB_HOST=your_database_host
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password

### Run the application:

bash

    uvicorn app:app --host 127.0.0.1 --port 8000 --reload

### Usage

The FastAPI application provides endpoints for recommending trees based on a specified region. Additionally, there's an endpoint to check the status of the recommendation system.

Access the Swagger documentation at http://127.0.0.1:8000/docs for detailed API documentation.
Endpoints

    GET /status: Check the status of the recommendation system.

    POST /recommend-trees: Get recommendations for tree planting based on a specified region.

### Technologies Used

    FastAPI: A modern, fast web framework for building APIs with Python.
    PostgreSQL: A powerful, open-source relational database system.
    scikit-learn: A machine learning library for data analysis and modeling.
    NumPy and Pandas: Libraries for numerical and data analysis.
    uvicorn: An ASGI server for running FastAPI applications.

### Acknowledgements

This project acknowledges the use of machine learning techniques, particularly the KMeans clustering algorithm, to enhance the recommendation system. The integration of IoT devices contributes to real-time monitoring and data collection for a more sustainable approach to reforestation.
