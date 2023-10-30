from utils.capture import camera, get_bounding_box
from utils.hand_position.predict_hand import HandModel
from utils.person.predict_person import PersonModel
import cv2

cap,width,height = camera.get_video_capture()
hand_model = HandModel()
person_model = PersonModel()

while True:
    success, img = cap.read()
    hand_result = hand_model.predict(source=img)
    person_result = person_model.predict(source=img)
    person_xy1, person_xy2 = get_bounding_box.get_bounding_box(person_result)
    hand_xy1, hand_xy2 = get_bounding_box.get_bounding_box(hand_result)

    for h_ind in range(len(hand_xy1)):
        x1,y1 = hand_xy1[h_ind]
        x2, y2 = hand_xy2[h_ind]
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

    for p_ind in range(len(person_xy1)):
        x1,y1 = person_xy1[p_ind]
        x2, y2 = person_xy2[p_ind]
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 3)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()