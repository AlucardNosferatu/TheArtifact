import random


def battle_end(offensive, defensive):
    # todo
    return False


def battle_result(offensive, defensive):
    # todo
    return {
        'conclude': 'draw',
        'offensive': [],
        'defensive': []
    }


def battle_rounds(offensive, defensive):
    print('战斗开始！')
    flag = True
    offensive.confront = defensive
    defensive.confront = offensive
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
    offensive.confront = None
    defensive.confront = None
    result = battle_result(offensive, defensive)
    return result
