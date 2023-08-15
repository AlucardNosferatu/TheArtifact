import random

from Buffs.BasicBuffs import Evade, Defend
from Classes.Fleet import Fleet


def escape(action, order, acting_ship, extra_params):
    interrupt, orders, acting_fleet = extra_params[0], extra_params[1], extra_params[2]
    fleet_names = {'FleetA': "Player's Fleet", 'FleetB': "Enemies' Fleet"}
    print(fleet_names[order[2]], 'is about to escape. {} is evading combat.'.format(acting_ship.name))
    if acting_ship.escapable == 0:
        failed = False
        if int(action[1]) < 6:
            size = 6 - int(action[1])
            chances: list[bool] = [True] * size
            chances[random.randint(0, size - 1)] = False
            print('The chance is {}%.'.format(int(100 / size)))
            if random.choice(chances):
                print('It failed to escape.')
                failed = True
        else:
            print('The chance is 100%.')
        if not failed:
            acting_fleet: Fleet
            if acting_fleet.will_to_fight <= 1:
                while len(orders) <= 0:
                    orders.append(None)
                print('It escaped from the battle zone.')
                interrupt[0] = True
            else:
                acting_fleet.will_to_fight -= 1
                print("It flew for a while, but it hasn't been out of battle zone yet.")
    elif acting_ship.escapable == 1:
        print('There are something wrong with {}, it cannot escape for now!'.format(acting_ship.name))
    elif acting_ship.escapable == 2:
        acting_fleet.will_to_fight = 0
        interrupt[0] = True
        print('{} cover the whole fleet, they can quickly escape now!'.format(acting_ship.name))


def idle(action, order, acting_ship, extra_params):
    _, _, _ = action, order, extra_params
    speech = random.choice(acting_ship.idle_speech)
    print('{}: {}'.format(acting_ship.name, speech))


def attack(action, order, acting_ship, extra_params):
    fleets_and_actions = extra_params[0]
    if action[2] < len(acting_ship.weapons):
        weapon = acting_ship.weapons[action[2]]
        basic_accuracy = acting_ship.fire_control_system
        maneuver = acting_ship.maneuver
        params_error = False
        if hasattr(weapon, 'special_function'):
            if len(action) == 3:
                weapon.special_function(action, order, acting_ship, extra_params)
            else:
                params_error = True
        else:
            if len(action) == 4:
                amount = int((((action[1] - 6) / 13) + 1) * weapon.power)
                print(acting_ship.name, 'fires on active target(s)!')
                for target_uid in action[3]:
                    if target_uid not in fleets_and_actions[fleets_and_actions[order[2]][2]][0].ships.keys():
                        print("But one of its targets was no longer in targets' fleet! Attack was nullified!")
                        continue
                    target_ship = fleets_and_actions[fleets_and_actions[order[2]][2]][0].ships[target_uid]
                    if not target_ship.is_destroyed():
                        print(target_ship.name, 'was fired by', acting_ship.name, '!')
                        maneuver_target = target_ship.maneuver
                        if hit(basic_accuracy, maneuver, maneuver_target):
                            old_hp = target_ship.hit_points
                            target_ship.damaged(amount)
                            print('Target was hit! HP:{}->{}'.format(old_hp, target_ship.hit_points))
                        else:
                            print('Missed!')
            else:
                params_error = True
        if params_error:
            print('FCS Error@{}: Amount of firing setup is mismatched.'.format(acting_ship.name))
            print('This could be caused by using disposable weapons more than 1 time in a round.')
    else:
        print('FCS Error@{}: weapon index exceeded current weapon amount.'.format(acting_ship.name))
        print('This could be caused by using disposable weapons more than 1 time in a round.')


def repair(action, order, acting_ship, extra_params):
    _, _ = order, extra_params
    amount = int((action[1] / 13) * acting_ship.max_hit_points * 0.5)
    old_hp = acting_ship.hit_points
    acting_ship.repair(amount)
    print(acting_ship.name, 'repaired itself! HP:{}->{}'.format(old_hp, acting_ship.hit_points))


def evade(action, order, acting_ship, extra_params):
    _, _ = order, extra_params
    effectiveness = action[1]
    amount = max(int((effectiveness / 13) * acting_ship.maneuver * 0.5), 1)
    evade_buff = Evade(acting_ship, amount)
    maneuver = acting_ship.maneuver
    evade_buff.trigger()
    print(acting_ship.name, 'is maneuvering for evading attacks!',
          'maneuver:{}->{}'.format(maneuver, acting_ship.maneuver))
    acting_ship.buff_list.append(evade_buff)


def defend(action, order, acting_ship, extra_params):
    _, _ = order, extra_params
    effectiveness = action[1]
    amount = max(int((effectiveness / 13) * acting_ship.armor * 0.5), 1)
    defend_buff = Defend(acting_ship, amount)
    armor = acting_ship.armor
    defend_buff.trigger()
    print(acting_ship.name, 'is preparing for impact!', 'armor:{}->{}'.format(armor, acting_ship.armor))
    acting_ship.buff_list.append(defend_buff)


def hit(basic_accuracy, maneuver, maneuver_target):
    accuracy = basic_accuracy
    bias = maneuver - maneuver_target
    bias /= ((maneuver + maneuver_target) / 2)
    accuracy += (100 * bias)
    accuracy = min(int(accuracy), 100)
    print('Hit chance is {}%'.format(accuracy))
    chances = [False] * 100
    selected = []
    indices = list(range(100))
    index = -1
    for _ in range(accuracy):
        while index not in indices or index in selected:
            index = random.choice(indices)
        selected.append(index)
    for index in selected:
        chances[index] = True
    return random.choice(chances)


basic_actions_dict = {
    'escape': [escape, '[interrupt, orders, acting_fleet]'],
    'idle': [idle, '[]'],
    'attack': [attack, '[fleets_and_actions]'],
    'repair': [repair, '[]'],
    'evade': [evade, '[]'],
    'defend': [defend, '[]']
}
