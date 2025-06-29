import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from models.detector import Detector

router = APIRouter()

model_path = r"D:\AI_Learning\python\01_Learning\Target_Detection\fatigue_monitor_update\runs\detect\myexp2\weights\best.pt"
config_path = r"D:\AI_Learning\python\01_Learning\Target_Detection\fatigue_monitor_update\backend\data.yaml"

detector = Detector(model_path=model_path, config_path=config_path)

@router.post("/detect")
async def detect(file: UploadFile = File(...)):
    image_bytes = await file.read()
    results = detector.detect(image_bytes)
    return {"results": results}