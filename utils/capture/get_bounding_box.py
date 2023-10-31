from ultralytics.engine.results import Results
def get_bounding_box(result: list[Results]) -> tuple[list[list[int]], list[list[int]]]:
    xy1 = list()
    xy2 = list()
    for r in result:
        for box in r.boxes:
           x1, y1, x2, y2 = box.xyxy[0]
           x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
           cls = int(box.cls[0])
           xy1.append([x1,y1,cls])
           xy2.append([x2,y2,cls])

    return xy1, xy2