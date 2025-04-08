FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
ENV MLFLOW_TRACKING_URI="http://mlflow:5000"
ENV MODEL_NAME="modelo-prediccion"
ENV MODEL_STAGE="Production"
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]