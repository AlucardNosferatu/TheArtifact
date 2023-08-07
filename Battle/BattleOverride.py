import random
import time

from Battle.BattleActions import basic_actions_dict
from Battle.BattleOverrideActions import overload_weapon, redistribute_firepower
from Battle.BattlePlan import pap_choice_6_select_weapon, pap_tree_5, pap_choice_2_show_status, pap_tree_2
from Classes.Fleet import Fleet

chances = [0]
override_actions_dict_sample = {
    'Overload Weapon': [overload_weapon, 'Over-charge all weapons installed at a cost of 20% HP.'],
    'Redistribute Firepower': [redistribute_firepower, 'Focus energy on less targets to raise power, or vice versa.']
}


class OverrideActions:
    skill_points = None
    basic_actions_dict = basic_actions_dict
    override_actions_dict = None

    def __init__(self):
        self.skill_points = 0
        # self.override_actions_dict = {}
        self.override_actions_dict = override_actions_dict_sample

    def learn(self):
        pass

    def forget(self):
        pass

    def use(self):
        pass

    def interaction(self, fleet_a, fleet_b, round_chance: list[int], packed_ep):
        def prompt(rc):
            print('{} chances for basic actions left!\nAvailable action types:'.format(round_chance[0]))
            if rc[0] > 0:
                print('1.Basic Actions')
                print('2.Override Actions')
                print('3.Show Status')
                e = {'1': self.basic_act, '2': self.override_act, '3': self.show_status}
            else:
                print('1.Override Actions')
                print('2.Show Status')
                e = {'1': self.override_act, '2': self.show_status}
            return e

        while True:
            entries = prompt(round_chance)
            cmd = input()
            while cmd not in entries.keys():
                entries = prompt(round_chance)
                cmd = input()
            # noinspection PyArgumentList
            finished = entries[cmd](fleet_a, fleet_b, round_chance, packed_ep)
            if finished:
                break

    def override_act(self, fleet_a, fleet_b, round_chance, packed_ep):
        _, _, _ = fleet_b, round_chance, packed_ep
        options, keys = self.prompt_input(ad=self.override_actions_dict)
        cmd = input()
        while cmd not in options:
            options, keys = self.prompt_input(ad=self.override_actions_dict)
            cmd = input()
        if cmd == options[-1]:
            return False
        else:
            act_name = keys[int(cmd) - 1]
            print(self.override_actions_dict[act_name][1])
            cmd = ''
            while cmd not in ['y', 'n']:
                cmd = input('Confirm?[y/n]')
            if cmd == 'y':
                acting_ship = fleet_a.ships[fleet_a.flag_ship]
                finished = self.override_actions_dict[act_name][0](acting_ship)
                return finished
            elif cmd == 'n':
                return False

    def basic_act(self, fleet_a, fleet_b, round_chance, packed_ep):
        assert round_chance[0] > 0
        options, keys = self.prompt_input(ad=self.basic_actions_dict)
        cmd = input()
        while cmd not in options:
            options, keys = self.prompt_input(ad=self.basic_actions_dict)
            cmd = input()
        if cmd == options[-1]:
            return False
        else:
            act_name, acting_ship, action, order, set_weapon = self.fake_basic_action(cmd, fleet_a, fleet_b, keys)
            if not set_weapon:
                return False
            else:
                action_function = self.basic_actions_dict[act_name][0]
                ep_need = self.unpack_ep(pe=packed_ep, an=act_name)
                action_function(action, order, acting_ship, extra_params=ep_need)
                round_chance[0] -= 1
                return True

    @staticmethod
    def show_status(fleet_a, fleet_b, round_chance, packed_ep):
        _, _ = round_chance, packed_ep
        cmd = pap_choice_2_show_status()
        pap_tree_2(cmd, fleet_b, fleet_a)
        return False

    @staticmethod
    def prompt_input(ad):
        last_index = 0
        ks = list(ad.keys())
        for i in range(len(ks)):
            print('{}.{}'.format(i + 1, list(ad.keys())[i]), end='\t')
            last_index = i
        print('{}.{}'.format(last_index + 2, 'Back'))
        opts = [str(index) for index in list(range(1, last_index + 3))]
        return opts, ks

    @staticmethod
    def fake_basic_action(weapon_index, fleet_a, fleet_b, keys):
        act_name = keys[int(weapon_index) - 1]
        action = [act_name, random.randint(1, 13)]
        acting_ship = fleet_a.ships[fleet_a.flag_ship]
        order = [fleet_a.flag_ship, fleet_a.ships[fleet_a.flag_ship].speed, 'FleetA']
        if act_name == 'attack':
            weapon_index = pap_choice_6_select_weapon(fleet_a, fleet_a.flag_ship)
            set_weapon = pap_tree_5(
                {fleet_a.flag_ship: [None]}, action, 0, weapon_index, fleet_b, fleet_a, fleet_a.flag_ship
            )
        else:
            set_weapon = True
        return act_name, acting_ship, action, order, set_weapon

    @staticmethod
    def unpack_ep(pe, an):
        for key in pe.keys():
            exec_str = "{}=pe['{}']".format(key, key)
            exec(exec_str)
        en = eval(basic_actions_dict[an][1])
        return en


def override_orders(fleet_p, orders):
    override_chances = []
    [override_chances.append(index) for index in range(len(orders)) if orders[index][0] == fleet_p.flag_ship]
    override_chances.sort()
    override_chances.reverse()
    for index in override_chances:
        orders.pop(index)
    print('SysOC: There will be {} chances for basic actions during this round!'.format(len(override_chances)))
    return orders, len(override_chances)


def override_init(override_chances):
    global chances
    chances[0] = override_chances


def override_control(fleet_p: Fleet, fleet_e: Fleet, packed_ep):
    # noinspection SpellCheckingInspection
    def fancy_animation():
        print('(T)ransient.', end='')
        time.sleep(0.25)
        print('(R)eflection.', end='')
        time.sleep(0.25)
        print('(A)ugmented.', end='')
        time.sleep(0.25)
        print('(N)eural.', end='')
        time.sleep(0.25)
        print('(S)ystem.', end='')
        time.sleep(0.25)
        print('-(A)ctive.', end='')
        time.sleep(0.25)
        print('(M)ode.')
        time.sleep(1)
        print('=============================T.R.A.N.S-A.M.=============================')

    global chances
    fancy_animation()
    print('{} <<<Override-Control>>> left in this round!'.format(len(packed_ep['orders']) + 1))
    # todo: implement override_control
    oa: OverrideActions = fleet_p.ships[fleet_p.flag_ship].override_actions
    oa.interaction(fleet_p, fleet_e, chances, packed_ep)
