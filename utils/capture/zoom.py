import cv2
def zoom_at(img, zoom, coord=None, size=None):
    # Translate to zoomed coordinates
    # h, w, _ = [ zoom * i for i in img.shape ]
    h, w = img.shape
    
    # if coord is None: cx, cy = w/2, h/2
    # else: cx, cy = [ zoom*c for c in coord ]
    
    # img = cv2.resize( img, (0, 0), fx=zoom, fy=zoom)
    # img = img[ int(round(cy - h/zoom * .5)) : int(round(cy + h/zoom * .5)),
    #            int(round(cx - w/zoom * .5)) : int(round(cx + w/zoom * .5)),
    #            : ]

    # img = img[ coord[0] ]
    
    return img