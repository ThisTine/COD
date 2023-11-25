def calculate_object_via_hand_position(obj_pos: list[list[int]], hand_pos: int, isLeft: bool):
    # print(obj_pos)
    obj = None
    for ind in range(len(obj_pos)):
        x, y, _ = obj_pos[ind]
        if isLeft is False and x < hand_pos:
            obj = list([x, y, ind])
            break

        if isLeft is True and x > hand_pos:
            obj = list([x, y, ind])
            break

    return obj
