from ultralytics import YOLO

class ObjectModel:

    def __init__(self):
        self.model = YOLO("weight/object/openImg.pt")

    def predict(self, source):
        includeClass = [*range(0,601)]
        for i in range(259, 272):
            print(i)
            includeClass.remove(i)
        includeClass.remove(70)
        includeClass.remove(115)
        includeClass.remove(116)
        includeClass.remove(217)
        includeClass.remove(283)
        includeClass.remove(322)
        includeClass.remove(354)
        includeClass.remove(381)
        includeClass.remove(505)
        includeClass.remove(594)
        
        return self.model.predict(source=source,stream=True, conf=0.2, hide_labels=True, classes=includeClass)
