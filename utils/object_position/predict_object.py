from ultralytics import YOLO

class ObjectModel:

    def __init__(self):
        # self.model = YOLO("weight/object/openImg.pt")
        self.model = YOLO("weight/object/yolov8n-oiv7.pt")
        self.includeClass = [*range(0,601)]
        for i in range(259, 272):
            # print(i)
            self.includeClass.remove(i)
        self.includeClass.remove(70)
        self.includeClass.remove(115)
        self.includeClass.remove(116)
        self.includeClass.remove(217)
        self.includeClass.remove(283)
        self.includeClass.remove(322)
        self.includeClass.remove(354)
        self.includeClass.remove(381)
        self.includeClass.remove(505)
        self.includeClass.remove(594)
        # self.includeClass = [*range(1,80)]

    def predict(self, source):


        return self.model.predict(source=source,stream=True, conf=0.1, classes=self.includeClass,verbose=False)
