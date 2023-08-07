from Buffs.OverrideBuffs import WeaponOverload, RedistributedPower, ShieldOverload, PinpointShield, EngineOverload, \
    HighGManeuver, CantEscape, FastEscape, EnhancedCircuit, DamageControl


def overload_weapon(acting_ship):
    wo = WeaponOverload(acting_ship)
    acting_ship.buff_list.append(wo)
    wo.trigger()
    return True


def redistribute_firepower(acting_ship):
    w_count = len(acting_ship.weapons)
    opts = [str(option + 1) for option in list(range(w_count + 1))]
    cmd = ''
    while cmd not in opts:
        print('Select 1 weapon to redistribute its firepower.')
        [
            print(
                '{}.Power:{} Targets:{}'.format(
                    opt, acting_ship.weapons[int(opt) - 1].power, acting_ship.weapons[int(opt) - 1].target
                )
            ) for opt in opts if int(opt) - 1 < w_count
        ]
        print('{}.Back'.format(opts[-1]))
        cmd = input()
    if cmd == opts[-1]:
        return False
    else:
        weapon_index = int(cmd) - 1
        opts = [str(option) for option in list(range(1, 101))]
        cmd = ''
        while cmd not in opts:
            print('Input a new targets count, range from 1 to 100, input -1 to return:')
            cmd = input()
            if cmd == '-1':
                return False
        new_targets = int(cmd)
        rp = RedistributedPower(acting_ship, new_targets=new_targets, weapon_index=weapon_index)
        acting_ship.buff_list.append(rp)
        rp.trigger()
        return True


# ShieldOverload()
# PinpointShield()
# EngineOverload()
# HighGManeuver()
# CantEscape()
# FastEscape()
# EnhancedCircuit()
# DamageControl()
