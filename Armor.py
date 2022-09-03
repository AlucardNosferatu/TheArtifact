from copy import deepcopy

import numpy as np
from Box2D import b2Vec2, b2RayCastCallback

from Physics import world, PPM, SCREEN_HEIGHT, persist_draw

shell_spec = {
    'AP Level': 2,
    'AP Angle In Degree': 45
}


# noinspection PyArgumentList,PyAttributeOutsideInit
class RayCastClosestCallback(b2RayCastCallback):
    """This callback finds the closest hit"""

    def __repr__(self):
        return 'Closest hit'

    def __init__(self, **kwargs):
        b2RayCastCallback.__init__(self, **kwargs)
        self.fixture = None
        self.hit = False

    def ReportFixture(self, fixture, point, normal, fraction):
        """
        Called for each fixture found in the query. You control how the ray
        proceeds by returning a float that indicates the fractional length of
        the ray. By returning 0, you set the ray length to zero. By returning
        the current fraction, you proceed to find the closest point. By
        returning 1, you continue with the original ray clipping. By returning
        -1, you will filter out the current fixture (the ray will not hit it).
        """
        self.hit = True
        self.fixture = fixture
        self.point = b2Vec2(point)
        self.normal = b2Vec2(normal)
        # NOTE: You will get this error:
        #   "TypeError: Swig director type mismatch in output value of
        #    type 'float32'"
        # without returning a value
        return fraction


def dot_product_angle(v1, v2):
    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
        print("Zero magnitude vector!")
    else:
        vector_dot_product = np.dot(v1, v2)
        arccos = np.arccos(vector_dot_product / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        angle = np.degrees(arccos)
        return 90 - (180 - angle)
    return 0


def weapon_sim(fire_loc: list[float], aim_loc: list[float]):
    fl_scr = deepcopy(fire_loc)
    al_scr = deepcopy(aim_loc)
    fire_loc = [fire_loc[0], SCREEN_HEIGHT - fire_loc[1]]
    aim_loc = [aim_loc[0], SCREEN_HEIGHT - aim_loc[1]]
    fire_loc = [c / PPM for c in fire_loc]
    aim_loc = [c / PPM for c in aim_loc]
    fire_loc = b2Vec2(fire_loc[0], fire_loc[1])
    aim_loc = b2Vec2(aim_loc[0], aim_loc[1])
    if (aim_loc - fire_loc).length > 0.0:
        callback = RayCastClosestCallback()
        world.RayCast(callback, fire_loc, aim_loc)
        if callback.hit:
            cp_scr = callback.point.copy()
            head = b2Vec2(cp_scr) + 10 * b2Vec2(callback.normal)
            cp_scr *= PPM
            cp_scr = [cp_scr[0], SCREEN_HEIGHT - cp_scr[1]]
            head *= PPM
            head = [head[0], SCREEN_HEIGHT - head[1]]
            ang = dot_product_angle(aim_loc - fire_loc, callback.normal)
            print('ang:', ang)
            if ang <= shell_spec['AP Angle In Degree']:
                print('跳弹！我们未能击穿他们的装甲！')
            else:
                print('我们击穿了他们的装甲！')
            persist_draw.__setitem__(
                'shell_ray',
                {
                    'type': 'line',
                    'color': (0, 255, 0, 255),
                    'p1': fl_scr,
                    'p2': cp_scr
                }
            )
            persist_draw.__setitem__(
                'normal_ray',
                {
                    'type': 'line',
                    'color': (0, 0, 255, 255),
                    'p1': cp_scr,
                    'p2': head
                }
            )
            return callback.fixture.body.userData
        else:
            persist_draw.__setitem__(
                'shell_ray',
                {
                    'type': 'line',
                    'color': (255, 0, 0, 255),
                    'p1': fl_scr,
                    'p2': al_scr
                }
            )
            if 'normal_ray' in persist_draw:
                del persist_draw['normal_ray']
            return None
    return None
