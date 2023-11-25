import time
from multiprocessing import Process, Manager
from utils.capture import camera, get_bounding_box, zoom
from utils.hand_position.predict_hand import HandModel
from utils.object_position.shift_bounding_box import shift_bounding_box
from utils.person.calculate_person_position import calculate_person_position
from utils.person.predict_person import PersonModel
from utils.object_position.predict_object import ObjectModel
from utils.object_position.calculate_object_via_hand_position import calculate_object_via_hand_position
import cv2

path = str("./test_dict")

current_zoom_pos = None


def start_video(is_show_person_text_o, is_show_person_bounding_box_o, is_show_object_bounding_box_o,
                is_show_hand_bounding_box_o, is_zoom_to_object_o):
    cap, width, height = camera.get_video_capture()
    hand_model = HandModel()
    person_model = PersonModel()
    object_model = ObjectModel()

    # 0->left_pointer
    # 1->right_pointer
    hand_class_names = hand_model.model.names

    start_point = (int(width / 4), 0)
    end_point = (int(width - (width / 4)), int(height))

    big_box_x = (start_point[0], end_point[0])

    def change_zoom_pos(coord: ([int, int], [int, int]), current_time: int):
        global current_zoom_pos
        if current_zoom_pos is None:
            current_zoom_pos = {
                "coord": coord,
                "time": current_time
            }
        else:
            if current_time < current_zoom_pos["time"] + 5:
                return
            current_zoom_pos = {
                "coord": coord,
                "time": current_time
            }

    while True:
        is_show_hand_bounding_box = is_show_hand_bounding_box_o.value
        is_show_person_bounding_box = is_show_person_bounding_box_o.value
        is_show_person_text = is_show_person_text_o.value
        is_show_object_bounding_box = is_show_object_bounding_box_o.value
        is_zoom_to_object = is_zoom_to_object_o.value
        success, img = cap.read()
        hand_result = hand_model.predict(source=img)
        person_result = person_model.predict(source=img)
        person_xy1, person_xy2 = get_bounding_box.get_bounding_box(person_result)
        hand_xy1, hand_xy2 = get_bounding_box.get_bounding_box(hand_result)

        for h_ind in range(len(hand_xy1)):
            x1, y1, cls = hand_xy1[h_ind]
            x2, y2, _ = hand_xy2[h_ind]
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            if is_show_hand_bounding_box:
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.putText(img, hand_class_names[cls], org, font, fontScale, color, thickness)

        for p_ind in range(len(person_xy1)):
            x1, y1, _ = person_xy1[p_ind]
            x2, y2, _ = person_xy2[p_ind]
            if is_show_person_bounding_box:
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
            if is_show_person_text:
                cv2.putText(img, calculate_person_position(big_box_x, (x1, x2)), [int(width / 2) - 200, int(height)],
                            cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 0), 5)

        if len(hand_xy1) == 1:
            # print(hand_class_names)
            hand_cls = hand_class_names[hand_xy1[0][2]]
            if hand_cls == 'left_pointer':
                point_pos = hand_xy2[0][0]
                cod = (0, int(height), 0, hand_xy1[0][0])
                # cv2.rectangle(img, (cod[2]-10, cod[0]-10), (cod[3]-10, cod[1]-10), (255, 0, 255), 3)
                temp = img[cod[0]:cod[1], cod[2]:cod[3]]
                # img = temp
                oj = object_model.predict(source=temp)
                try:
                    oj_xy1, oj_xy2 = get_bounding_box.get_bounding_box(oj)
                    obj = calculate_object_via_hand_position(obj_pos=oj_xy1, hand_pos=point_pos, isLeft=False)
                    if obj is not None:
                        o_x1 = obj[0]
                        o_y1 = obj[1]
                        o_ind = obj[2]
                        o_x2, o_y2, _ = oj_xy2[o_ind]
                        change_zoom_pos(coord=([o_x1, o_y1], [o_x2, o_y2]), current_time=int(time.time()))

                        if is_show_object_bounding_box:
                            for oj_ind in range(len(oj_xy1)):
                                x1, y1, _ = oj_xy1[oj_ind]
                                x2, y2, _ = oj_xy2[oj_ind]
                                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 3)

                except:
                    print("error")

            elif hand_cls == 'right_pointer':
                point_pos = hand_xy1[0][0]
                cod = (0, int(height), hand_xy2[0][0], int(width))
                temp = img[cod[0]:cod[1], cod[2]:cod[3]]
                # cv2.rectangle(img, (cod[2] - 10, cod[0] - 10), (cod[3] - 10, cod[1] - 10), (255, 0, 255), 3)
                # img = temp
                oj = object_model.predict(source=temp)
                # #     # img = temp
                try:
                    t_oj_xy1, t_oj_xy2 = get_bounding_box.get_bounding_box(oj)
                    # print(t_oj_xy1)
                    oj_xy1 = list(map(lambda x: [shift_bounding_box(x[0], cod[2]), x[1], x[2]], t_oj_xy1))
                    oj_xy2 = list(map(lambda x: [shift_bounding_box(x[0], cod[2]), x[1], x[2]], t_oj_xy2))
                    obj = calculate_object_via_hand_position(obj_pos=oj_xy2, hand_pos=point_pos, isLeft=True)
                    #         print(obj)
                    if obj != None:
                        o_x2 = obj[0]
                        o_y2 = obj[1]
                        o_ind = obj[2]
                        o_x1, o_y1, _ = oj_xy1[o_ind]
                        # print("left_pointer")
                        change_zoom_pos(coord=([o_x1, o_y1], [o_x2, o_y2]), current_time=int(time.time()))
                        # img = zoom.zoom_at(img, coord=([o_x1, o_y1], [o_x2, o_y2]), size=(width, height))
                    if is_show_object_bounding_box:
                        for oj_ind in range(len(oj_xy1)):
                            x1, y1, _ = oj_xy1[oj_ind]
                            x2, y2, _ = oj_xy2[oj_ind]
                            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
                except Exception as e:
                    print(e)
            if current_zoom_pos is not None and current_zoom_pos["coord"] is not None and is_zoom_to_object:
                img = zoom.zoom_at(img, coord=current_zoom_pos["coord"], size=(width, height))
        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def set_hand_bounding_box(is_show_hand_bounding_box_o):
    is_show_hand_bounding_box_o.value = not is_show_hand_bounding_box_o.value


def set_person_text(is_show_person_text_o):
    is_show_person_text_o.value = not is_show_person_text_o.value


def set_person_bounding_box(is_show_person_bounding_box_o):
    is_show_person_bounding_box_o.value = not is_show_person_bounding_box_o.value


def set_object_bounding_box(is_show_object_bounding_box_o):
    is_show_object_bounding_box_o.value = not is_show_object_bounding_box_o.value


def set_zoom_to_object(is_zoom_to_object):
    is_zoom_to_object.value = not is_zoom_to_object.value


def start_gui(is_show_person_text_o, is_show_person_bounding_box_o, is_show_object_bounding_box_o,
              is_show_hand_bounding_box_o, is_zoom_to_object_o):
    import tkinter as tk

    window = tk.Tk()
    hand_bounding_box_bth = tk.Button(window, text="{status} Show person text".format(
        status="Hide" if is_show_person_text_o.value else "Show"),

                                      command=lambda: set_person_text(is_show_person_text_o))
    hand_bounding_box_bth.pack()
    person_text_bth = tk.Button(window, text="{status} hand bounding box".format(status="Hide"
    if is_show_hand_bounding_box_o.value else "Show"),
                                command=lambda: set_hand_bounding_box(is_show_hand_bounding_box_o))
    person_text_bth.pack()
    person_bounding_box_bth = tk.Button(window, text="{status} person bounding Box".format(
        status="Hide" if is_show_person_bounding_box_o.value else "Show"),
                                        command=lambda: set_person_bounding_box(is_show_person_bounding_box_o))
    person_bounding_box_bth.pack()
    object_bounding_box_bth = tk.Button(window, text="{status} object bounding Box".format(
        status="Hide" if is_show_object_bounding_box_o.value else "Show"),
                                        command=lambda: set_object_bounding_box(is_show_object_bounding_box_o))
    object_bounding_box_bth.pack()
    zoom_to_object_bth = tk.Button(window, text="{status} zoom to object".format(
        status="Hide" if is_zoom_to_object_o.value else "Show"),
                                   command=lambda: set_zoom_to_object(is_zoom_to_object_o))
    zoom_to_object_bth.pack()
    window.title("COD Debugger")
    window.geometry("300x300")
    window.mainloop()


if __name__ == '__main__':
    manager = Manager()
    is_show_person_text = manager.Value('p', False)
    is_show_person_bounding_box = manager.Value('pb', False)
    is_show_object_bounding_box = manager.Value('ob', False)
    is_show_hand_bounding_box = manager.Value('hb', False)
    is_zoom_to_object = manager.Value('zto', True)
    p1 = Process(target=start_video, args=(is_show_person_text, is_show_person_bounding_box, is_show_object_bounding_box
                                           , is_show_hand_bounding_box, is_zoom_to_object))
    p2 = Process(target=start_gui, args=(is_show_person_text, is_show_person_bounding_box, is_show_object_bounding_box,
                                         is_show_hand_bounding_box, is_zoom_to_object))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
