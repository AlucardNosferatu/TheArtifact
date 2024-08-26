from Mechanism.Agent import Agent
from Mechanism.Entity import Entity


class Event:
    def __init__(self, radius, trigger_ent_type: list, trigger_function, world, priority=1):
        self.att_ent = None
        self.radius = radius
        self.trigger_ent_type: list = trigger_ent_type
        self.trigger_function = trigger_function
        self.world = world
        self.priority = priority
        self.status = 'idle'
        # ['idle', 'triggered']

    def is_triggered(self, trigger_ent, triggered_ent: None | Entity = None, distance=None):
        if triggered_ent is None:
            triggered_ent = self.att_ent
        if distance is None:
            try:
                distance = Entity.distance_between(ent1=triggered_ent, ent2=trigger_ent)
            except Exception as e:
                print(repr(e))
                return False
        if distance <= self.radius:
            ent_id = trigger_ent.ent_id
            ent_type_name = Agent.dec_ent_id(ent_id=ent_id)['type_name']
            if ent_type_name in self.trigger_ent_type:
                return True
        return False

    def triggered(self, trigger_ent, triggered_ent=None):
        if triggered_ent is None:
            triggered_ent = self.att_ent
        self.trigger_function(trigger_ent=trigger_ent, triggered_ent=triggered_ent, world=self.world)
        if self.status == 'idle':
            self.status = 'triggered'
