
def obj_update_obj1(obj, world):
    obj['v_x'] = 10
    obj['v_y'] -= 1
    if obj['v_y'] < -10:
        obj['v_y'] = -10
    if obj['y'] < world['frameHeight'] - 300:
        obj['v_y'] = 0
    elif obj['y'] < world['frameHeight'] - 200:
        obj['v_y'] = -4
    elif obj['y'] < world['frameHeight'] - 100:
        obj['v_y'] = -8
    obj['pitch'] = abs(obj['v_y']) * 5
