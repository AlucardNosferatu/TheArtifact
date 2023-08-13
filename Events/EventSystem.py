import random

import Battle.BattlePlan
from Battle.BattleEvent import battle_event
from Plots.Area88 import new_mercenary, leaved_mercenary, volunteers, defection
from Plots.MainPlot import unlock_override
from Utils import nothing

global_pools_dict = {
    'default': {
        'events': [new_mercenary] * 4 + [defection] + [nothing] * 4 + [unlock_override],
        'add_flags': {
            new_mercenary: [],
            defection: ['encounter_rebel'],
            nothing: [],
            unlock_override: []
        },
        'del_flags': {
            new_mercenary: [],
            defection: ['annihilate_rebel'],
            nothing: [],
            unlock_override: []
        },
        'pool_triggers': {
            'Area88': {'include': ['encounter_rebel'], 'exclude': ['annihilate_rebel']}
        }
    },
    'Area88': {
        'events': [battle_event] + [new_mercenary] * 2 + [leaved_mercenary] + [volunteers] * 3 + [nothing] * 3,
        'add_flags': {
            battle_event: ['annihilate_rebel'],
            new_mercenary: [],
            leaved_mercenary: [],
            volunteers: [],
            nothing: []
        },
        'del_flags': {
            battle_event: [],
            new_mercenary: [],
            leaved_mercenary: [],
            volunteers: [],
            nothing: []
        },
        'pool_triggers': {
            'default': {'include': ['annihilate_rebel'], 'exclude': []}
        }
    },
}


def event_process(game_obj, event):
    # select an event in current event_pool
    # event = random.choice(game_obj.events_pool['events'])
    # the code above will be used in update_map
    # execute that event
    game_obj.fleet, change_score = event(game_obj.fleet)
    # update flags by pool_flags
    update_score_and_flags(change_score, event, game_obj)
    # check pools jumper with flags
    triggered_pools = gather_triggered_pools(game_obj)
    if len(triggered_pools) > 0:
        next_pool = random.choice(triggered_pools)
        print('Event pool is switching to:', next_pool)
        new_events_pool = global_pools_dict[next_pool]
        game_obj.events_pool = new_events_pool


def gather_triggered_pools(game_obj):
    pool_triggers = game_obj.events_pool['pool_triggers']
    triggered_pools = []
    for next_pool in pool_triggers.keys():
        excluded = False
        for exclude_flag in pool_triggers[next_pool]['exclude']:
            if exclude_flag in game_obj.flags:
                excluded = True
                break
        if not excluded:
            included = True
            for include_flag in pool_triggers[next_pool]['include']:
                if include_flag not in game_obj.flags:
                    included = False
                    break
            if included:
                triggered_pools.append(next_pool)
    return triggered_pools


def update_score_and_flags(change_score, event, game_obj):
    game_obj.score += change_score
    add_flags = game_obj.events_pool['add_flags']
    del_flags = game_obj.events_pool['del_flags']
    if event in add_flags.keys():
        for flag in add_flags[event]:
            if type(flag) is str:
                if flag not in game_obj.flags:
                    game_obj.flags.append(flag)
            elif type(flag) is list:
                flag_list = set(flag)
                common_flags = flag_list.intersection(set(game_obj.flags))
                flag_list = list(flag_list.difference(common_flags))
                if len(flag_list) > 0:
                    flag = random.choice(flag_list)
                    game_obj.flags.append(flag)
            else:
                raise TypeError('flag should be str or list[str]!')
    if event in del_flags.keys():
        for flag in del_flags[event]:
            if flag == '%ALL%':
                Battle.BattlePlan.clear()
                break
            elif flag in game_obj.flags:
                game_obj.flags.remove(flag)
