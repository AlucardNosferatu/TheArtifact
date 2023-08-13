import random

import Battle.BattlePlan
from Battle.BattleEvent import BattleEvent
from Plots.Area88 import NewMercenary, Defection, LeavedMercenary, Volunteers
from Plots.MainPlot import UnlockOverride
from Utils import Nothing

# todo: Event should be refactored as an object!!! see ya next version.
# noinspection PyTypeChecker
global_pools_dict = {
    'default': {
        'events': [NewMercenary] * 4 + [Defection] + [Nothing] * 4 + [UnlockOverride],
        'stealth': {
            NewMercenary: 20,
        },
        'add_flags': {
            NewMercenary: [],
            Defection: ['encounter_rebel'],
            Nothing: [],
            UnlockOverride: []
        },
        'del_flags': {
            NewMercenary: [],
            Defection: ['annihilate_rebel'],
            Nothing: [],
            UnlockOverride: []
        },
        'pool_triggers': {
            'Area88': {'include': ['encounter_rebel'], 'exclude': ['annihilate_rebel']}
        }
    },
    'Area88': {
        'events': [BattleEvent] + [NewMercenary] * 2 + [LeavedMercenary] * 2 + [Volunteers] * 2 + [Nothing] * 3,
        'stealth': {
            BattleEvent: 10,
            NewMercenary: 20
        },
        'add_flags': {
            BattleEvent: ['annihilate_rebel'],
            NewMercenary: [],
            LeavedMercenary: [],
            Volunteers: [],
            Nothing: []
        },
        'del_flags': {
            BattleEvent: [],
            NewMercenary: [],
            LeavedMercenary: [],
            Volunteers: [],
            Nothing: []
        },
        'pool_triggers': {
            'default': {'include': ['annihilate_rebel'], 'exclude': []}
        }
    },
}


def event_process(game_obj, event, specified_fleet=None):
    # select an event in current event_pool
    # event = random.choice(game_obj.events_pool['events'])
    # the code above will be used in update_map
    # execute that event
    if specified_fleet is None:
        game_obj.fleet, change_score = event(game_obj.fleet)
    else:
        _, change_score = event(specified_fleet)
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
    if type(event) in add_flags.keys():
        for flag in add_flags[type(event)]:
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
    if type(event) in del_flags.keys():
        for flag in del_flags[type(event)]:
            if flag == '%ALL%':
                Battle.BattlePlan.clear()
                break
            elif flag in game_obj.flags:
                game_obj.flags.remove(flag)
