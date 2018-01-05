import cv2
import numpy as np

cap = cv2.VideoCapture(0)

arg = 44

highest_w = 0
highest_h = 0

distance_x = 0
distance_y = 0

template = cv2.imread('E:\\opencv_img\\wechat.jpg', 0)
w, h = template.shape[::-1]

while True:
    ret, frame = cap.read()

    b, g, r = cv2.split(frame)

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    canny = cv2.Canny(b, arg, arg * 3)

    for i in range(640):
        for j in range(480):
            # print(str(i) + '+' + str(j))

            if canny[j][639 - i] > 150:
                highest_w = i - 50
                highest_h = j
                break

    # cv2.waitKey(0)

    cv2.rectangle(frame, (639 - highest_w - 10, highest_h - 10), (639 - highest_w + 10, highest_h + 10), (0, 0, 255), 2)

    # if highest_w > 0:
    #     print(str(639 - highest_w) + ',' + str(highest_h))

    res_filter = cv2.matchTemplate(canny, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.375
    loc_filter = np.where(res_filter >= threshold)

    buffer_x = buffer_y = 0
    for pt in zip(*loc_filter[::-1]):
        if abs(buffer_y - pt[1]) > 4:
            cv2.rectangle(frame, pt, (pt[0] + 40, pt[1] + 40), (0, 255, 0), 2)
            buffer_x = pt[0]
            buffer_y = pt[1]
        else:
            if abs(buffer_x - pt[0]) > 9:
                cv2.rectangle(frame, pt, (pt[0] + 40, pt[1] + 40), (0, 255, 0), 2)
                buffer_x = pt[0]
                buffer_y = pt[1]
    distance = np.square(buffer_x + 40 - (639 - highest_w)) + np.square(buffer_y + 20 - highest_h)

    dis_buf = np.round(np.sqrt(distance))

    distance = str(np.round(np.sqrt(distance)))
    # print(distance)

    cv2.putText(frame, 'Pixels Dis:' + distance, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
    cv2.putText(frame, 'Delay:' + str(dis_buf * 2.35 + 136), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
    cv2.imshow('frame', frame)
    # cv2.imshow('b pass', b)
    # cv2.imshow("Canny", canny)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
