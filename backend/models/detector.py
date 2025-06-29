from fastapi import FastAPI
import torch
import cv2
import yaml
import numpy as np
from ultralytics import YOLO

class Detector:
    def __init__(self, model_path: str, config_path: str):
        self.model = YOLO(model_path)
        self.classes = self.load_classes(config_path)

    def load_classes(self, config_path: str):
        with open(config_path, 'r') as file:
            data = yaml.safe_load(file)
        return data['names']

    def detect(self, image_bytes):
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return []
        
        results = self.model(image, conf=0.25, iou=0.45)
        detections = []
        
        # Debug: Print the structure of results
        print(f"Results type: {type(results)}")
        print(f"Results length: {len(results)}")
        if len(results) > 0:
            print(f"First result type: {type(results[0])}")
            print(f"First result attributes: {dir(results[0])}")
            if hasattr(results[0], 'boxes'):
                print(f"Boxes shape: {results[0].boxes.shape if results[0].boxes is not None else 'None'}")
            if hasattr(results[0], 'xyxy'):
                print(f"xyxy shape: {results[0].xyxy.shape if results[0].xyxy is not None else 'None'}")
        
        # Try different ways to access detection results
        if len(results) > 0:
            result = results[0]
            
            # Method 1: Try using boxes attribute
            if hasattr(result, 'boxes') and result.boxes is not None:
                boxes = result.boxes
                if hasattr(boxes, 'xyxy') and boxes.xyxy is not None:
                    for i in range(len(boxes.xyxy)):
                        box = boxes.xyxy[i]
                        conf = boxes.conf[i]
                        cls = boxes.cls[i]
                        x1, y1, x2, y2 = box[0].item(), box[1].item(), box[2].item(), box[3].item()
                        detections.append({
                            'label': self.classes[int(cls)],
                            'confidence': conf.item(),
                            'bbox': [x1, y1, x2 - x1, y2 - y1]
                        })
                        print(f"Detection: {self.classes[int(cls)]} at {[x1, y1, x2, y2]} with conf {conf.item()}")
            
            # Method 2: Try using xyxy attribute directly
            elif hasattr(result, 'xyxy') and result.xyxy is not None:
                for i in range(len(result.xyxy)):
                    box = result.xyxy[i]
                    conf = result.conf[i] if hasattr(result, 'conf') else 1.0
                    cls = result.cls[i] if hasattr(result, 'cls') else 0
                    x1, y1, x2, y2 = box[0].item(), box[1].item(), box[2].item(), box[3].item()
                    detections.append({
                        'label': self.classes[int(cls)],
                        'confidence': conf.item(),
                        'bbox': [x1, y1, x2 - x1, y2 - y1]
                    })
                    print(f"Detection: {self.classes[int(cls)]} at {[x1, y1, x2, y2]} with conf {conf.item()}")
        
        print(f"Total detections: {len(detections)}")
        return detections

    def process_image(self, image_path: str):
        image = cv2.imread(image_path)
        return self.detect(image)