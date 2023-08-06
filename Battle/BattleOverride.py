import time

from Classes.Fleet import Fleet

chances = 0


class OverrideActions:
    points = None

    def __init__(self):
        pass

    def learn(self):
        pass

    def forget(self):
        pass

    def use(self):
        pass


def override_orders(fleet_p, orders):
    override_chances = []
    [override_chances.append(index) for index in range(len(orders)) if orders[index][0] == fleet_p.flag_ship]
    override_chances.sort()
    override_chances.reverse()
    for index in override_chances:
        orders.pop(index)
    return orders, len(override_chances)


def override_init(override_chances):
    global chances
    chances = override_chances


def override_control(fleet_p: Fleet, fleet_e: Fleet):
    # noinspection SpellCheckingInspection
    def fancy_animation():
        print('(T)ransient.', end='')
        time.sleep(0.5)
        print('(R)eflection.', end='')
        time.sleep(0.5)
        print('(A)ugmented.', end='')
        time.sleep(0.5)
        print('(N)eural.', end='')
        time.sleep(0.5)
        print('(S)ystem.', end='')
        time.sleep(0.5)
        print('-(A)ctive.', end='')
        time.sleep(0.5)
        print('(M)ode.')
        time.sleep(1.25)
        print('=============================T.R.A.N.S-A.M.=============================')

    global chances
    fancy_animation()
    # todo: implement override_control
    player = fleet_p.ships[fleet_p.flag_ship]
    override_actions = player.override_actions
