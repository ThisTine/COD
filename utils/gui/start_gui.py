import requests


def start_gui(is_show_person_text_o, is_show_person_bounding_box_o, is_show_object_bounding_box_o,
              is_show_hand_bounding_box_o, is_zoom_to_object_o):
    import tkinter as tk

    window = tk.Tk()

    def reset_position():
        requests.patch("https://cod9000.pspgun.com/change/C", verify=False)

    def set_person_text(is_show_person_text_o):
        is_show_person_text_o.value = not is_show_person_text_o.value
        hand_bounding_box_bth['text'] = "{status} center stage".format(
            status="Disabled" if is_show_person_text_o.value else "Enabled")

    hand_bounding_box_bth = tk.Button(window, command=lambda: set_person_text(is_show_person_text_o))
    hand_bounding_box_bth['text'] = "{status} center stage".format(
            status="Disabled" if is_show_person_text_o.value else "Enabled")
    hand_bounding_box_bth.pack()

    def set_hand_bounding_box(is_show_hand_bounding_box_o):
        is_show_hand_bounding_box_o.value = not is_show_hand_bounding_box_o.value
        person_text_bth['text'] = "{status} hand bounding box".format(status="Hide"
        if is_show_hand_bounding_box_o.value else "Show")

    person_text_bth = tk.Button(window, command=lambda: set_hand_bounding_box(is_show_hand_bounding_box_o))
    person_text_bth['text'] = "{status} hand bounding box".format(status="Hide"
    if is_show_hand_bounding_box_o.value else "Show")
    person_text_bth.pack()

    def set_person_bounding_box(is_show_person_bounding_box_o):
        is_show_person_bounding_box_o.value = not is_show_person_bounding_box_o.value
        person_bounding_box_bth['text'] = "{status} person bounding Box".format(
            status="Hide" if is_show_person_bounding_box_o.value else "Show")

    person_bounding_box_bth = tk.Button(window, command=lambda: set_person_bounding_box(is_show_person_bounding_box_o))
    person_bounding_box_bth['text'] = "{status} person bounding Box".format(
        status="Hide" if is_show_person_bounding_box_o.value else "Show")
    person_bounding_box_bth.pack()

    def set_object_bounding_box(is_show_object_bounding_box_o):
        is_show_object_bounding_box_o.value = not is_show_object_bounding_box_o.value
        object_bounding_box_bth['text'] = "{status} object bounding Box".format(
            status="Hide" if is_show_object_bounding_box_o.value else "Show")

    object_bounding_box_bth = tk.Button(window, command=lambda: set_object_bounding_box(is_show_object_bounding_box_o))
    object_bounding_box_bth['text'] = "{status} object bounding Box".format(
        status="Hide" if is_show_object_bounding_box_o.value else "Show")
    object_bounding_box_bth.pack()

    def set_zoom_to_object(is_zoom_to_object):
        is_zoom_to_object.value = not is_zoom_to_object.value
        zoom_to_object_bth['text'] = "{status} zoom to object".format(
            status="Hide" if is_zoom_to_object_o.value else "Show")

    zoom_to_object_bth = tk.Button(window, command=lambda: set_zoom_to_object(is_zoom_to_object_o))
    zoom_to_object_bth['text'] = "{status} zoom to object".format(
        status="Hide" if is_zoom_to_object_o.value else "Show")
    zoom_to_object_bth.pack()

    reset_position_bth = tk.Button(window, text="Reset Position", command=lambda: reset_position())
    reset_position_bth.pack()

    window.title("COD Debugger")
    window.geometry("300x300")
    window.mainloop()
