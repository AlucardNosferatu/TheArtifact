def event_1(fleet):
    print('This is event 1')
    return fleet, 1


def event_2(fleet):
    print('This is event 2')
    return fleet, 10


def event_3(fleet):
    print('This is event 3')
    return fleet, 100


def event_4(fleet):
    print('This is event 4')
    return fleet, 1000


def event_5(fleet):
    print('This is event 5')
    return fleet, 10000


def event_6(fleet):
    print('This is event 6')
    return fleet, 100000


global_pools_dict = {
    'default': {
        'events': [event_1, event_2],
        'add_flags': {
            event_1: ['flag1', ['flag1', 'flag21', 'flag22']],
            event_2: ['flag2', ['flag2', 'flag23', 'flag24']]
        },
        'del_flags': {
            event_1: ['%ALL%'],
            event_2: ['%ALL%']
        },
        'pool_triggers': {
            'pool_1': {'include': ['flag1', 'flag2'], 'exclude': ['flag3', 'flag4']}
        }
    },
    'pool_1': {
        'events': [event_3, event_4],
        'add_flags': {
            event_3: ['flag5', 'flag6', 'flag11', 'flag12', 'flag15', 'flag16'],
            event_4: ['flag9', 'flag10', 'flag7', 'flag8', 'flag19', 'flag20']
        },
        'del_flags': {
            event_3: ['flag7', 'flag8', 'flag19', 'flag20'],
            event_4: ['flag11', 'flag12', 'flag15', 'flag16']
            # prevent pool_2 from returning to default
        },
        'pool_triggers': {
            'default': {'include': ['flag5', 'flag6'], 'exclude': ['flag7', 'flag8']},
            'pool_2': {'include': ['flag9', 'flag10'], 'exclude': ['flag11', 'flag12']}
        }
    },
    'pool_2': {
        'events': [event_5, event_6],
        'add_flags': {
            event_5: ['flag13', 'flag14'],
            event_6: ['flag17', 'flag18']
        },
        'del_flags': {
            event_5: ['flag19', 'flag20'],
            event_6: ['flag15', 'flag16']
            # can only return to default after event_6
        },
        'pool_triggers': {
            'default': {'include': ['flag13', 'flag14'], 'exclude': ['flag15', 'flag16']},
            'pool_1': {'include': ['flag17', 'flag18'], 'exclude': ['flag19', 'flag20']}
        }
    }
}
