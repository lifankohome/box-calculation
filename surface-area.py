import cv2
import numpy as np

img_bgr = cv2.imread('E:\\opencv_img\\5.png')
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

canny = cv2.Canny(img_gray, 10, 150)
cv2.imshow("Canny", canny)

template_front = cv2.imread('E:\\opencv_img\\front.png', 0)
w, h = template_front.shape[::-1]

res_front = cv2.matchTemplate(canny, template_front, cv2.TM_CCOEFF_NORMED)
threshold = 0.735
loc_front = np.where(res_front >= threshold)

front = 0
for pt in zip(*loc_front[::-1]):
    cv2.rectangle(img_bgr, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 1)
    front += 1
    print(pt)

print("前：" + str(front))

template_right = cv2.imread('E:\\opencv_img\\right.png', 0)
w, h = template_right.shape[::-1]

res_right_filter = cv2.matchTemplate(canny, template_right, cv2.TM_CCOEFF_NORMED)
threshold = 0.72
loc_right_filter = np.where(res_right_filter >= threshold)

right_filter = 0
buffer_x = buffer_y = 0
for pt in zip(*loc_right_filter[::-1]):
    if abs(buffer_y - pt[1]) > 4:
        cv2.rectangle(img_bgr, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)
        right_filter += 1
        # print(pt , abs(buffer_y-pt[1]))
        print(pt)
        buffer_x = pt[0]
        buffer_y = pt[1]
    else:
        if abs(buffer_x - pt[0]) > 9:
            cv2.rectangle(img_bgr, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)
            right_filter += 1
            print(pt)
            buffer_x = pt[0]
            buffer_y = pt[1]

print("右：" + str(right_filter))

template_up_filter = cv2.imread('E:\\opencv_img\\up_filter.png', 0)
w, h = template_up_filter.shape[::-1]

res_up_filter = cv2.matchTemplate(canny, template_up_filter, cv2.TM_CCOEFF_NORMED)
threshold = 0.6922
loc_up_filter = np.where(res_up_filter >= threshold)

up_filter = 0
buffer_x = buffer_y = 0
for pt in zip(*loc_up_filter[::-1]):
    if abs(buffer_y - pt[1]) > 4:
        cv2.rectangle(img_bgr, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 1)
        up_filter += 1
        # print(pt , abs(buffer_y-pt[1]))
        print(pt)
        buffer_x = pt[0]
        buffer_y = pt[1]
    else:
        if abs(buffer_x - pt[0]) > 9:
            cv2.rectangle(img_bgr, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 1)
            up_filter += 1
            print(pt)
            buffer_x = pt[0]
            buffer_y = pt[1]

print("上-filter：" + str(up_filter))

surface_area = (front + right_filter + up_filter) * 2

img_bgr_height = img_bgr.shape[0]
img_bgr_width = img_bgr.shape[1]

cv2.putText(img_bgr, 'Surface-area:' + str(surface_area), (int(img_bgr_width * 0.04), int(img_bgr_height * 0.04)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
cv2.putText(img_bgr, 'Front:' + str(front), (int(img_bgr_width * 0.04), int(img_bgr_height * 0.07)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
cv2.putText(img_bgr, 'Right-filter:' + str(right_filter), (int(img_bgr_width * 0.04), int(img_bgr_height * 0.10)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
cv2.putText(img_bgr, 'UP-filter:' + str(up_filter), (int(img_bgr_width * 0.04), int(img_bgr_height * 0.13)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

cv2.imshow('detected', img_bgr)

cv2.waitKey(0)
cv2.destroyAllWindows()
