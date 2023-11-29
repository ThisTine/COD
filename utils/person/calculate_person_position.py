import  requests
import ssl
def calculate_person_position(bigBox: (int,int), smallBox: (int,int)):
    b_x1 = bigBox[0]
    b_x2 = bigBox[1]
    s_x1 = smallBox[0]
    s_x2 = smallBox[1]

    left = s_x1 - b_x1
    right = b_x2 - s_x2
    # response = Request('GET', "http://cod9000.pspgun.com/")
    # prepped = s.prepare_request(response)
    # resp = s.send(prepped)
    # print(resp.status_code)
    # print(response)
    # print(prepped)
    print(requests.get("https://httpbin.org/get"))
    if left < 0 < right:
        response = requests.patch("https://cod9000.pspgun.com/change/L",verify=False)
        print(response.status_code)
        return "LEFT"
    if right < 0 < left:
        response = requests.patch("https://cod9000.pspgun.com/change/R",verify=False)
        print(response.status_code)
        return "RIGHT"
    if left >= 0 and right >= 0 :
        response = requests.patch("https://cod9000.pspgun.com/change/S",verify=False)
        print(response.status_code)
        return "CENTER"

    if abs(left) - abs(right) > 0 :
        response = requests.patch("https://cod9000.pspgun.com/change/L",verify=False)
        print(response.status_code)
        return "LEFT"
    if abs(right) - abs(left) > 0 :
        response = requests.patch("https://cod9000.pspgun.com/change/R",verify=False)
        print(response.status_code)
        return "RIGHT"
    response = requests.post("https://cod9000.pspgun.com/change/S",verify=False)
    return "CENTER"

    # return "LEFT"