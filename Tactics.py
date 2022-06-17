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


def battle_rounds(offensive, defensive):
    print('战斗开始！')
    flag = True
    offensive, defensive = battle_init(offensive, defensive)
    while flag:
        while not offensive.acted():
            print('进攻方回合：')
            if offensive.ai_controlled:
                print('AI行动中：')
                unit = random.choice(offensive.units)
                unit.select_part(random.randint(0, len(unit.p_list) - 1), True)
            else:
                print('玩家行动：')
                u_index = input()
                p_index = input()
                offensive.units[int(u_index)].select_part(p_index)
        while not defensive.acted():
            print('防守方回合：')
            if defensive.ai_controlled:
                print('AI行动中：')
                unit = random.choice(defensive.units)
                unit.select_part(random.randint(0, len(unit.p_list) - 1), True)
            else:
                print('玩家行动：')
                u_index = input()
                p_index = input()
                defensive.units[int(u_index)].select_part(p_index)
        if battle_end(offensive, defensive):
            flag = False
    offensive, defensive, result = battle_result(offensive, defensive)
    return result
