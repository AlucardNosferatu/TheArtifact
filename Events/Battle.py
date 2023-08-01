import random

from Classes.Fleet import Fleet
from Utils import generate_fleet, show_ship


def battle_event(fleet, enemy_fleet=None):
    print('You encountered a fleet of enemies!')
    if enemy_fleet is None:
        enemy_fleet = generate_fleet(10, 20)
    while True:
        orders = arrange_orders(fleet, enemy_fleet)
        enemy_cards = spawn_actions(enemy_fleet)
        player_cards = spawn_actions(fleet)
        enemy_actions = plan_actions(fleet, enemy_fleet, enemy_cards)
        player_actions = plan_actions_player(enemy_fleet, fleet, player_cards)
        orders = make_it_happen(fleet, enemy_fleet, player_actions, enemy_actions, orders)
        if should_it_break(fleet, enemy_fleet, orders):
            break
    fleet = remove_destroyed(fleet)
    return fleet


def arrange_orders(fleet_a: Fleet, fleet_b: Fleet):
    orders = [[fleet_a.ships[ship].uid, fleet_a.ships[ship].speed, 'FleetA'] for ship in fleet_a.ships.keys()]
    orders += [[fleet_b.ships[ship].uid, fleet_b.ships[ship].speed, 'FleetB'] for ship in fleet_b.ships.keys()]
    speeds = [ship_info[1] for ship_info in orders]
    new_orders = []
    while len(speeds) > 1:
        assert len(speeds) == len(orders)
        max_speed = max(speeds)
        max_speed_count = speeds.count(max_speed)
        max_speed_indices = []
        prev_max_speed_index = -1
        for _ in range(max_speed_count):
            prev_max_speed_index = speeds.index(max_speed, prev_max_speed_index + 1)
            max_speed_indices.append(prev_max_speed_index)
        msi_copy = max_speed_indices.copy()
        while len(max_speed_indices) > 0:
            pop_index = random.choice(max_speed_indices)
            max_speed_indices.remove(pop_index)
            new_orders.append(orders[pop_index])
        msi_copy.sort()
        while len(msi_copy) > 0:
            pop_index = msi_copy.pop(-1)
            speeds.pop(pop_index)
            orders.pop(pop_index)
    return new_orders


def spawn_actions(fleet):
    cards_dict = {}
    for ship_uid in fleet.ships.keys():
        cards = []
        if fleet.ships[ship_uid].is_destroyed():
            cards.append(['idle', 1])
        else:
            for _ in range(5):
                card_type = random.choice(['attack', 'repair', 'idle', 'escape'])
                card_point = random.randint(1, 13)
                cards.append([card_type, card_point])
        cards_dict.__setitem__(ship_uid, cards.copy())
    return cards_dict


def plan_actions(enemy_fleet: Fleet, fleet: Fleet, cards):
    actions = {}
    for ship_uid in fleet.ships.keys():
        card = random.choice(cards[ship_uid])
        if card[0] == 'attack':
            use_weapon = random.randint(0, len(fleet.ships[ship_uid].weapons) - 1)
            card.append(use_weapon)
            target_count = fleet.ships[ship_uid].weapons[use_weapon].target
            targets = []
            valid_targets = 0
            for ship_uid_ in enemy_fleet.ships.keys():
                if not enemy_fleet.ships[ship_uid_].is_destroyed():
                    valid_targets += 1
            for i in range(min(valid_targets, target_count)):
                selected = random.choice(list(enemy_fleet.ships.keys()))
                while selected in targets:
                    selected = random.choice(list(enemy_fleet.ships.keys()))
                targets.append(selected)
            card.append(targets)
        actions.__setitem__(ship_uid, card)
    return actions


def plan_actions_player(enemy_fleet, fleet, player_cards):
    # todo: implement interactive actions planning
    actions = plan_actions(enemy_fleet, fleet, player_cards)
    return actions


def make_it_happen(fleet_a: Fleet, fleet_b: Fleet, actions_a, actions_b, orders):
    fleets_and_actions = {'FleetA': [fleet_a, actions_a, 'FleetB'], 'FleetB': [fleet_b, actions_b, 'FleetA']}
    will_to_fight = {'FleetA': 5, 'FleetB': 5}
    while len(orders) > 0:
        order = orders.pop(0)
        action = fleets_and_actions[order[2]][1][order[0]]
        ship = fleets_and_actions[order[2]][0].ships[order[0]]
        if not ship.is_destroyed():
            if action[0] == 'idle':
                print(order[0], 'waits for a better chance!')
            elif action[0] == 'repair':
                amount = int((order[1] / 13) * ship.max_hit_points * 0.75)
                ship.repair(amount)
                print(order[0], 'repairs itself!')
                show_ship(ship)
            elif action[0] == 'attack':
                amount = ship.weapons[action[2]].power
                print(order[0], 'fires on active target(s)!')
                for target_uid in action[3]:
                    target_ship = fleets_and_actions[fleets_and_actions[order[2]][2]][0].ships[target_uid]
                    if not target_ship.is_destroyed():
                        target_ship.damaged(amount)
                        print(target_uid, 'was fired by', order[0], '!')
                        show_ship(target_ship)
            elif action[0] == 'escape':
                fleet_names = {'FleetA': "Player's Fleet", 'FleetB': "Enemies' Fleet"}
                print(fleet_names[order[2]], 'is about to escape.')
                if will_to_fight[order[2]] <= 0:
                    while len(orders) <= 0:
                        orders.append(None)
                    print(fleet_names[order[2]], 'escapes from the battle zone.')
                    break
                else:
                    will_to_fight[order[2]] -= 1
            else:
                raise ValueError('Wrong action type:', action[0])
        else:
            print(order[0], 'was destroyed, it cannot do anything!')
        print('==========================================================================')
    return orders


def should_it_break(fleet_a, fleet_b, orders):
    return len(orders) > 0 or fleet_a.ships[fleet_a.flag_ship].is_destroyed() or fleet_b.ships[
        fleet_b.flag_ship].is_destroyed()


def remove_destroyed(fleet: Fleet):
    blacklist = []
    for ship_uid in fleet.ships.keys():
        if ship_uid != fleet.flag_ship and fleet.ships[ship_uid].is_destroyed():
            blacklist.append(ship_uid)
    for ship_uid in blacklist:
        del fleet.ships[ship_uid]
    return fleet


if __name__ == '__main__':
    fa = generate_fleet(10, 20)
    fa = battle_event(fa)
