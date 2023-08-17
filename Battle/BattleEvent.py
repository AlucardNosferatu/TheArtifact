import random

from Battle.BattleActions import basic_actions_dict
from Battle.BattleOverride import override_control, override_orders, override_init
from Battle.BattlePlan import plan_actions_player, plan_actions, clear_screen
from Classes.Event import Event
from Classes.Fleet import Fleet
from Classes.Ship import Ship
from Utils import generate_fleet
from Weapons.Melee import Boarding, Salvage

clear = True


def battle_event(fleet_p, fleet_e=None, clear_=True):
    def count_killed(enemy_fleet_):
        score_per_ship = 10
        change_score_ = 0
        loots_ = []
        for ship_uid in enemy_fleet_.ships:
            if enemy_fleet_.ships[ship_uid].is_destroyed():
                change_score_ += score_per_ship
                loots_ += enemy_fleet_.ships[ship_uid].weapons
        return change_score_, loots_

    global clear
    override_enabled = fleet_p.ships[fleet_p.flag_ship].override_enabled
    if clear_:
        clear = True
    else:
        clear = False
    clear = clear_screen(clear)
    print('You encountered a fleet of enemies!')
    if fleet_e is None:
        player_fleet_scale = len(list(fleet_p.ships.keys()))
        deviant = 1
        fleet_e = generate_fleet(max(1, player_fleet_scale - deviant), player_fleet_scale + deviant)
    fleet_p.reset_w2f()
    fleet_e.reset_w2f()
    while True:
        if override_enabled:
            cmd = ''
            while cmd not in ['y', 'n']:
                cmd = input('Override FlagShip?[y/n]')
        else:
            cmd = 'n'
        orders = arrange_orders(fleet_p, fleet_e)
        if cmd == 'y':
            orders, override_chances = override_orders(fleet_p, orders)
        elif cmd == 'n':
            override_chances = 0
        else:
            raise ValueError('Override FlagShip?[y/n]')
        cards_p = spawn_actions(fleet_p, orders)
        cards_e = spawn_actions(fleet_e, orders)
        actions_e = plan_actions(fleet_p, fleet_e, cards_e)
        if cmd == 'n':
            actions_p = plan_actions_player(fleet_e, fleet_p, cards_p)
        elif cmd == 'y':
            actions_p = plan_actions(fleet_e, fleet_p, cards_p)
        else:
            raise ValueError('Override FlagShip?[y/n]')
        orders = make_it_happen(fleet_p, fleet_e, actions_p, actions_e, orders, override_chances)
        # god mode
        # fleet.ships[fleet.flag_ship].hit_points = fleet.ships[fleet.flag_ship].max_hit_points
        change_score, loots = count_killed(fleet_e)
        buffs_decay(fleet_p)
        buffs_decay(fleet_e)
        break_loop = should_it_break(fleet_p, fleet_e, orders)
        buffs_clear(fleet_p, break_loop)
        buffs_clear(fleet_e, break_loop)
        if break_loop:
            break
    fleet_p = remove_destroyed(fleet_p)
    fleet_p.storage += loots
    print('Loots after battle:')
    for i in range(len(loots)):
        weapon = loots[i]
        print('++++++++Weapons++++++++')
        print('■Storage ID:', fleet_p.storage.index(weapon), '■Power:', weapon.power, '■Targets:', weapon.target)
    setattr(fleet_p, 'enemy_fleet', fleet_e)
    return fleet_p, change_score


class BattleEvent(Event):
    def __init__(self, customized_event=None):
        if customized_event is None:
            customized_event = battle_event
        super().__init__(customized_event)
        self.fleet = None

    def __call__(self, *args, **kwargs):
        if self.fleet is None:
            fleet, score = self.event_function(*args, **kwargs)
        else:
            print('ATTENTION: This hostile fleet was engaged before.')
            fleet, score = self.event_function(fleet_e=self.fleet, *args, **kwargs)
        if fleet.battle_result == 'win':
            self.end = True
        else:
            self.fleet = fleet.enemy_fleet
            delattr(fleet, 'enemy_fleet')
        delattr(fleet, 'battle_result')
        return fleet, score


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


def spawn_actions(fleet, orders):
    cards_dict = {}
    for ship_uid in list(fleet.ships.keys()):
        cards = [[] for order in orders if order[0] == ship_uid]
        if len(cards) > 0:
            for action_chance in range(len(cards)):
                if fleet.ships[ship_uid].is_destroyed():
                    cards[action_chance].append(['idle', 1])
                else:
                    for _ in range(5):
                        card_type = random.choice(['attack', 'repair', 'idle', 'escape', 'evade', 'defend'])
                        card_point = random.randint(1, 13)
                        cards[action_chance].append([card_type, card_point])
            cards_dict.__setitem__(ship_uid, cards.copy())
    return cards_dict


def make_it_happen(fleet_a: Fleet, fleet_b: Fleet, actions_a, actions_b, orders, override_chances=0):
    fleets_and_actions = {'FleetA': [fleet_a, actions_a, 'FleetB'], 'FleetB': [fleet_b, actions_b, 'FleetA']}
    interrupt = [False]
    if override_chances > 0:
        print('============WARNING!=============')
        print('============WARNING!=============')
        print('============WARNING!=============')
        print('===Override Control Initiated!===')
        override_init(override_chances)
    while len(orders) > 0 and not interrupt[0]:
        order = orders.pop(0)
        # noinspection PyUnresolvedReferences
        acting_fleet = fleets_and_actions[order[2]][0]
        action = fleets_and_actions[order[2]][1][order[0]].pop(0)
        if order[0] not in acting_fleet.ships.keys():
            print('The order cannot be executed as the executor was no longer in the fleet!')
            continue
        acting_ship = acting_fleet.ships[order[0]]
        if not acting_ship.is_destroyed():
            if action[0] in basic_actions_dict.keys():
                action_function = basic_actions_dict[action[0]][0]
                extra_params = eval(basic_actions_dict[action[0]][1])
                action_function(action, order, acting_ship, extra_params=extra_params)
            else:
                raise ValueError('Wrong action type:', action[0])
        else:
            print(acting_ship.name, 'was destroyed, it cannot do anything!')
        if override_chances > 0:
            if fleet_a.ships[fleet_a.flag_ship].is_destroyed():
                print('##ERROR##ERROR##ERROR##ERROR##ERROR##ERROR##ERROR##ERROR##')
                print('The Flagship was destroyed! Cannot start Override Control!')
                print('##ERROR##ERROR##ERROR##ERROR##ERROR##ERROR##ERROR##ERROR##')
            else:
                packed_ep = {
                    'interrupt': interrupt,
                    'orders': orders,
                    'acting_fleet': acting_fleet,
                    'fleets_and_actions': fleets_and_actions
                }
                override_control(fleet_a, fleet_b, packed_ep=packed_ep)
        print('==========================================================================')
    return orders


def buffs_clear(fleet, clear_buff=False):
    for ship_uid in fleet.ships:
        buff_count = len(fleet.ships[ship_uid].buff_list)
        for index in range(buff_count):
            index = buff_count - index - 1
            if fleet.ships[ship_uid].buff_list[index].expired or clear_buff:
                fleet.ships[ship_uid].buff_list.pop(index)


def buffs_decay(fleet):
    uid_list = list(fleet.ships.keys())
    for ship_uid in uid_list:
        if ship_uid in fleet.ships.keys():
            buff_ship = fleet.ships[ship_uid]
            buff_count = len(buff_ship.buff_list)
            for index in range(buff_count):
                index = buff_count - index - 1
                buff_ship.buff_list[index].decay()


def should_it_break(fleet_a, fleet_b, orders):
    if len(orders) > 0:
        print('A fleet that joined this battle has withdrawn so the fight was over.')
        setattr(fleet_a, 'battle_result', 'escape')
    elif fleet_a.ships[fleet_a.flag_ship].is_destroyed():
        print('Your flagship was destroyed so the fight was over.')
        setattr(fleet_a, 'battle_result', 'lose')
    elif fleet_b.ships[fleet_b.flag_ship].is_destroyed():
        print("Enemies' flagship was destroyed so the fight was over.")
        setattr(fleet_a, 'battle_result', 'win')
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
    fa = generate_fleet(2, 2)

    acting_ship_: Ship = [fa.ships[ship_uid] for ship_uid in fa.ships.keys() if ship_uid != fa.flag_ship][0]
    acting_ship_.fire_control_system = 100
    acting_ship_.maneuver = 100
    acting_ship_.change_speed(amount=7, allow_exceed=True)
    acting_ship_.install_weapon(Boarding(acting_ship=acting_ship_))

    acting_ship_ = fa.ships[fa.flag_ship]
    acting_ship_.fire_control_system = 100
    acting_ship_.maneuver = 100
    acting_ship_.change_speed(amount=7, allow_exceed=True)
    acting_ship_.install_weapon(Salvage(acting_ship=acting_ship_))

    fb = generate_fleet(2, 2)
    fa = battle_event(fa, fb)
