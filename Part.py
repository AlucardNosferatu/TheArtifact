import uuid

from MapEvent import TaskForce


class Part:
    # 部件所属载机对象指针，用于数据交互
    v_ptr = None
    size = None
    # 组件类型名称，一类一个
    type_str: None | str = None
    # 组件对象名称，一个实例一个
    uid_str: None | str = None
    # 容器或连接器
    # 容器允许该组件挂载一个小于载机尺寸级别的载具，con='cont'
    # 连接器允许该组件挂载一个与载机同尺寸级别的载具，con='conn'
    # 既不是容器也不是连接器，con=None
    con: None | str = None
    con_target = None
    # 组件重量
    mass: None | float = None
    hp = None

    # 以列表的形式列出该组件特有功能统一传入载具对象
    function_list = None
    params_list = None

    def set_v_ptr(self, vessel_ptr):
        self.v_ptr = vessel_ptr

    def __init__(self, size, hp, mass, type_str):
        self.size = size
        self.type_str = type_str
        self.hp = hp
        self.mass = mass
        self.uid_str = str(uuid.uuid4())
        self.function_list = []
        self.params_list = []

    def destroyed(self):
        index = self.v_ptr.p_list.index(self)
        self.v_ptr.uninstall_part(index)

    def on_install(self):
        pass

    def on_uninstall(self):
        pass


building_params = {'size': 'huge', 'mass': 10000, 'hp': 10000}
room_params = {'size': 'large', 'mass': 1000, 'hp': 1000}
equipment_params = {'size': 'medium', 'mass': 100, 'hp': 100}
device_params = {'size': 'small', 'mass': 10, 'hp': 10}


def embark(steer_part, target):
    parasite_v = steer_part.v_ptr
    if parasite_v is not target:
        if parasite_v.size in ['medium', 'small']:
            if target.size in parasite_v.can_para:
                if parasite_v.para_target is None:
                    if abs(parasite_v.tactic_pos - target.tactic_pos) <= parasite_v.thrust:
                        if parasite_v not in target.para_in:
                            target.para_in.append(parasite_v)
                        parasite_v.para_target = target
                        parasite_v.tactic_pos = target.tactic_pos
                        if target.belonged == parasite_v.belonged:
                            print('驻扎成功！正在守卫！')
                        else:
                            print('跳帮成功！正在占领！')
                        return True
                    else:
                        print('距离太远！接近后才能跳帮！')
                else:
                    print('已经跳帮了其它载具！请先脱离当前跳帮的载具！')
            else:
                print('目标尺寸太小！')
        else:
            print('跳帮作战仅限中小型载具可用')
    else:
        print('无法对自机进行跳帮！（？？？）')
    return False


def disembark(steer_part):
    parasite_v = steer_part.v_ptr
    if parasite_v.size in ['medium', 'small']:
        if parasite_v.para_target is not None:
            target = parasite_v.para_target
            if parasite_v in target.para_in:
                target.para_in.remove(parasite_v)
            parasite_v.para_target = None
            print('跳帮作战中止，载具已撤离')
            return True
        else:
            print('该载具没有跳帮到其它载具上')
    else:
        print('跳帮作战仅限中小型载具可用')
    return False


def move_to_tac_pos(thrust_part, dst_tac_pos):
    vessel = thrust_part.v_ptr
    if vessel.para_target is None:
        if abs(dst_tac_pos - vessel.tactic_pos) <= vessel.thrust:
            vessel.tactic_pos = dst_tac_pos
        else:
            if dst_tac_pos > vessel.tactic_pos:
                vessel.tactic_pos += vessel.thrust
            else:
                vessel.tactic_pos -= vessel.thrust
        for para_unit in vessel.para_in:
            para_unit.tactic_pos = vessel.tactic_pos
        print('移动到了：', vessel.tactic_pos)
        return True
    else:
        print('跳帮中无法自由移动！')
        return False


def attack(weapon, target, part_index):
    # todo:filter parasite unit
    attacker = weapon.v_ptr
    if hasattr(weapon, 'anti_embark'):
        if target.para_target == attacker:
            # todo:damage process
            return True
        else:
            print('内部防卫武器无法用于攻击外部目标！')
            return False
    else:
        if target.para_target == attacker.para_target:
            # todo:damage process
            return True
        else:
            print('攻击者和目标不同处战场或相同载具中（跳帮）！')
            return False


# Buildings
class Crane(Part):
    def __init__(self):
        s = building_params['size']
        m = building_params['mass']
        h = building_params['hp']
        super().__init__(type_str='crane', size=s, mass=m, hp=h)
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


class Command(Part):
    task_force_cap = None
    tf_ptr: None | list[None | TaskForce] = None

    def __init__(self):
        s = building_params['size']
        m = building_params['mass']
        h = building_params['hp']
        super().__init__(type_str='command', size=s, mass=m, hp=h)
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
            x = self.v_ptr.guard_force.coordinate['x']
            y = self.v_ptr.guard_force.coordinate['y']
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


# Rooms
class LiftEngine(Part):
    lift = None

    def __init__(self, lift):
        s = room_params['size']
        m = room_params['mass']
        h = room_params['hp']
        super().__init__(type_str='lift_engine', size=s, mass=m, hp=h)
        self.lift = lift


class Propulsion(Part):
    thrust = None

    def __init__(self, thrust):
        s = room_params['size']
        m = room_params['mass']
        h = room_params['hp']
        super().__init__(type_str='propulsion', size=s, mass=m, hp=h)
        self.thrust = thrust
        self.function_list.append(self.move_to_tac_pos)
        self.params_list.append(['dst_tac_pos'])

    def move_to_tac_pos(self, params):
        dst_tac_pos = params[0]
        return move_to_tac_pos(self, dst_tac_pos)


class SentryGun(Part):
    anti_embark = None

    def __init__(self):
        s = room_params['size']
        m = room_params['mass']
        h = room_params['hp']
        super().__init__(type_str='sentry_gun', size=s, mass=m, hp=h)
        self.anti_embark = True
        self.function_list.append(self.attack)
        self.params_list.append(['target_index', 'p_index'])

    def attack(self, params):
        target_index = params[0]
        p_index = params[1]
        target = self.v_ptr.belonged.confront.units[target_index]
        return attack(self, target, p_index)


# Equipments
class Wing(Part):
    lift = None

    def __init__(self, lift):
        s = equipment_params['size']
        m = equipment_params['mass']
        h = equipment_params['hp']
        super().__init__(type_str='wing', size=s, mass=m, hp=h)
        self.lift = lift


class Thruster(Part):
    thrust = None

    def __init__(self, thrust):
        s = equipment_params['size']
        m = equipment_params['mass']
        h = equipment_params['hp']
        super().__init__(type_str='thruster', size=s, mass=m, hp=h)
        self.thrust = thrust
        self.function_list.append(self.move_to_tac_pos)
        self.params_list.append(['dst_tac_pos'])

    def move_to_tac_pos(self, params):
        dst_tac_pos = params[0]
        return move_to_tac_pos(self, dst_tac_pos)


class CtrlSurface(Part):
    yaw_spd = None

    def __init__(self, yaw_spd):
        s = equipment_params['size']
        m = equipment_params['mass']
        h = equipment_params['hp']
        super().__init__(type_str='ctrl_surface', size=s, mass=m, hp=h)
        self.yaw_spd = yaw_spd
        self.function_list.append(self.embark)
        self.params_list.append(['target_index', 'belonged'])
        self.function_list.append(self.disembark)
        self.params_list.append([])

    def embark(self, params):
        target_index = params[0]
        target_belonged = params[1]
        if target_belonged == 0:
            target = self.v_ptr.belonged.confront.units[target_index]
        else:
            target = self.v_ptr.belonged.units[target_index]
        return embark(self, target)

    # noinspection PyUnusedLocal
    def disembark(self, params):
        return disembark(self)


class Drill(Part):
    def __init__(self):
        s = equipment_params['size']
        m = equipment_params['mass']
        h = equipment_params['hp']
        super().__init__(type_str='drill', size=s, mass=m, hp=h)
        self.function_list.append(self.attack)
        self.params_list.append(['target_index'])

    def attack(self, params):
        target_index = params[0]
        part_index = params[1]
        target = self.v_ptr.belonged.confront.units[target_index]
        return attack(self, target, part_index)


class TransformHinge(Part):
    def __init__(self):
        s = equipment_params['size']
        m = equipment_params['mass']
        h = equipment_params['hp']
        super().__init__(type_str='trans_hinge', size=s, mass=m, hp=h)

    def on_install(self):
        self.v_ptr.can_para.append('large')

    def on_uninstall(self):
        self.v_ptr.can_para.remove('large')


class SalvageMagnet(Part):
    def __init__(self):
        s = equipment_params['size']
        m = equipment_params['mass']
        h = equipment_params['hp']
        super().__init__(type_str='salvage_magnet', size=s, mass=m, hp=h)

    def on_install(self):
        self.v_ptr.can_para.append('large')
        self.v_ptr.can_para.append('medium')

    def on_uninstall(self):
        self.v_ptr.can_para.remove('large')
        self.v_ptr.can_para.remove('medium')


# Devices
class Stabilizer(Part):
    def __init__(self):
        s = device_params['size']
        m = device_params['mass']
        h = device_params['hp']
        super().__init__(type_str='stabilizer', size=s, mass=m, hp=h)


class Accelerator(Part):
    thrust = None

    def __init__(self, thrust):
        s = device_params['size']
        m = device_params['mass']
        h = device_params['hp']
        super().__init__(type_str='accelerator', size=s, mass=m, hp=h)
        self.thrust = thrust
        self.function_list.append(self.move_to_tac_pos)
        self.params_list.append(['dst_tac_pos'])

    def move_to_tac_pos(self, params):
        dst_tac_pos = params[0]
        return move_to_tac_pos(self, dst_tac_pos)


class Elevator(Part):
    lift = None

    def __init__(self, lift):
        s = device_params['size']
        m = device_params['mass']
        h = device_params['hp']
        super().__init__(type_str='elevator', size=s, mass=m, hp=h)
        self.lift = lift


class SteerMotor(Part):
    yaw_spd = None

    def __init__(self, yaw_spd):
        s = device_params['size']
        m = device_params['mass']
        h = device_params['hp']
        super().__init__(type_str='steer_motor', size=s, mass=m, hp=h)
        self.yaw_spd = yaw_spd
        self.function_list.append(self.embark)
        self.params_list.append(['target_index', 'belonged'])
        self.function_list.append(self.disembark)
        self.params_list.append([])

    def embark(self, params):
        vessel = self.v_ptr
        for part in vessel.p_list:
            if type(part) is Stabilizer:
                target_index = params[0]
                target_belonged = params[1]
                if target_belonged == 0:
                    target = self.v_ptr.belonged.confront.units[target_index]
                else:
                    target = self.v_ptr.belonged.units[target_index]
                return embark(self, target)
        print('没有悬停稳定装置，无法进行跳帮作业！')
        return False

    # noinspection PyUnusedLocal
    def disembark(self, params):
        return disembark(self)


class Harpoon(Part):
    def __init__(self):
        s = device_params['size']
        m = device_params['mass']
        h = device_params['hp']
        super().__init__(type_str='harpoon', size=s, mass=m, hp=h)

    def on_install(self):
        self.v_ptr.can_para.append('medium')

    def on_uninstall(self):
        self.v_ptr.can_para.remove('medium')


class HackerInterface(Part):
    def __init__(self):
        s = device_params['size']
        m = device_params['mass']
        h = device_params['hp']
        super().__init__(type_str='hacker_interface', size=s, mass=m, hp=h)

    def on_install(self):
        self.v_ptr.can_para.append('medium')
        self.v_ptr.can_para.append('small')

    def on_uninstall(self):
        self.v_ptr.can_para.remove('medium')
        self.v_ptr.can_para.remove('small')
