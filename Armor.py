from Box2D import b2Body, b2Vec2, b2_dynamicBody

from Physics import world, PPM, SCREEN_HEIGHT


def weapon_simulate(fire_loc: list[float], aim_loc: list[float]):
    fire_loc = [fire_loc[0], SCREEN_HEIGHT - fire_loc[1]]
    aim_loc = [aim_loc[0], SCREEN_HEIGHT - aim_loc[1]]
    fire_loc = [c / PPM for c in fire_loc]
    aim_loc = [c / PPM for c in aim_loc]
    line_vec = b2Vec2(aim_loc[0] - fire_loc[0], aim_loc[1] - fire_loc[1])
    fire_loc = b2Vec2(fire_loc[0], fire_loc[1])
    print('Test:')
    for body in world.bodies:
        body: b2Body
        if body.type is b2_dynamicBody:
            cp_list = []
            shape = body.fixtures[0].shape
            v_pos = [body.transform * v for v in shape.vertices]
            for vertex in v_pos:
                vertex: b2Vec2
                v2fl = vertex - fire_loc
                cp = v2fl.cross(line_vec)
                cp_list.append(cp)
            for i in range(len(v_pos) - 1):
                if cp_list[0] * cp_list[i + 1] < 0:
                    print('Hit!')
                    break
