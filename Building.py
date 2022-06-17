from Part import *
from MapEvent import *


class Crane(Building):
    def __init__(self):
        super().__init__('crane')
        self.function_list.append(self.build_new)
        self.params_list.append(['slot_index', 'build_type'])
        self.function_list.append(self.remove_old)
        self.params_list.append(['slot_index'])

    def build_new(self, params):
        slot_index = params[0]
        build_type = params[1]
        print(self)

    def remove_old(self, params):
        slot_index = params[0]
        print(self)


class Lab(Building):
    def __init__(self):
        super().__init__('lab')

    def research_part(self):
        pass


class Factory(Building):
    pass


class Command(Building):
    task_force_cap = None
    tf_ptr: None | list[None | TaskForce] = None

    def __init__(self):
        super().__init__('command')
        self.function_list.append(self.create_task_force)
        self.params_list.append(['unit_ap_indices'])
        self.function_list.append(self.retire_task_force)
        self.params_list.append(['tf_index'])
        self.task_force_cap = 3
        self.tf_ptr = []
        for i in range(self.task_force_cap):
            self.tf_ptr.append(None)

    def create_task_force(self, params):
        unit_ap_indices = params[0]
        if None in self.tf_ptr:
            tf_index = self.tf_ptr.index(None)
            x = self.v_ptr.coordinate['x']
            y = self.v_ptr.coordinate['y']
            units = []
            for u_index in unit_ap_indices:
                if 0 <= u_index < self.v_ptr.ap_cap:
                    if self.v_ptr.ap_basic[u_index] is not None:
                        units.append(self.v_ptr.ap_basic[u_index])
                    else:
                        return
                else:
                    return
            self.tf_ptr[tf_index] = TaskForce(x, y)
            for unit in units:
                unit.belonged = self.tf_ptr[tf_index]
                self.tf_ptr[tf_index].add_unit(unit)
                ap_index = self.v_ptr.ap_basic.index(unit)
                self.v_ptr.ap_basic[ap_index] = None
        else:
            return

    def retire_task_force(self, params):
        tf_index = params[0]
        if self.tf_ptr[tf_index] is not None:
            if self.tf_ptr[tf_index].dist_to_me(self.v_ptr) < 2:
                if self.v_ptr.ap_basic.count(None) >= len(self.tf_ptr[tf_index].units):
                    for unit in self.tf_ptr[tf_index].units:
                        unit.belonged = None
                        index = self.v_ptr.ap_basic.index(None)
                        self.v_ptr.ap_basic[index] = unit
                    self.tf_ptr[tf_index] = None
                else:
                    return
            else:
                return
        else:
            return

    def order_task_force(self, params):
        tf_index = params[0]
        print(self)


class Warehouse(Building):
    pass


class Airport(Building):
    pass
