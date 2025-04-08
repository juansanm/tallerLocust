import os
import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
app = FastAPI(title="API- Inferencia de Modelo ML", 
              description="Realizar inferencias usando un modelo de MLflow")
MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MODEL_NAME = os.environ.get("MODEL_NAME", "modelo-prediccion")
MODEL_STAGE = os.environ.get("MODEL_STAGE", "Production")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
try:
    model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/{MODEL_STAGE}")
    print(f"Modelo cargado {MODEL_NAME}/{MODEL_STAGE}")
except Exception as e:
    print(f"Error en {e}")
    model = None
class PredictionInput(BaseModel):
    features: List[float]
@app.get("/health")
def health_check():
    if model is None:
        raise HTTPException(status_code=503, detail="El modelo no está disponible")
    return {"status": "ok", "model": f"{MODEL_NAME}/{MODEL_STAGE}"}
@app.post("/predict", response_model=Dict[str, Any])
async def predict(input_data: PredictionInput):
    if model is None:
        raise HTTPException(status_code=503, 
                           detail="El modelo no está disponible para inferencia")
    
    try:
        input_df = pd.DataFrame([input_data.features])
        prediction = model.predict(input_df)   
        return {
            "prediction": prediction.tolist() if hasattr(prediction, "tolist") else prediction,
            "model": f"{MODEL_NAME}/{MODEL_STAGE}",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, 
                           detail=f"Error durante la inferencia: {str(e)}")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)