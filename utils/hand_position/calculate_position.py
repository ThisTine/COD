def calculate_position(bigBox: (int,int), smallBox: (int,int)):
    b_x1 = bigBox[0]
    b_x2 = bigBox[1]
    s_x1 = smallBox[0]
    s_x2 = smallBox[1]

    left = s_x1 - b_x1
    right = b_x2 - s_x2

    if left < 0 < right:
        return "LEFT"
    if right < 0 < left:
        return "RIGHT"
    if left >= 0 and right >= 0 :
        return "CENTER"

    if abs(left) - abs(right) > 0 :
        return "LEFT"
    if abs(right) - abs(left) > 0 :
        return "RIGHT"
    return "CENTER"

    return "LEFT"