import random


def battle_end(offensive, defensive):
    # todo
    return False


def battle_result(offensive, defensive):
    offensive.confront = None
    defensive.confront = None
    for unit in offensive.units:
        unit.tactic_pos = 0
        unit.tactic_ang = 0
    for unit in defensive.units:
        unit.tactic_pos = 0
        unit.tactic_ang = 0
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
        unit.tactic_ang = 180
    for unit in defensive.units:
        unit.tactic_pos = dist
        unit.tactic_ang = 0
    return offensive, defensive


def round_start(task_force):
    changed = []
    for unit in task_force.units:
        # todo:kill units without essential parts
        unit.acted = False
        if len(unit.para_in) > 0:
            has_hostile_para = False
            controlled = False
            for para in unit.para_in:
                if para.belonged != unit.belonged:
                    has_hostile_para = True
                    if not controlled:
                        print('由于跳帮入侵，载具', unit, '的控制权正在丧失！')
                    unit.para_cd += 1
                    if unit.para_cd >= unit.para_to:
                        if not controlled:
                            print('载具', unit, '被跳帮单位控制！')
                        controlled = True
                        if unit not in changed:
                            changed.append(unit)
                else:
                    if unit.para_cd > 0:
                        print('由于驻军支援，载具', unit, '的控制权正在夺回！')
                    unit.para_cd -= 1

                    if unit.para_cd < 0:
                        unit.para_cd = 0
            if not has_hostile_para:
                unit.para_cd = 0
            elif not controlled:
                print(
                    '载具',
                    unit,
                    '损失的控制权',
                    str(round(100 * unit.para_cd / unit.para_to)) + '%'
                )
        else:
            unit.para_cd = 0
    for unit in changed:
        unit.para_cd = 0
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
            unit.use_part(random.randint(0, len(unit.p_list) - 1), True)
        else:
            print('玩家行动：')
            unit_acted = True
            u_index = ''
            while unit_acted:
                battle_awareness(task_force)
                print('输入接收命令的载具编号：')
                u_index = input()
                unit_acted = task_force.units[int(u_index)].acted
                if unit_acted:
                    print('这个载具本回合已经行动过了')
            print(task_force.units[int(u_index)].p_list)
            p_index = input()
            if p_index == '':
                print('这个载具本回合待机')
                task_force.units[int(u_index)].acted = True
            else:
                task_force.units[int(u_index)].use_part(int(p_index))
    return task_force


def battle_awareness(task_force):
    print('打击群单位：')
    size = [unit.size for unit in task_force.units]
    print(size)
    dist = [unit.tactic_pos for unit in task_force.units]
    print('所处位置：')
    print(dist)
    print('敌对方单位：')
    size = [unit.size for unit in task_force.confront.units]
    print(size)
    dist = [unit.tactic_pos for unit in task_force.confront.units]
    print('所处位置：')
    print(dist)


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
