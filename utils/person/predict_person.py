import os
from ultralytics import YOLO

class PersonModel:

    def __init__(self):
        print(os.getcwd())
        self.model = YOLO("./weight/human/yolov8n.pt")

    def predict(self,source):
        return self.model.predict(source=source,stream=True, classes=[0], conf=0.8)