from Part import *
from MapEvent import *


class Crane(Building):
    def __init__(self):
        super().__init__('crane')
        self.function_list.append(self.build_new)
        self.function_list.append(self.remove_old)

    def build_new(self):
        pass

    def remove_old(self):
        pass


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
        self.function_list.append(self.retire_task_force)
        self.task_force_cap = 3
        self.tf_ptr = []
        for i in range(self.task_force_cap):
            self.tf_ptr.append(None)

    def create_task_force(self, unit_ap_indices):
        if None in self.tf_ptr:
            index = self.tf_ptr.index(None)
            x = self.v_ptr.coordinate['x']
            y = self.v_ptr.coordinate['y']
            units = []
            for index in unit_ap_indices:
                if 0 <= index < len(self.v_ptr.ap_cap):
                    if self.v_ptr.ap_basic[index] is not None:
                        units.append(self.v_ptr.ap_basic[index])
                    else:
                        return
                return
            self.tf_ptr[index] = TaskForce(x, y)
            for unit in units:
                self.tf_ptr[index].add_unit(unit)
                index = self.v_ptr.ap_basic.index(unit)
                self.v_ptr.ap_basic[index] = None
        else:
            return

    def retire_task_force(self, tf_index):
        if self.tf_ptr[tf_index] is not None:
            if self.tf_ptr[tf_index].dist_to_me(self.v_ptr) < 2:
                if self.v_ptr.ap_basic.count(None) >= len(self.tf_ptr[tf_index].units):
                    for unit in self.tf_ptr[tf_index].units:
                        index = self.v_ptr.ap_basic.index(None)
                        self.v_ptr.ap_basic[index] = unit
                    self.tf_ptr[tf_index] = None
                else:
                    return
            else:
                return
        else:
            return

    def order_task_force(self, tf_index):
        pass


class Warehouse(Building):
    pass


class Airport(Building):
    pass
