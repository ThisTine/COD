from ultralytics import YOLO

class HandModel:

    def __init__(self):
        self.model = YOLO("weight/hand/hand.pt")

    def predict(self, source):
        return self.model.predict(source=source,stream=True, conf=0.6)