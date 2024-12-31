# backend/main.py
from fastapi import FastAPI, HTTPException, Body, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import time

app = FastAPI()

# Dictionary to store trained models
models = {}
active_connections: List[WebSocket] = []

class PredictRequest(BaseModel):
    model_name: str
    test_data: List[List[float]]

class SensorData(BaseModel):
    time: float
    accelX: float
    accelY: float
    accelZ: float
    rotationRateAlphaRad: float
    rotationRateBetaRad: float
    rotationRateGammaRad: float
    magnitude:float


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received data: {data}")  # Log the raw data

            sensor_data = parse_sensor_data(data)  # Parse the received data

            if sensor_data is None:
                print("Failed to parse sensor data. Skipping prediction.")
                continue  # Skip this iteration if parsing failed

            # If you need to predict based on sensor data
            prediction_result = await make_prediction(sensor_data)

            # Broadcast received data and predictions to all connections
            for connection in active_connections:
                await connection.send_text(f"Data: {data}, Prediction: {prediction_result}") 
    except WebSocketDisconnect:
        active_connections.remove(websocket)


@app.post("/sensor/")
async def receive_sensor_data(data: SensorData):
    print(f"Received sensor data: {data}")
    return {"message": "Sensor data received", "data": data}

@app.post("/train/")
async def train_model(file: bytes = Body(...), model_name: str = "random_forest"):
    temp_file_path = "AIfalling.xlsx"
    with open(temp_file_path, "wb") as f:
        f.write(file)

    df = pd.read_excel(temp_file_path, engine='openpyxl')
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values

    model = RandomForestClassifier()
    model.fit(X, y)

    models[model_name] = model
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    return {"message": f"Training complete with model = {model_name} trained on data from {temp_file_path} at {current_time}"}

@app.post("/predict/")
async def predict(request: PredictRequest):
    if request.model_name not in models:
        raise HTTPException(status_code=404, detail="Model not found")

    model = models[request.model_name]
    predictions = model.predict(request.test_data)
    
    return {"predictions": predictions.tolist()}

@app.get("/")
async def get():
    return HTMLResponse(open("index.html").read())

def parse_sensor_data(data: str) -> SensorData:
    """Parse incoming sensor data from JSON string to SensorData object."""
    import json
    try:
        json_data = json.loads(data)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

    # Extract motion data from the received JSON structure
    motion = json_data.get('motion')
    if motion is None:
        print("Invalid data: 'motion' key not found")
        return None

    try:
        # Use get with default values to avoid key errors
        return SensorData(
            time=float(motion.get('time', 0)),  # New: include time
            accelX=float(motion.get('accelerationX', 0)),  # Default to 0 if not found
            accelY=float(motion.get('accelerationY', 0)),  # Default to 0 if not found
            accelZ=float(motion.get('accelerationZ', 0)),  # Default to 0 if not found
            rotationRateAlphaRad=float(motion.get('rotationRateAlphaRad', 0)),
            rotationRateBetaRad=float(motion.get('rotationRateBetaRad', 0)),
            rotationRateGammaRad=float(motion.get('rotationRateGammaRad', 0)),
            magnitude=float(motion.get('magnitude', 0))  # New: include magnitude
        )
    except (ValueError, TypeError) as e:
        print(f"Error converting motion data to float: {e}")
        return None


async def make_prediction(sensor_data: SensorData):
    """Make a prediction using the sensor data."""
    # Check if sensor_data is None
    if sensor_data is None:
        print("sensor_data is None, cannot make prediction.")
        return None

    try:
        # Prepare the data for the model (assumes data is 2D)
        test_data = [[
            sensor_data.time,
            sensor_data.accelX,
            sensor_data.accelY,
            sensor_data.accelZ,
            sensor_data.rotationRateAlphaRad,
            sensor_data.rotationRateBetaRad,
            sensor_data.rotationRateGammaRad,
            sensor_data.magnitude,
        ]]
        
        # Specify which model to use here
        model_name = "random_forest"  # Change as needed
        if model_name not in models:
            raise HTTPException(status_code=404, detail="Model not found")
        
        model = models[model_name]
        prediction = model.predict(test_data)
        
        return prediction.tolist()
    
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

