import cv2
import numpy

from Dynamics import obj_update_obj1

world = {'frameWidth': 1024, 'frameHeight': 768}
obj_list = []

pic = cv2.imread('mark.png')
r, c = pic.shape[:2]
obj_1 = {
    'x_c': 0 + round(c / 2),
    'y_c': world['frameHeight'] - round(r / 2),
    'pic': pic,
    'cols': c,
    'rows': r,
    'v_x': 0,
    'v_y': 0,
    'pitch': 0,
    'update_phy': obj_update_obj1
}
obj_1.__setitem__('x', obj_1['x_c'] - round(obj_1['cols'] / 2))
obj_1.__setitem__('y', obj_1['y_c'] - round(obj_1['rows'] / 2))

obj_list.append(obj_1)


def rotate_image(image, angle):
    image_center = tuple(numpy.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def physics_frame():
    global obj_list
    for obj in obj_list:
        obj['update_phy'](obj, world)
        # dx = random.randint(-10, 20)
        # dy = random.randint(-10, 20)
        dx = obj['v_x']
        dy = obj['v_y']
        obj['x_c'] = max(round(obj['cols'] / 2), min(obj['x_c'] + dx, world['frameWidth'] - round(obj['cols'] / 2)))
        obj['y_c'] = max(round(obj['rows'] / 2), min(obj['y_c'] + dy, world['frameHeight'] - round(obj['rows'] / 2)))
        obj.__setitem__('x', obj['x_c'] - round(obj['cols'] / 2))
        obj.__setitem__('y', obj['y_c'] - round(obj['rows'] / 2))


def draw_frame():
    global obj_list
    canvas = numpy.ones([world['frameHeight'], world['frameWidth'], 3], dtype=numpy.uint8) * 255
    for obj in obj_list:
        y1 = obj['y']
        y2 = obj['y'] + obj['rows']
        x1 = obj['x']
        x2 = obj['x'] + obj['cols']
        r_pic = rotate_image(obj['pic'], obj['pitch'])
        canvas[y1:y2, x1:x2] = r_pic
    cv2.imshow("Title", canvas)
    cv2.waitKey(1)


f_count = 0
while True:
    if f_count >= 10:
        f_count = 0
        physics_frame()
    draw_frame()
    f_count += 1

cap.release()
cv2.destroyAllWindows()
