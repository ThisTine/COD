from multiprocessing import Process, Manager

from utils.core import start_video
from utils.gui.start_gui import start_gui



if __name__ == '__main__':
    manager = Manager()
    is_show_person_text = manager.Value('p', False)
    is_show_person_bounding_box = manager.Value('pb', False)
    is_show_object_bounding_box = manager.Value('ob', True)
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
