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
        return True

    def remove_old(self, params):
        slot_index = params[0]
        print(self)
        return True


class Lab(Building):
    def __init__(self):
        super().__init__('lab')

    def research_part(self, params):
        print(self)
        return True


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
                        print('打击群至少要有一台载具。')
                        return False
                else:
                    print('输入的载具所在停机坪编号错误。')
                    return False
            self.tf_ptr[tf_index] = TaskForce(x, y)
            for unit in units:
                unit.belonged = self.tf_ptr[tf_index]
                self.tf_ptr[tf_index].add_unit(unit)
                ap_index = self.v_ptr.ap_basic.index(unit)
                self.v_ptr.ap_basic[ap_index] = None
            print('新的打击群已建立。')
            return True
        else:
            print('已达到该指挥中心可指挥打击群数量上限，无法建立新的打击群。')
            return False

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
                    print('打击群编制撤销完毕，载具已放入停机坪。')
                    return True
                else:
                    print('空闲停机坪数量不足以存放打击群内的全部载具，编制撤销失败。')
                    return False
            else:
                print('打击群与所属指挥部太远，请命令打击群返回至浮空城（距离小于2）再撤销其编制。')
                return False
        else:
            print('指挥部没有对应输入编号的打击群。')
            return False

    def order_task_force(self, params):
        tf_index = params[0]
        print(self)
        return True


class Warehouse(Building):
    pass


class Airport(Building):
    pass
