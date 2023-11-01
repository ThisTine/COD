import cv2
def zoom_at(img, coord=None, size=None):
    print(coord)
    # Translate to zoomed coordinates
    # h, w, _ = [ zoom * i for i in img.shape ]
    h, w, _ = img.shape
    aspectRatio = w/h

    minX,minY = coord[0]
    maxX,maxY = coord[1]

    len_X = maxX - minX
    len_Y = maxY - minY
    if len_X > len_Y:
        # check if the shorter side is larger than a 3:2 ration
        if len_Y > len_X * (aspectRatio):
            # if so, increase larger side to 3:2 ratio
            len_X = len_Y * aspectRatio
        else:
            # else, increase shorter side to 3:2 ratio
            len_Y = len_X * (3/2) 
    else:
        # same as above
        if len_X > len_Y * (aspectRatio):
            len_Y = len_X * aspectRatio
        else:
            len_X = len_Y * (aspectRatio) 
    
    # if coord is None: cx, cy = w/2, h/2
    # else: cx, cy = [ zoom*c for c in coord ]

    if minX + len_X > img.shape[1]:
        len_X = img.shape[1]-minX
    #minX = img.shape[1]-len_X
    if minY + len_Y > img.shape[0]:
        len_Y = img.shape[0]-minY
        #minY = img.shape[0]-len_Y


    
    # img = cv2.resize( img, (0, 0), fx=zoom, fy=zoom)
    # print([[int(minY-(len_Y/2)),int(minY+len_Y/2)],[int(minX-len_X/2),int(minX+len_X/2)]] )
    cropped_img = img[int(minY):int(minY+len_Y),int(minX-len_X/2):int(minX+len_X)]
    try:
        temp = cv2.resize(cropped_img, (w,h), interpolation=cv2.INTER_AREA)
        return temp
    except:
        return img