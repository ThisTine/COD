def calculate_object_via_hand_position(obj_pos: list[list[int]],hand_pos:int, isLeft: bool):
    obj = None
    for ind in range(len(obj_pos)):
       x,y,_ = obj_pos[ind]
       print(x)
       print(hand_pos)
       if isLeft == True and x < hand_pos:
           obj = list([x,y,ind])
           break
       
       if isLeft == False and x > hand_pos:
           obj = list([x,y,ind])
           break

    return obj