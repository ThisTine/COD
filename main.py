from utils.capture import camera, get_bounding_box, zoom
from utils.hand_position.predict_hand import HandModel
from utils.object_position.shift_bounding_box import shift_bounding_box
from utils.person.calculate_person_position import calculate_person_position
from utils.person.predict_person import PersonModel
from utils.object_position.predict_object import ObjectModel
from utils.object_position.calculate_object_via_hand_position import calculate_object_via_hand_position
import cv2
from statistics import mean 


cap,width,height = camera.get_video_capture()
hand_model = HandModel()
person_model = PersonModel()
object_model = ObjectModel()

#0->left_pointer
#1->right_pointer
hand_class_names = hand_model.model.names

start_point = (int(width / 4), 0)
end_point = (int(width - (width / 4)), int(height))

big_box_x = (start_point[0], end_point[0])

while True:
    success, img = cap.read()
    hand_result = hand_model.predict(source=img)
    person_result = person_model.predict(source=img)
    person_xy1, person_xy2 = get_bounding_box.get_bounding_box(person_result)
    hand_xy1, hand_xy2 = get_bounding_box.get_bounding_box(hand_result)

    # for h_ind in range(len(hand_xy1)):
    #     x1, y1,cls = hand_xy1[h_ind]
    #     x2, y2,_ = hand_xy2[h_ind]
    #     org = [x1, y1]
    #     font = cv2.FONT_HERSHEY_SIMPLEX
    #     fontScale = 1
    #     color = (255, 0, 0)
    #     thickness = 2
    #     cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
    #     cv2.putText(img, hand_class_names[cls], org, font, fontScale, color, thickness)

    for p_ind in range(len(person_xy1)):
       x1,y1,_ = person_xy1[p_ind]
       x2, y2,_ = person_xy2[p_ind]
       cv2.putText(img, calculate_person_position(big_box_x, (x1, x2)), [int(width / 2)-200, int(height)],
                        cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 0), 5)
    #    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 3)


    if len(hand_xy1) == 1:
        # print(hand_class_names)
        hand_cls = hand_class_names[hand_xy1[0][2]]
        print(hand_cls)
        if hand_cls == 'left_pointer':
            point_pos = hand_xy2[0][0]
            cod = (0,int(height),0,hand_xy1[0][0])
            temp = img[cod[0]:cod[1],cod[2]:cod[3]]
            # img = temp
            oj = object_model.predict(source=temp)
            try:
                oj_xy1, oj_xy2 = get_bounding_box.get_bounding_box(oj)
                obj = calculate_object_via_hand_position(obj_pos=oj_xy1,hand_pos=point_pos,isLeft=False)
                if obj != None:
                    o_x1 = obj[0]
                    o_y1 = obj[1]
                    o_ind = obj[2]
                    o_x2,o_y2,_ = oj_xy2[o_ind]
                    img = zoom.zoom_at(img,coord=([o_x1,o_y1],[o_x2,o_y2]),size=(width,height))

            except:
                print("error")

        elif hand_cls == 'right_pointer':
            point_pos = hand_xy1[0][0]
            cod = (0,int(height),hand_xy2[0][0],int(width))
            temp = img[cod[0]:cod[1],cod[2]:cod[3]]
            # img = temp
            oj = object_model.predict(source=temp)
        #     # img = temp
            try:
                t_oj_xy1, t_oj_xy2 = get_bounding_box.get_bounding_box(oj)
                # print(t_oj_xy1)
                oj_xy1 = list(map(lambda x: [ shift_bounding_box(x[0],cod[2]),x[1],x[2] ],t_oj_xy1))
                oj_xy2 = list(map(lambda x: [ shift_bounding_box(x[0],cod[2]),x[1],x[2] ],t_oj_xy2))
                obj = calculate_object_via_hand_position(obj_pos=oj_xy2,hand_pos=point_pos,isLeft=True)
        #         print(obj)
                if obj != None:
                    o_x2 = obj[0]
                    o_y2 = obj[1]
                    o_ind = obj[2]
                    o_x1,o_y1,_ = oj_xy1[o_ind]
                    # print("left_pointer")
                    img = zoom.zoom_at(img,coord=([o_x1,o_y1],[o_x2,o_y2]),size=(width,height))
                for oj_ind in range(len(oj_xy1)):
                    x1,y1,_ = oj_xy1[oj_ind]
                    x2, y2,_ = oj_xy2[oj_ind]
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            except Exception as e:
                print(e)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()