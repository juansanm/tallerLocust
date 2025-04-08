## Pruebas de Carga con Locust para API de ML 

Este proyecto implementa pruebas de carga utilizando Locust para una API de inferencia de Machine Learning basada en FastAPI y MLflow.

Autor

Juan Felipe Gonzalez Sanmiguel



El proyecto consta de varios componentes:

Una API de inferencia desarrollada con FastAPI que consume un modelo entrenado almacenado en MLflow
Una imagen Docker de la API publicada en DockerHub
Configuración de docker-compose para desplegar la API
Configuración de docker-compose para realizar pruebas de carga con Locust
Scripts para optimizar los recursos del contenedor y analizar la resistencia de la API

Requisitos

Docker y Docker Compose
Python 3.9 o superior (para desarrollo local)
Una instancia de MLflow con un modelo entrenado

Configuración
Variables de Entorno
La API utiliza las siguientes variables de entorno:

MLFLOW_TRACKING_URI: URL del servidor de MLflow (por defecto: "http://mlflow:5000")
MODEL_NAME: Nombre del modelo en MLflow (por defecto: "modelo-prediccion")
MODEL_STAGE: Etapa del modelo en MLflow (por defecto: "Production")

Uso
1. Desplegar la API
bashCopydocker-compose up -d
La API estará disponible en http://localhost:8000
2. Realizar pruebas de carga
bashCopydocker-compose -f docker-compose.locust.yaml up --build
La interfaz web de Locust estará disponible en http://localhost:8089
3. Optimizar recursos
El script optimize_resources.sh permite encontrar la configuración óptima de recursos:
bashCopychmod +x optimize_resources.sh
./optimize_resources.sh
API Endpoints

GET /health: Verifica el estado de la API y del modelo
POST /predict: Realiza una inferencia con el modelo

Ejemplo de solicitud a /predict:
jsonCopy{
  "features": [5.1, 3.5, 1.4, 0.2]
}



## Procedimiento de Prueba

Abrir la interfaz web de Locust (http://localhost:8089)
Configurar la prueba:

Number of users: 10000
Spawn rate: 500 (usuarios/segundo)


Resultados
Durante las pruebas, se encontró que la configuración mínima para soportar 10,000 usuarios con una tasa de adición de 500 usuarios por segundo es medio core con un réplica


Conclusiones

La API puede manejar eficientemente 10,000 usuarios concurrentes con una tasa de llegada de 500 usuarios/segundo utilizando recursos mínimos.
El escalamiento horizontal (aumentar réplicas) resultó ser más eficiente que el escalamiento vertical (aumentar recursos por réplica).
Para cargas de trabajo de alta concurrencia, se recomienda utilizar al menos 3 réplicas con recursos moderados en lugar de pocas réplicas con muchos recursos.

Referencias

Clase de Dr.Cris Diaz
