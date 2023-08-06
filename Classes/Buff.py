class Buff:
    effect_target = None
    trigger_function = None
    restore_function = None
    decay_count = None
    memorized_params = None
    triggered = None
    expired = None

    def __init__(self, trigger_count, effect_target, trigger_function, restore_function, memorized_params=None):
        self.decay_count = trigger_count
        self.effect_target = effect_target
        self.trigger_function = trigger_function
        self.restore_function = restore_function
        if memorized_params is None:
            self.memorized_params = {}
        else:
            self.memorized_params = memorized_params
        self.triggered = False
        self.expired = False

    def trigger(self):
        assert not self.expired
        assert not self.triggered
        self.trigger_function(self.effect_target, self.memorized_params)
        self.triggered = True

    def decay(self):
        assert not self.expired
        assert self.triggered
        if self.decay_count > 1:
            self.decay_count -= 1
        else:
            self.restore_function(self.effect_target, self.memorized_params)
            self.expired = True
            print('Buff:', str(self), 'Expired!')
