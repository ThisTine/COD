def calculate_center_frame(width,height):
    start_point = (int(width / 4), 0)
    end_point = (int(width - (width / 4)), int(height))

    center_box = (start_point[0], end_point[0])
    return center_box, start_point, end_point