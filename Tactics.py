import random


def battle_end(offensive, defensive):
    # todo
    return False


def battle_result(offensive, defensive):
    offensive.confront = None
    defensive.confront = None
    for unit in offensive.units:
        unit.tactic_pos = 0
    for unit in defensive.units:
        unit.tactic_pos = 0
    result = {
        'conclude': 'draw',
        'offensive': [],
        'defensive': []
    }
    return offensive, defensive, result


def battle_init(offensive, defensive):
    dist = offensive.dist_to_me(defensive)
    offensive.confront = defensive
    defensive.confront = offensive
    for unit in offensive.units:
        unit.tactic_pos = 0
    for unit in defensive.units:
        unit.tactic_pos = dist
    return offensive, defensive


def round_start(task_force):
    changed = []
    for unit in task_force.units:
        # todo:kill units without essential parts
        unit.acted = False
        if len(unit.para_in) > 0:
            has_hostile_para = False
            for para in unit.para_in:
                if para.belonged != unit.belonged:
                    has_hostile_para = True
                    unit.para_cd += 1
                    if unit.para_cd >= unit.para_to:
                        unit.para_cd = 0
                        changed.append(unit)
                else:
                    unit.para_cd -= 1
                    if unit.para_cd < 0:
                        unit.para_cd = 0
            if not has_hostile_para:
                unit.para_cd = 0
        else:
            unit.para_cd = 0
    for unit in changed:
        task_force.remove_unit(unit, False)
        task_force.confront.add_unit(unit)
        unit.belonged = task_force.confront


def task_force_action(task_force, tf_side):
    round_start(task_force)
    while not task_force.acted():
        print(tf_side, '回合：')
        if task_force.ai_controlled:
            print('AI行动中：')
            unit = random.choice(task_force.units)
            unit.select_part(random.randint(0, len(unit.p_list) - 1), True)
        else:
            print('玩家行动：')
            unit_acted = True
            u_index = ''
            while unit_acted:
                print(task_force.units)
                u_index = input()
                unit_acted = task_force.units[int(u_index)].acted
                if unit_acted:
                    print('这个载具本回合已经行动过了')
            print(task_force.units[int(u_index)].p_list)
            p_index = input()
            task_force.units[int(u_index)].select_part(int(p_index))
    return task_force


def battle_rounds(offensive, defensive):
    print('战斗开始！')
    flag = True
    offensive, defensive = battle_init(offensive, defensive)
    while flag:
        offensive = task_force_action(offensive, '进攻方')
        defensive = task_force_action(defensive, '防守方')
        if battle_end(offensive, defensive):
            flag = False
    offensive, defensive, result = battle_result(offensive, defensive)
    return result
