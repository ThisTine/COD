from ultralytics import YOLO

class ObjectModel:

    def __init__(self):
        self.model = YOLO("weight/object/openImg.pt")

    def predict(self, source):
        return self.model.predict(source=source,stream=True, conf=0.2)