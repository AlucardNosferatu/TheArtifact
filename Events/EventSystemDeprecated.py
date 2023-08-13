from Battle.BattleEvent import battle_event
from Plots.Area88 import NewMercenary, leaved_mercenary, volunteers, defection
from Utils import nothing

events_pool_default = [NewMercenary, leaved_mercenary, nothing]
events_chains = {
    '0#Area 88': {'condition': ['a88'], 'events_pool': [battle_event, leaved_mercenary, volunteers, defection]}
}
add_flags = {NewMercenary: ['a88']}
del_flags = {leaved_mercenary: ['a88']}
