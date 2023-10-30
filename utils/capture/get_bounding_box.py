from ultralytics.engine.results import Results
def get_bounding_box(result: list[Results]):
    xy1 = list()
    xy2 = list()
    for r in result:
        for box in r.boxes:
           x1, y1, x2, y2 = box.xyxy[0]
           x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
           
           xy1.append([x1,y1])
           xy2.append([x2,y2])

    return xy1, xy2