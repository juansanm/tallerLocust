from locust import HttpUser, task, between
import json
import random
class MLInferenceUser(HttpUser):
    wait_time = between(0.5, 3)
    def on_start(self):
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"API no disponible: {response.text}")
    
    @task
    def predict(self):
        features = [random.uniform(0, 10) for _ in range(4)]
        
        payload = {
            "features": features
        }      
        headers = {"Content-Type": "application/json"}

        with self.client.post(
            "/predict", 
            data=json.dumps(payload),
            headers=headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if "prediction" not in result:
                        response.failure("Respuesta sin predicción")
                except json.JSONDecodeError:
                    response.failure("Respuesta no es JSON válido")
            else:
                response.failure(f"Error {response.text}")