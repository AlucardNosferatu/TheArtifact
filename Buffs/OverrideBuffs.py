from Classes.Buff import Buff


class WeaponOverload(Buff):
    def __init__(self, effect_target):
        super().__init__(1, effect_target, WeaponOverload.t_func, WeaponOverload.r_func)

    @staticmethod
    def t_func(target, params: dict):
        if hasattr(target, 'free_overload') and target.free_overload:
            print('{} has enhanced circuit that can endure energy overload!'.format(target.name))
            params['activated'] = True
        else:
            cost = max(1, int(0.2 * target.max_hit_points))
            if target.hit_points - cost <= 0:
                print('HP of {} is too low, cannot overload!'.format(target.name))
                params['activated'] = False
            else:
                target.hit_points -= cost
                print('{} overloaded its weapons! but its hull was damaged by overloaded energy circuit!'.format(
                    target.name))
                params['activated'] = True
        if params['activated']:
            amounts = []
            for weapon in target.weapons:
                amount = max(1, int(0.2 * weapon.power))
                amounts.append(amount)
                p = weapon.power
                weapon.power += amount
                print('Weapon Power:{}->{}'.format(p, weapon.power))
            params['amounts'] = amounts

    @staticmethod
    def r_func(target, params: dict):
        if params['activated']:
            for i in range(min(len(params['amounts']), len(target.weapons))):
                p = target.weapons[i].power
                target.weapons[i].power -= params['amounts'][i]
                print('Weapon Power:{}->{}'.format(p, target.weapons[i].power))


class RedistributedPower(Buff):
    def __init__(self, effect_target, new_targets, weapon_index):
        super().__init__(1, effect_target, RedistributedPower.t_func, RedistributedPower.r_func,
                         {'new_targets': new_targets, 'weapon_index': weapon_index})

    @staticmethod
    def t_func(target, params: dict):
        weapon_index = params['weapon_index']
        weapon = target.weapons[weapon_index]
        params['old_targets'] = weapon.target
        params['old_power'] = weapon.power
        new_power = round(params['old_power'] * params['old_targets'] / params['new_targets'])
        weapon.target = params['new_targets']
        weapon.power = new_power

    @staticmethod
    def r_func(target, params: dict):
        weapon_index = params['weapon_index']
        weapon = target.weapons[weapon_index]
        weapon.target = params['old_targets']
        weapon.power = params['old_power']


class ShieldOverload(Buff):
    def __init__(self, effect_target):
        super().__init__(1, effect_target, ShieldOverload.t_func, ShieldOverload.r_func)

    @staticmethod
    def t_func(target, params: dict):
        if hasattr(target, 'free_overload') and target.free_overload:
            print('{} has enhanced circuit that can endure energy overload!'.format(target.name))
            params['activated'] = True
        else:
            cost = max(1, int(0.2 * target.max_hit_points))
            if target.hit_points - cost <= 0:
                print('HP of {} is too low, cannot overload!'.format(target.name))
                params['activated'] = False
            else:
                target.hit_points -= cost
                print('{} overloaded its shield! but its hull was damaged by overloaded energy circuit!'.format(
                    target.name))
                params['activated'] = True
        if params['activated']:
            amount = max(1, 0.2 * target.armor)
            a = target.armor
            target.armor += amount
            print('Ship Armor:{}->{}'.format(a, target.armor))
            params['amount'] = amount

    @staticmethod
    def r_func(target, params: dict):
        if params['activated']:
            a = target.armor
            target.armor -= params['amount']
            print('Ship Armor:{}->{}'.format(a, target.armor))


class PinpointShield(Buff):
    def __init__(self, effect_target):
        super().__init__(1, effect_target, PinpointShield.t_func, PinpointShield.r_func,
                         {'new_damaged': self.damaged})

    @staticmethod
    def t_func(target, params: dict):
        if target.hit_points < 0.5 * target.max_hit_points:
            print('Pinpoint-Shield of {} cannot be triggered when its HP  is below 50%!'.format(target.name))
            params['activated'] = False
        else:
            print('Pinpoint-Shield of {} was triggered!'.format(target.name))
            params['activated'] = True
        if params['activated']:
            params['old_damaged'] = target.damaged
            target.damaged = params['new_damaged']

    @staticmethod
    def r_func(target, params: dict):
        if params['activated']:
            target.damaged = params['old_damaged']

    def damaged(self, amount):
        print('Pinpoint-Shield is working!')
        if self.effect_target.hit_points <= 0.5 * self.effect_target.max_hit_points:
            print('HP below 50%: double shield!')
            amount -= (self.effect_target.armor * 2)
        else:
            print('HP above 50%: half shield.')
            amount -= (self.effect_target.armor / 2)
        if amount < 0:
            amount = 0
        self.effect_target.hit_points -= amount
        if self.effect_target.hit_points < 0:
            self.effect_target.hit_points = 0


class EngineOverload(Buff):
    def __init__(self, effect_target):
        super().__init__(1, effect_target, EngineOverload.t_func, EngineOverload.r_func)

    @staticmethod
    def t_func(target, params: dict):
        if hasattr(target, 'free_overload') and target.free_overload:
            print('{} has enhanced circuit that can endure energy overload!'.format(target.name))
            params['activated'] = True
        else:
            cost = max(1, int(0.2 * target.max_hit_points))
            if target.hit_points - cost <= 0:
                print('HP of {} is too low, cannot overload!'.format(target.name))
                params['activated'] = False
            else:
                target.hit_points -= cost
                print('{} overloaded its engine! but its hull was damaged by overloaded energy circuit!'.format(
                    target.name))
                params['activated'] = True
        if params['activated']:
            amount = max(1, int(1.2 * target.max_speed - target.speed))
            s = target.speed
            target.change_speed(amount=amount, allow_exceed=True)
            print('Ship Speed:{}->{}'.format(s, target.speed))
            params['amount'] = amount

    @staticmethod
    def r_func(target, params: dict):
        if params['activated']:
            s = target.speed
            target.change_speed(amount=-params['amount'])
            print('Ship Speed:{}->{}'.format(s, target.speed))


class HighGManeuver(Buff):
    def __init__(self, effect_target):
        super().__init__(1, effect_target, HighGManeuver.t_func, HighGManeuver.r_func)

    @staticmethod
    def t_func(target, params: dict):
        cost = max(1, int(0.2 * target.speed))
        amount = max(1, 0.2 * target.maneuver)
        if target.speed - cost <= 0:
            print('Speed of {} is too low, cannot brake!'.format(target.name))
            params['activated'] = False
        else:
            print('{} activated the air-brake while doing a sharp turn!'.format(target.name))
            params['old_speed'] = target.speed
            params['speed_cost'] = cost
            params['old_maneuver'] = target.maneuver
            target.change_speed(amount=-cost)
            target.maneuver += amount
            print('Ship Speed:{}->{}'.format(params['old_speed'], target.speed))
            print('Ship Maneuver:{}->{}'.format(params['old_maneuver'], target.maneuver))
            params['activated'] = True

    @staticmethod
    def r_func(target, params: dict):
        if params['activated']:
            print('{} recovered from the PSM (post-stall maneuver).'.format(target.name))
            print('Ship Speed:{}->{}'.format(target.speed, params['old_speed']))
            print('Ship Maneuver:{}->{}'.format(target.maneuver, params['old_maneuver']))
            target.change_speed(amount=params['speed_cost'])
            target.maneuver = params['old_maneuver']


class CantEscape(Buff):
    def __init__(self, effect_target):
        super().__init__(1, effect_target, CantEscape.t_func, CantEscape.r_func)

    @staticmethod
    def t_func(target, params: dict):
        params['prev_state'] = target.escapable
        target.escapable = 1

    @staticmethod
    def r_func(target, params: dict):
        target.escapable = params['prev_state']


class FastEscape(Buff):
    def __init__(self, effect_target):
        super().__init__(1, effect_target, FastEscape.t_func, FastEscape.r_func)

    @staticmethod
    def t_func(target, params: dict):
        params['prev_state'] = target.escapable
        target.escapable = 2

    @staticmethod
    def r_func(target, params: dict):
        target.escapable = params['prev_state']


class EnhancedCircuit(Buff):
    def __init__(self, effect_target):
        super().__init__(1, effect_target, EnhancedCircuit.t_func, EnhancedCircuit.r_func)

    @staticmethod
    def t_func(target, params: dict):
        _ = params
        setattr(target, 'free_overload', True)

    @staticmethod
    def r_func(target, params: dict):
        _ = params
        delattr(target, 'free_overload')


class DamageControl(Buff):
    def __init__(self, effect_target):
        super().__init__(1, effect_target, DamageControl.t_func, DamageControl.r_func,
                         {'new_damaged': self.damaged, 'this_buff': self})

    @staticmethod
    def t_func(target, params: dict):
        already_triggered = False
        for buff in target.buff_list:
            if buff is not params['this_buff']:
                if type(buff) is DamageControl:
                    if buff.triggered:
                        already_triggered = True
                        break
        if already_triggered:
            print('Damage Control can only be triggered once per round!'.format(target.name))
            params['activated'] = False
        else:
            print('Damage Control of {} was triggered! It can prevent {} from destroyed once in this round.'.format(
                target.name, target.name))
            params['activated'] = True
        if params['activated']:
            params['old_damaged'] = target.damaged
            target.damaged = params['new_damaged']

    @staticmethod
    def r_func(target, params: dict):
        if params['activated']:
            target.damaged = params['old_damaged']

    def damaged(self, amount):
        amount -= self.effect_target.armor
        if amount < 0:
            amount = 0
        self.effect_target.hit_points -= amount
        if self.effect_target.hit_points < 0:
            self.effect_target.hit_points = 0
        if self.effect_target.hit_points <= 0:
            amount = max(1, int(self.effect_target.max_hit_points * 0.2))
            self.effect_target.hit_points += amount
            print('Damage Control is working! {} recovered {} HP!'.format(self.effect_target.name, amount))
            self.effect_target.damaged = self.memorized_params['old_damaged']
            print('Damage Control was used, it cannot be used again in this round anymore!')


if __name__ == '__main__':
    pass
