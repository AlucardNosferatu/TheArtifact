import os
import random

from Classes.Fleet import Fleet
from Utils import generate_fleet, show_ship, show_status


def battle_event(fleet, enemy_fleet=None):
    def count_killed(enemy_fleet_):
        score_per_ship = 10
        change_score_ = 0
        for ship_uid in enemy_fleet_.ships:
            if enemy_fleet_.ships[ship_uid].is_destroyed():
                change_score_ += score_per_ship
        return change_score_

    os.system('cls' if os.name == 'nt' else "printf '\033c'")
    print('You encountered a fleet of enemies!')
    if enemy_fleet is None:
        player_fleet_scale = len(list(fleet.ships.keys()))
        deviant = 2
        enemy_fleet = generate_fleet(max(1, player_fleet_scale - deviant), player_fleet_scale + deviant)
    will_to_fight = {'FleetA': len(list(fleet.ships.keys())), 'FleetB': len(list(enemy_fleet.ships.keys()))}
    while True:
        orders = arrange_orders(fleet, enemy_fleet)
        cards = spawn_actions(fleet, enemy_fleet, orders)
        enemy_cards = {}
        [enemy_cards.__setitem__(suid, cards[suid]) for suid in cards if suid in enemy_fleet.ships.keys()]
        player_cards = {}
        [player_cards.__setitem__(suid, cards[suid]) for suid in cards if suid in fleet.ships.keys()]
        enemy_actions = plan_actions(fleet, enemy_fleet, enemy_cards)
        player_actions = plan_actions_player(enemy_fleet, fleet, player_cards)
        orders = make_it_happen(fleet, enemy_fleet, player_actions, enemy_actions, orders, will_to_fight)
        change_score = count_killed(enemy_fleet)
        if should_it_break(fleet, enemy_fleet, orders):
            break
    fleet = remove_destroyed(fleet)
    return fleet, change_score


def arrange_orders(fleet_a: Fleet, fleet_b: Fleet):
    def get_action_times(speed_, round_duration_, battlefield_size_):
        action_duration = battlefield_size_ / speed_
        action_times = round_duration_ // action_duration
        lead_time = round_duration_ % action_duration
        return [action_times, lead_time]

    ships2orders = [[fleet_a.ships[ship].uid, fleet_a.ships[ship].speed, 'FleetA'] for ship in fleet_a.ships.keys()]
    ships2orders += [[fleet_b.ships[ship].uid, fleet_b.ships[ship].speed, 'FleetB'] for ship in fleet_b.ships.keys()]
    ships2orders_new = []
    ships2speeds = [ship_info[1] for ship_info in ships2orders]
    min_speed = min(ships2speeds)
    battlefield_size = len(list(fleet_a.ships.keys())) + len(list(fleet_b.ships.keys()))
    round_duration = battlefield_size / min_speed
    ships2speeds = [get_action_times(speed, round_duration, battlefield_size) for speed in ships2speeds]
    ships2rounds = [speed[0] for speed in ships2speeds]
    ships2leads = [speed[1] for speed in ships2speeds]
    total_rounds = int(max(ships2rounds))
    for round_nth in range(1, total_rounds + 1):
        orders_in_round = []
        ships_in_round = []
        for ship_index in range(len(ships2rounds)):
            if ships2rounds[ship_index] >= round_nth:
                ships_in_round.append(ship_index)
        leads_in_round = [ships2leads[index] for index in ships_in_round]

        while len(leads_in_round) > 0:
            assert len(ships_in_round) == len(leads_in_round)
            max_lead = max(leads_in_round)
            max_lead_count = leads_in_round.count(max_lead)
            max_lead_indices = []
            prev_max_lead_index = -1
            for _ in range(max_lead_count):
                prev_max_lead_index = leads_in_round.index(max_lead, prev_max_lead_index + 1)
                max_lead_indices.append(prev_max_lead_index)
            mli_copy = max_lead_indices.copy()
            while len(max_lead_indices) > 0:
                pop_index = random.choice(max_lead_indices)
                max_lead_indices.remove(pop_index)
                orders_in_round.append(ships_in_round[pop_index])
            mli_copy.sort()
            while len(mli_copy) > 0:
                pop_index = mli_copy.pop(-1)
                leads_in_round.pop(pop_index)
                ships_in_round.pop(pop_index)
        orders_in_round = [ships2orders[index] for index in orders_in_round]
        ships2orders_new = orders_in_round + ships2orders_new
    return ships2orders_new


def spawn_actions(fleet_a, fleet_b, orders):
    fleets_dict = {'FleetA': fleet_a, 'FleetB': fleet_b}
    cards_dict = {}
    for ship_uid in list(fleet_a.ships.keys()) + list(fleet_b.ships.keys()):
        cards = [[order[2]] for order in orders if order[0] == ship_uid]
        faction = cards[0][0]
        [cards_.pop(0) for cards_ in cards]
        for action_chance in range(len(cards)):
            if fleets_dict[faction].ships[ship_uid].is_destroyed():
                cards[action_chance].append(['idle', 1])
            else:
                for _ in range(5):
                    card_type = random.choice(['attack', 'repair', 'idle', 'escape'])
                    card_point = random.randint(1, 13)
                    cards[action_chance].append([card_type, card_point])
        cards_dict.__setitem__(ship_uid, cards.copy())
    return cards_dict


def plan_actions(enemy_fleet: Fleet, fleet: Fleet, cards):
    actions = {}
    for ship_uid in fleet.ships.keys():
        actions.__setitem__(ship_uid, [])
        for action_chance in cards[ship_uid]:
            card = random.choice(action_chance)
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
            actions[ship_uid].append(card)
    return actions


def plan_actions_player(enemy_fleet, fleet, player_cards):
    def check_ready(actions_, fleet_):
        for ship_uid in actions_.keys():
            if None in actions_[ship_uid]:
                if fleet_.ships[ship_uid].is_destroyed():
                    for index in range(len(actions_[ship_uid])):
                        actions_[ship_uid][index] = ['idle', 1]
                else:
                    return False
        return True

    actions = {}
    [actions.__setitem__(ship_uid, [None] * len(player_cards[ship_uid])) for ship_uid in player_cards.keys()]
    while True:
        cmd = ''
        clear = False
        while cmd not in ['1', '2', '3']:
            if not clear:
                clear = True
            else:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            print('You need to plan actions for each ship in your fleet now.')
            print('1.Show Status', end='\t')
            print('2.Plan Actions', end='\t')
            print("3.What's the plan?")
            cmd = input()
        if cmd == '1':
            cmd = ''
            while cmd not in ['1', '2', '3']:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                print('1.Your Fleet', end='\t')
                print("2.Enemies' Fleet", end='\t')
                print('3.Back')
                cmd = input()
            if cmd == '1':
                show_status(fleet)
            elif cmd == '2':
                show_status(enemy_fleet)
            elif cmd == '3':
                pass
        elif cmd == '2':
            uid_map = {}
            uid_list = list(fleet.ships.keys())
            [uid_map.__setitem__(str(index + 1), uid_list[index]) for index in range(len(uid_list))]
            cmd = ''
            while cmd not in list(uid_map.keys()) + [str(len(uid_list) + 1)]:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                [print(key + '.', fleet.ships[uid_map[key]].name, end='\t') for key in uid_map.keys()]
                print(str(len(uid_list) + 1) + '.', 'Back')
                cmd = input()
            if cmd == str(len(uid_list) + 1):
                pass
            else:
                ship_uid = uid_map[cmd]
                if fleet.ships[ship_uid].is_destroyed():
                    os.system('cls' if os.name == 'nt' else "printf '\033c'")
                    print('Ship:', fleet.ships[ship_uid].name, 'was destroyed!')
                    pass
                else:
                    chance_count = len(player_cards[ship_uid])
                    cmd = ''
                    while cmd not in [str(element) for element in range(1, chance_count + 1)]:
                        os.system('cls' if os.name == 'nt' else "printf '\033c'")
                        print('Ship:', fleet.ships[ship_uid].name, 'has {} times to act'.format(chance_count))
                        print(
                            'Select chance to perform actions by input chance_index start from 1 to {}.'.format(
                                chance_count
                            )
                        )
                        cmd = input()
                    chance_index = int(cmd) - 1
                    cards = player_cards[ship_uid][chance_index]
                    card_map = {}
                    [card_map.__setitem__(str(index + 1), cards[index]) for index in range(len(cards))]
                    cmd = ''
                    while cmd not in list(card_map.keys()) + [str(len(cards) + 1)]:
                        os.system('cls' if os.name == 'nt' else "printf '\033c'")
                        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                        print('Select 1 action for:', fleet.ships[ship_uid].name)
                        [print(key + '.', card_map[key], end='\t') for key in card_map.keys()]
                        print(str(len(cards) + 1) + '.', 'Back')
                        cmd = input()
                    if cmd == str(len(cards) + 1):
                        pass
                    else:
                        card = card_map[cmd].copy()
                        if card[0] == 'attack':
                            weapons = fleet.ships[ship_uid].weapons
                            cmd = ''
                            while cmd not in [str(index + 1) for index in range(len(weapons) + 1)]:
                                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                                print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                                print('Select 1 weapon used by:', fleet.ships[ship_uid].name)
                                [print(str(index + 1) + '.', 'Power:', weapons[index].power, 'Target:',
                                       weapons[index].target, end='\t') for index in range(len(weapons))]
                                print(str(len(weapons) + 1) + '.', 'Back')
                                cmd = input()
                            if cmd == str(len(weapons) + 1):
                                pass
                            else:
                                use_weapon = int(cmd) - 1
                                target_count = weapons[use_weapon].target
                                card.append(use_weapon)
                                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                                print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                                print('Select {} targets fired by:'.format(target_count), fleet.ships[ship_uid].name)
                                print('*CAUTION*', 'Destroyed targets will be ignored during execution!')
                                print('*CAUTION*', 'Duplicated targets will only be fired once!')
                                targets = []
                                target_map = {}
                                target_list = list(enemy_fleet.ships.keys())
                                [target_map.__setitem__(str(index + 1), target_list[index]) for index in
                                 range(len(target_list))]
                                back_flag = False
                                for _ in range(target_count):
                                    cmd = ''
                                    while cmd not in list(target_map.keys()) + [str(len(target_list) + 2)]:
                                        os.system('cls' if os.name == 'nt' else "printf '\033c'")
                                        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                                        [print(key + '.', enemy_fleet.ships[target_map[key]].name,
                                               show_ship(enemy_fleet.ships[target_map[key]])) for key in
                                         target_map.keys()]
                                        print(str(len(target_list) + 1) + '.', 'Back')
                                        print(str(len(target_list) + 2) + '.', 'OK')
                                        cmd = input()
                                    if cmd == str(len(target_list) + 1):
                                        back_flag = True
                                        break
                                    elif cmd == str(len(target_list) + 2):
                                        break
                                    else:
                                        targets.append(target_map[cmd])
                                if back_flag:
                                    pass
                                else:
                                    targets = list(set(targets))
                                    card.append(targets)
                                    actions[ship_uid][chance_index] = card
                                    os.system('cls' if os.name == 'nt' else "printf '\033c'")
                                    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                                    print(fleet.ships[ship_uid].name, 'will do:', card, 'during next round.')
                        else:
                            actions[ship_uid][chance_index] = card
                            os.system('cls' if os.name == 'nt' else "printf '\033c'")
                            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                            print(fleet.ships[ship_uid].name, 'will do:', card, 'during next round.')
        elif cmd == '3':
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            [print(fleet.ships[ship_uid].name, actions[ship_uid]) for ship_uid in actions.keys()]
        if check_ready(actions_=actions, fleet_=fleet):
            cmd = ''
            while cmd not in ['1', '2']:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                print('All ships in your fleet were scheduled:')
                print('1.Make It Happen', end='\t')
                print('2.Wait A Minute')
                cmd = input()
            if cmd == '1':
                break
            elif cmd == '2':
                pass
    return actions


def make_it_happen(fleet_a: Fleet, fleet_b: Fleet, actions_a, actions_b, orders, will_to_fight):
    fleets_and_actions = {'FleetA': [fleet_a, actions_a, 'FleetB'], 'FleetB': [fleet_b, actions_b, 'FleetA']}
    while len(orders) > 0:
        order = orders.pop(0)
        # noinspection PyUnresolvedReferences
        action = fleets_and_actions[order[2]][1][order[0]].pop(0)
        ship = fleets_and_actions[order[2]][0].ships[order[0]]
        if not ship.is_destroyed():
            if action[0] == 'idle':
                print(ship.name, 'waits for a better chance!')
            elif action[0] == 'repair':
                amount = int((order[1] / 13) * ship.max_hit_points * 0.5)
                ship.repair(amount)
                print(ship.name, 'repairs itself!')
                show_ship(ship)
            elif action[0] == 'attack':
                amount = int((((order[1] - 6) / 13) + 1) * ship.weapons[action[2]].power)
                print(ship.name, 'fires on active target(s)!')
                for target_uid in action[3]:
                    target_ship = fleets_and_actions[fleets_and_actions[order[2]][2]][0].ships[target_uid]
                    if not target_ship.is_destroyed():
                        target_ship.damaged(amount)
                        print(target_ship.name, 'was fired by', ship.name, '!')
                        show_ship(target_ship)
            elif action[0] == 'escape':
                fleet_names = {'FleetA': "Player's Fleet", 'FleetB': "Enemies' Fleet"}
                print(fleet_names[order[2]], 'is about to escape. {} is evading combat.'.format(ship.name))
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
                    if will_to_fight[order[2]] <= 1:
                        while len(orders) <= 0:
                            orders.append(None)
                        print('It escaped from the battle zone.')
                        break
                    else:
                        will_to_fight[order[2]] -= 1
                        print("It flew for a while, but it hasn't been out of battle zone yet.")
            else:
                raise ValueError('Wrong action type:', action[0])
        else:
            print(ship.name, 'was destroyed, it cannot do anything!')
        print('==========================================================================')
    return orders


def should_it_break(fleet_a, fleet_b, orders):
    if len(orders) > 0:
        print('A fleet that joined this battle has withdrawn so the fight was over.')
    elif fleet_a.ships[fleet_a.flag_ship].is_destroyed():
        print('Your flagship was destroyed so the fight was over.')
    elif fleet_b.ships[fleet_b.flag_ship].is_destroyed():
        print("Enemies' flagship was destroyed so the fight was over.")
    else:
        return False
    return True


def remove_destroyed(fleet: Fleet):
    blacklist = []
    for ship_uid in fleet.ships.keys():
        if ship_uid != fleet.flag_ship and fleet.ships[ship_uid].is_destroyed():
            blacklist.append(ship_uid)
    for ship_uid in blacklist:
        del fleet.ships[ship_uid]
    return fleet


if __name__ == '__main__':
    fa = generate_fleet(1, 1)
    fa = battle_event(fa)
