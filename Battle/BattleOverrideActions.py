from Buffs.OverrideBuffs import WeaponOverload, RedistributedPower, ShieldOverload, PinpointShield, EngineOverload, \
    HighGManeuver, CantEscape, FastEscape, EnhancedCircuit, DamageControl


def overload_weapon(fleet_a, fleet_b, acting_ship):
    _, _ = fleet_a, fleet_b
    wo = WeaponOverload(acting_ship)
    acting_ship.buff_list.append(wo)
    wo.trigger()
    return True


def redistribute_firepower(fleet_a, fleet_b, acting_ship):
    _, _ = fleet_a, fleet_b
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


def overload_shield(fleet_a, fleet_b, acting_ship):
    _, _ = fleet_a, fleet_b
    so = ShieldOverload(acting_ship)
    acting_ship.buff_list.append(so)
    so.trigger()


def pinpoint_shield(fleet_a, fleet_b, acting_ship):
    _, _ = fleet_a, fleet_b
    ps = PinpointShield(acting_ship)
    acting_ship.buff_list.append(ps)
    ps.trigger()


def overload_engine(fleet_a, fleet_b, acting_ship):
    _, _ = fleet_a, fleet_b
    eo = EngineOverload(acting_ship)
    acting_ship.buff_list.append(eo)
    eo.trigger()


def high_g_maneuver(fleet_a, fleet_b, acting_ship):
    _, _ = fleet_a, fleet_b
    hgm = HighGManeuver(acting_ship)
    acting_ship.buff_list.append(hgm)
    hgm.trigger()


def prevent_escape(fleet_a, fleet_b, acting_ship):
    _, _ = fleet_a, acting_ship
    for ship_uid in fleet_b.ships.keys():
        target_ship = fleet_b.ships[ship_uid]
        ce = CantEscape(target_ship)
        target_ship.buff_list.append(ce)
        ce.trigger()


def boost_escape(fleet_a, fleet_b, acting_ship):
    _, _ = fleet_a, fleet_b
    fe = FastEscape(acting_ship)
    acting_ship.buff_list.append(fe)
    fe.trigger()


def enhance_circuit(fleet_a, fleet_b, acting_ship):
    _, _ = fleet_a, fleet_b
    ec = EnhancedCircuit(acting_ship)
    acting_ship.buff_list.append(ec)
    ec.trigger()


def control_damage(fleet_a, fleet_b, acting_ship):
    _, _ = fleet_a, fleet_b
    dc = DamageControl(acting_ship)
    acting_ship.buff_list.append(dc)
    dc.trigger()
