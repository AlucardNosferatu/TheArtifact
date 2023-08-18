import os
import random

from Classes.Fleet import Fleet

clear = True


# as 'pap'
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

    global clear
    actions = {}
    [actions.__setitem__(ship_uid, [None] * len(player_cards[ship_uid])) for ship_uid in player_cards.keys()]
    while True:
        clear = False
        cmd = pap_choice_1_first_glance()
        pap_tree_1(actions, cmd, enemy_fleet, fleet, player_cards)
        if check_ready(actions_=actions, fleet_=fleet):
            cmd = pap_choice_8_final_check()
            if cmd == '1':
                break
            elif cmd == '2':
                pass
    return actions


def pap_tree_1(actions, cmd, enemy_fleet, fleet, player_cards):
    global clear
    if cmd == '1':
        cmd = pap_choice_2_show_status()
        pap_tree_2(cmd, enemy_fleet, fleet)
    elif cmd == '2':
        uid_map = {}
        uid_list = list(fleet.ships.keys())
        [uid_map.__setitem__(str(index + 1), uid_list[index]) for index in range(len(uid_list))]
        cmd = pap_choice_3_select_executor(fleet, uid_list, uid_map)
        pap_tree_3(actions, cmd, enemy_fleet, fleet, player_cards, uid_list, uid_map)
    elif cmd == '3':
        clear = clear_screen(clear)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        [print(fleet.ships[ship_uid].name, actions[ship_uid]) for ship_uid in actions.keys()]


def pap_tree_2(cmd, enemy_fleet, fleet):
    if cmd == '1':
        fleet.show_fleet_status()
    elif cmd == '2':
        enemy_fleet.show_fleet_status()
    elif cmd == '3':
        pass


def pap_tree_3(actions, cmd, enemy_fleet, fleet, player_cards, uid_list, uid_map):
    global clear
    if cmd == str(len(uid_list) + 1):
        pass
    else:
        ship_uid = uid_map[cmd]
        if fleet.ships[ship_uid].is_destroyed():
            clear = clear_screen(clear)
            print('Ship:', fleet.ships[ship_uid].name, 'was destroyed!')
            pass
        else:
            chance_count = len(player_cards[ship_uid])
            cmd = pap_choice_4_select_chance(chance_count, fleet, ship_uid)
            chance_index = int(cmd) - 1
            cards = player_cards[ship_uid][chance_index]
            card_map = {}
            [card_map.__setitem__(str(index + 1), cards[index]) for index in range(len(cards))]
            cmd = pap_choice_5_select_action(card_map, cards, fleet, ship_uid)
            pap_tree_4(actions, card_map, cards, chance_index, cmd, enemy_fleet, fleet, ship_uid)


def pap_tree_4(actions, card_map, cards, chance_index, cmd, enemy_fleet, fleet, ship_uid):
    global clear
    if cmd == str(len(cards) + 1):
        pass
    else:
        card = card_map[cmd].copy()
        if card[0] == 'attack':
            if len(fleet.ships[ship_uid].weapons) > 0:
                cmd = pap_choice_6_select_weapon(fleet, ship_uid)
                pap_tree_5(actions, card, chance_index, cmd, enemy_fleet, fleet, ship_uid)
            else:
                print('There is no weapon in this ship! This ship will be idle after giving "attack" order!')
                card = ['idle', 1]
                actions[ship_uid][chance_index] = card
                print(fleet.ships[ship_uid].name, 'will do:', card, 'during next round.')
        else:
            actions[ship_uid][chance_index] = card
            clear = clear_screen(clear)
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            print(fleet.ships[ship_uid].name, 'will do:', card, 'during next round.')


def pap_tree_5(actions, card, chance_index, cmd, enemy_fleet, fleet, ship_uid):
    global clear
    weapons = fleet.ships[ship_uid].weapons
    if cmd == str(len(weapons) + 1):
        return False
    else:
        use_weapon = int(cmd) - 1
        card.append(use_weapon)
        if not hasattr(weapons[use_weapon], 'special_function'):
            target_count = weapons[use_weapon].target
            clear = clear_screen(clear)
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
                cmd = pap_choice_7_select_targets(enemy_fleet, target_list, target_map)
                if cmd == str(len(target_list) + 1):
                    back_flag = True
                    break
                elif cmd == str(len(target_list) + 2):
                    break
                else:
                    targets.append(target_map[cmd])
            if back_flag:
                return False
            else:
                targets = list(set(targets))
                card.append(targets)
                actions[ship_uid][chance_index] = card
                clear = clear_screen(clear)
                print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                print(fleet.ships[ship_uid].name, 'will do:', card, 'during next round.')
                return True
        else:
            actions[ship_uid][chance_index] = card
            clear = clear_screen(clear)
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            print(fleet.ships[ship_uid].name, 'will do:', card, 'during next round.')
            return True


def pap_choice_8_final_check():
    global clear
    cmd = ''
    while cmd not in ['1', '2']:
        clear = clear_screen(clear)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('All ships in your fleet were scheduled:')
        print('1.Make It Happen', end='\t')
        print('2.Wait A Minute')
        cmd = input()
    return cmd


def pap_choice_7_select_targets(enemy_fleet, target_list, target_map):
    global clear
    cmd = ''
    while cmd not in list(target_map.keys()) + [str(len(target_list) + 2)]:
        clear = clear_screen(clear)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        [print(
            key + '.', enemy_fleet.ships[target_map[key]].name,
            enemy_fleet.ships[target_map[key]].show_ship()
        ) for key in
            target_map.keys()]
        print(str(len(target_list) + 1) + '.', 'Back')
        print(str(len(target_list) + 2) + '.', 'OK')
        cmd = input()
    return cmd


def pap_choice_6_select_weapon(fleet, ship_uid):
    global clear
    weapons = fleet.ships[ship_uid].weapons
    cmd = ''
    while cmd not in [str(index + 1) for index in range(len(weapons) + 1)]:
        clear = clear_screen(clear)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('Select 1 weapon used by:', fleet.ships[ship_uid].name)
        [print(str(index + 1) + '.', 'Power:', weapons[index].power, 'Target:',
               weapons[index].target, end='\t') for index in range(len(weapons))]
        print(str(len(weapons) + 1) + '.', 'Back')
        cmd = input()
    return cmd


def pap_choice_5_select_action(card_map, cards, fleet, ship_uid):
    global clear
    cmd = ''
    while cmd not in list(card_map.keys()) + [str(len(cards) + 1)]:
        clear = clear_screen(clear)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('Select 1 action for:', fleet.ships[ship_uid].name)
        [print(key + '.', card_map[key], end='\t') for key in card_map.keys()]
        print(str(len(cards) + 1) + '.', 'Back')
        cmd = input()
    return cmd


def pap_choice_4_select_chance(chance_count, fleet, ship_uid):
    global clear
    cmd = ''
    while cmd not in [str(element) for element in range(1, chance_count + 1)]:
        clear = clear_screen(clear)
        print('Ship:', fleet.ships[ship_uid].name, 'has {} times to act'.format(chance_count))
        print(
            'Select chance to perform actions by input chance_index start from 1 to {}.'.format(
                chance_count
            )
        )
        cmd = input()
    return cmd


def pap_choice_3_select_executor(fleet, uid_list, uid_map):
    global clear
    row_length = 5
    cmd = ''
    while cmd not in list(uid_map.keys()) + [str(len(uid_list) + 1)]:
        clear = clear_screen(clear)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('Select 1 of your ships below:')
        um_copy = list(uid_map.keys()).copy()
        while len(um_copy) > 0:
            for i in range(min(row_length, len(um_copy))):
                key = um_copy.pop(0)
                print(key + '.', fleet.ships[uid_map[key]].name, end='\t')
            print()
        print(str(len(uid_list) + 1) + '.', 'Back')
        cmd = input()
    return cmd


def pap_choice_2_show_status():
    global clear
    cmd = ''
    while cmd not in ['1', '2', '3']:
        clear = clear_screen(clear)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('1.Your Fleet', end='\t')
        print("2.Enemies' Fleet", end='\t')
        print('3.Back')
        cmd = input()
    return cmd


def pap_choice_1_first_glance():
    global clear
    cmd = ''
    while cmd not in ['1', '2', '3']:
        clear = clear_screen(clear)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('You need to plan actions for each ship in your fleet now.')
        print('1.Show Status', end='\t')
        print('2.Plan Actions', end='\t')
        print("3.What's the plan?")
        cmd = input()
    return cmd


def plan_actions(enemy_fleet: Fleet, fleet: Fleet, cards):
    actions = {}
    for ship_uid in cards.keys():
        actions.__setitem__(ship_uid, [])
        for action_chance in cards[ship_uid]:
            card = random.choice(action_chance)
            if card[0] == 'attack':
                if len(fleet.ships[ship_uid].weapons) > 0:
                    use_weapon = random.randint(0, len(fleet.ships[ship_uid].weapons) - 1)
                    card.append(use_weapon)
                    if not hasattr(fleet.ships[ship_uid].weapons[use_weapon], 'special_function'):
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
                else:
                    card = ['idle', 1]
            actions[ship_uid].append(card)
    return actions


def clear_screen(clear_):
    if not clear_:
        clear_ = True
    else:
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
    return clear_
