from math import sqrt


def fly_toward(tracker, dest_x, dest_y, displacement, err):
    d_w_x = dest_x - tracker.world_x
    d_w_y = dest_y - tracker.world_y
    dist = sqrt((d_w_x ** 2) + (d_w_y ** 2))
    if dist > err:
        s_w_x = round(displacement * d_w_x / dist)
        s_w_y = round(displacement * d_w_y / dist)
        tracker.move(d_x=s_w_x, d_y=s_w_y)
