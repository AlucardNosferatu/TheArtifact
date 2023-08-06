from Battle.BattleEvent import battle_event
from Plots.Area88 import new_mercenary, leaved_mercenary, volunteers, defection
from Utils import nothing

events_pool_default = [new_mercenary, leaved_mercenary, nothing]
events_chains = {
    '0#Area 88': {'condition': ['a88'], 'events_pool': [battle_event, leaved_mercenary, volunteers, defection]}
}
add_flags = {new_mercenary: ['a88']}
del_flags = {leaved_mercenary: ['a88']}
