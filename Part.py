import uuid


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


class Building(Part):
    def __init__(self, type_str):
        super().__init__(size='huge', type_str=type_str, mass=10000, hp=10000)


class Room(Part):
    def __init__(self, type_str):
        super().__init__(size='large', type_str=type_str, mass=1000, hp=1000)


class Equipment(Part):
    def __init__(self, type_str):
        super().__init__(size='medium', type_str=type_str, mass=100, hp=100)


class Device(Part):
    def __init__(self, type_str):
        super().__init__(size='small', type_str=type_str, mass=10, hp=10)


def embark(steer_part, target):
    parasite_v = steer_part.v_ptr
    if parasite_v.size in ['medium', 'small']:
        if target.size in parasite_v.can_para:
            if parasite_v.para_target is None:
                if abs(parasite_v.tactic_pos - target.tactic_pos) <= parasite_v.thrust:
                    if parasite_v not in target.para_in:
                        target.para_in.append(parasite_v)
                    parasite_v.para_target = target
                    parasite_v.tactic_pos = target.tactic_pos
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
    return True
