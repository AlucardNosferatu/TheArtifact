import os
import pickle
import random
import uuid

from artifacts import Artifact, Specs
from avionics import *
from designs import Engine, Warhead, Locomotive, Avionics, Weapon, Chassis, Part, Design
from map import Base, MapEvent
from production import Pipeline, read_pipeline_from_xls


class Building:
    health_point = 0
    slot = 0
    level = 0
    type_str = ''
    stat = ''
    base = None

    def tomorrow(self, map_events: list[MapEvent], r_queue: list[list]):
        return map_events, r_queue

    def __init__(self, hp, slot, lv, ts, stat, b_ptr: Base):
        self.level = lv
        self.health_point = hp
        self.slot = slot
        self.type_str = ts
        self.stat = stat
        self.base = b_ptr


class CommandCenter(Building):
    map_event_detected = []
    radar_radius = 0
    rwr_radius = 0
    radar_radius_dict = {
        1: 250,
        2: 500,
        3: 750,
        4: 1000
    }
    rwr_radius_ratio = {
        1: 2,
        2: 1.5,
        3: 1,
        4: 0.5
    }
    continuous = None

    def __init__(self, slot, b_ptr: Base):
        super().__init__(2000, slot, 1, 'command_center', 'normal', b_ptr)
        self.radar_radius = CommandCenter.radar_radius_dict[self.level]
        self.rwr_radius = CommandCenter.rwr_radius_ratio[self.level] * self.radar_radius
        self.continuous = False

    def scan_events(self, global_events: list[MapEvent], r_queue):
        r_queue = self.clear_scanned(r_queue)
        for event in global_events:
            if event.get_distance(self.base.coordinate) < self.radar_radius:
                self.map_event_detected.append(event)
                r_task = ['load_new', event.get_icon_id(), MapEvent.icon_path[event.event_type], event.get_screen_pos()]
                r_queue.append(r_task)
        return r_queue

    def clear_scanned(self, r_queue):
        for event in self.map_event_detected:
            event: MapEvent
            r_task = ['delete_old', event.get_icon_id(), None, None]
            r_queue.append(r_task)
        self.map_event_detected.clear()
        return r_queue

    def toggle_continuous_scan(self):
        if self.continuous:
            if self in self.base.time_passed_tasks:
                self.base.time_passed_tasks.remove(self)
            self.continuous = False
            if self in self.base.radiation_src:
                self.base.radiation_src.remove(self)
            print('连续扫描已关闭')
        else:
            if self not in self.base.time_passed_tasks:
                self.base.time_passed_tasks.append(self)
            self.continuous = True
            if self not in self.base.radiation_src:
                self.base.radiation_src.append(self)
            print('连续扫描已启动')

    def deploy_task_force(self):
        pass

    def tomorrow(self, map_events, r_queue):
        r_queue = self.scan_events(global_events=map_events, r_queue=r_queue)
        return map_events, r_queue


class Laboratory(Building):
    part_class_dict = {
        'chs': Chassis,
        'eng': Engine,
        'wpn': Weapon,
        'whd': Warhead,
        'loc': Locomotive,
        'avi': Avionics
    }
    basic_component = {
        'chs': ['wood'],
        'eng': ['steel'],
        'wpn': ['barrel'],
        'whd': ['gun_p', 'steel'],
        'loc': ['wood'],
        'avi': ['e-device']
    }
    experience_modifier = 0.0
    avi_function = [miner_drone, radar_scan, jammer, irst_scan]
    parts_names = {
        'chs': '载具骨架',
        'eng': '引擎',
        'wpn': '发射器',
        'whd': '弹头',
        'loc': '机动部件',
        'avi': '电子设备'
    }
    current_work: list[None | list[Part | int]] = None
    research_speed = {
        1: 5760,
        2: 4320,
        3: 2880,
        4: 1440
    }

    def __init__(self, slot, b_ptr: Base):
        super().__init__(2000, slot, 1, 'laboratory', 'normal', b_ptr)
        self.experience_modifier = 1.0
        self.current_work = [None, None, None]

    def research_new_part(self, part_type):
        if None not in self.current_work:
            print('实验室正忙！请等待当前工作完成！')
            return

        def gen_size(pt):
            if pt == 'chs':
                sz = -1
            else:
                # sz = random.choice([0, 1, 2])
                sz = 0
            return sz

        def gen_hp(sz, pt):
            if sz == 0:
                health = random.randint(10, 100)
            elif sz == 1:
                health = random.randint(50, 140)
            elif sz == 2:
                health = random.randint(90, 180)
            else:
                health = random.randint(130, 220)
            if pt == 'whd':
                health = round(health / 2)
            return health

        def gen_bc(sz, pt):
            build_cost = {}
            for res in Laboratory.basic_component[pt]:
                if sz == 0:
                    build_cost.__setitem__(res, random.randint(10, 30))
                elif sz == 1:
                    build_cost.__setitem__(res, random.randint(20, 40))
                elif sz == 2:
                    build_cost.__setitem__(res, random.randint(30, 50))
                else:
                    build_cost.__setitem__(res, random.randint(40, 60))
            return build_cost

        def gen_ep(sz, pt, base_ptr: Base):
            extra_params = []
            if pt == 'chs':
                slots_count = {}
                for pt2 in Laboratory.part_class_dict:
                    if pt2 not in ['chs', 'whd']:
                        slots_count.__setitem__(
                            pt2,
                            [
                                random.randint(1, 2),
                                random.randint(0, 0),
                                random.randint(0, 0)
                            ]
                        )
                extra_params.append(slots_count)
                extra_params.append(min(random.random() + 0.5, 1))
            elif pt == 'wpn':
                e_range = random.randint(50, 100)
                acc = random.randint(50, 150 - e_range)
                rof = random.randint(50, 200 - acc - e_range)
                if sz == 0:
                    # small wpn
                    e_range = max(25, e_range - 20)
                    acc = min(100, acc + 10)
                    rof = min(100, rof + 10)
                elif sz == 2:
                    # large wpn
                    e_range = min(125, e_range + 20)
                    acc = max(50, acc - 10)
                    rof = max(50, rof - 10)
                extra_params.append(rof)
                extra_params.append(acc)
                extra_params.append(e_range)
            elif pt == 'whd':
                damage = random.randint(50, 75)
                spd = random.randint(50, 150 - damage)
                ang_spd = random.randint(50, 200 - spd - damage)
                if sz == 0:
                    # small whd
                    damage = max(50, damage - 20)
                    spd = min(75, spd + 10)
                    ang_spd = min(100, ang_spd + 10)
                elif sz == 2:
                    # large whd
                    damage = min(125, damage + 20)
                    spd = max(75, spd - 10)
                    ang_spd = max(25, ang_spd - 10)
                dt = random.choice(['normal', 'AP', 'napalm', 'shock', 'toxic', 'corrosive', 'HE', 'radioactive'])
                extra_params.append(damage)
                extra_params.append(dt)
                extra_params.append(spd)
                extra_params.append(ang_spd)
            elif pt == 'avi':
                if base_ptr.is_able_to_build_miner:
                    func1 = random.choice(Laboratory.avi_function)
                else:
                    func1 = Laboratory.avi_function[0]
                    base_ptr.is_able_to_build_miner = True
                func2 = random.choice([None, func1])
                if func2 is not None:
                    while func2 == func1:
                        func2 = random.choice(Laboratory.avi_function)
                extra_params.append(func1)
                extra_params.append(func2)
            elif pt == 'loc':
                m = random.randint(10, 30) + 10 * sz
                d = m + random.randint(-5, 5) + 10 * sz
                extra_params.append(m)
                extra_params.append(d)
            elif pt == 'eng':
                mt = random.randint(10, 30) + 10 * sz
                fc = mt + random.randint(-5, 5) + 10 * sz
                extra_params.append(mt)
                extra_params.append(fc)
            else:
                print('零件种类代号错误！额外参数设为None')
                extra_params = None
            return extra_params

        size = gen_size(part_type)
        hp = gen_hp(size, part_type)
        bc = gen_bc(size, part_type)

        if part_type in ['chs', 'wpn', 'whd', 'avi', 'loc', 'eng']:
            ep = gen_ep(size, part_type, self.base)
            new_part = Laboratory.part_class_dict[part_type](hp=hp, bc=bc, size=size, extra_params=ep)
        else:
            new_part = Laboratory.part_class_dict[part_type](hp=hp, bc=bc, size=size)

        work_slot_index = self.current_work.index(None)
        self.current_work[work_slot_index] = [new_part, Laboratory.research_speed[self.level]]
        if self not in self.base.time_passed_tasks:
            self.base.time_passed_tasks.append(self)

    def dispose_old_part(self, part_type, part_index):
        self.base.unlocked_parts[part_type].pop(part_index)

    def terminate_ongoing_res(self, work_index):
        if 0 <= work_index < len(self.current_work):
            if self.current_work[work_index] is None:
                print('这个研究室没有正在进行的研究')
            else:
                self.current_work[work_index] = None
                print('已中止第', work_index, '实验室的研究')
        else:
            print('参数错误！')

    def compose_new_design(self):
        if len(self.base.unlocked_parts['chs']) <= 0:
            print('必须有至少一款载具骨架才能设计！')
            return
        name: None | str = None
        while name is None:
            name = input('设计命名（或输入ABORT中止设计）：')
            if name == 'ABORT':
                return
            elif name in self.base.designs:
                print('同名设计已存在！')
                name = None

        chs_selected_index = 0
        while True:
            print('第一阶段：选择', self.parts_names['chs'])
            chs_selected = self.base.unlocked_parts['chs'][chs_selected_index]
            attrs = [item for item in dir(chs_selected) if not item.startswith('__')]
            for attr in attrs:
                attr_val = getattr(chs_selected, attr)
                if not hasattr(attr_val, '__call__'):
                    print(attr, attr_val)
            print()
            print('当前款号：', chs_selected_index)
            choice = input('0.上一款 1.下一款 2.选中 3.中止设计')
            if choice == '0':
                chs_selected_index -= 1
                chs_selected_index += len(self.base.unlocked_parts['chs'])
                chs_selected_index %= len(self.base.unlocked_parts['chs'])
            elif choice == '1':
                chs_selected_index += 1
                chs_selected_index += len(self.base.unlocked_parts['chs'])
                chs_selected_index %= len(self.base.unlocked_parts['chs'])
            elif choice == '2':
                break
            elif choice == '3':
                return
            else:
                print('无效输入！')
                continue

        new_design = Design(name=name, chassis=chs_selected)
        for pt in new_design.slots:
            for i in range(3):
                # small medium large
                for j in range(len(new_design.slots[pt][i])):
                    # multiple slots with same size
                    pt_selected_index = 0
                    pt_selected: Part | None = None
                    while len(self.base.unlocked_parts[pt]) > 0:
                        print('第二阶段：选择', self.parts_names[pt], '插槽尺寸：', i)
                        pt_selected = self.base.unlocked_parts[pt][pt_selected_index]
                        attrs = [item for item in dir(pt_selected) if not item.startswith('__')]
                        for attr in attrs:
                            attr_val = getattr(pt_selected, attr)
                            if not hasattr(attr_val, '__call__'):
                                print(attr, attr_val)
                        print()
                        print('当前款号：', pt_selected_index)
                        choice = input('0.上一款 1.下一款 2.选中 3.留空（油箱） 4.中止设计')
                        if choice == '0':
                            pt_selected_index -= 1
                            pt_selected_index += len(self.base.unlocked_parts[pt])
                            pt_selected_index %= len(self.base.unlocked_parts[pt])
                        elif choice == '1':
                            pt_selected_index += 1
                            pt_selected_index += len(self.base.unlocked_parts[pt])
                            pt_selected_index %= len(self.base.unlocked_parts[pt])
                        elif choice == '2':
                            if pt_selected.size != i:
                                print('插槽大小不匹配！请重新选择！')
                                continue
                            else:
                                break
                        elif choice == '3':
                            pt_selected = None
                            break
                        elif choice == '4':
                            return
                        else:
                            print('无效输入！')
                            continue
                    new_design.slots[pt][i][j] = pt_selected
        print(new_design.name, '设计完成！')
        self.base.designs.__setitem__(new_design.name, new_design)

    def delete_old_design(self, design_name):
        if design_name in self.base.designs:
            del self.base.designs[design_name]
        else:
            print('没有这个名称的设计！')

    def part_not_in(self, part, part_type):
        for part_index, loaded_part in enumerate(self.base.unlocked_parts[part_type]):
            same_part = True
            attrs = [item for item in dir(loaded_part) if not item.startswith('__')]
            for attr in attrs:
                attr_val = getattr(loaded_part, attr)
                if not hasattr(attr_val, '__call__'):
                    if attr_val != getattr(part, attr):
                        same_part = False
                        break
            if same_part:
                return part_index
        return -1

    def replace_part_obj(self, name, pt, size, p_index, loaded_p_index):
        if pt == 'chs':
            self.base.designs[name].chassis_in_use = self.base.unlocked_parts[pt][loaded_p_index]
        else:
            self.base.designs[name].slots[pt][size][p_index] = self.base.unlocked_parts[pt][loaded_p_index]

    def load_design_from_file(self, bin_filepath):
        if os.path.exists(bin_filepath):
            with open(bin_filepath, 'rb') as f:
                design = pickle.load(f)
                if design.name in self.base.designs:
                    print('已有重名设计，覆盖？')
                    load_com = input('0.覆盖 1.重命名新设计')
                    if load_com == '1':
                        new_name = input('输入新名称')
                        design.name = new_name
                self.base.designs.__setitem__(design.name, design)
                same_part_index = self.part_not_in(design.chassis_in_use, 'chs')
                if same_part_index == -1:
                    self.base.unlocked_parts['chs'].append(design.chassis_in_use)
                else:
                    self.replace_part_obj(design.name, 'chs', -1, 0, same_part_index)
                for part_type in design.slots:
                    for size in range(3):
                        for p_index, part in enumerate(design.slots[part_type][size]):
                            if part is not None:
                                same_part_index = self.part_not_in(part, part_type)
                                if same_part_index == -1:
                                    self.base.unlocked_parts[part_type].append(part)
                                else:
                                    self.replace_part_obj(design.name, part_type, size, p_index, same_part_index)
        else:
            print('文件', bin_filepath, '不存在！')

    def save_design_to_file(self, design_name):
        if design_name in self.base.designs:
            with open(design_name + '.bin', 'wb') as f:
                pickle.dump(self.base.designs[design_name], f)
        else:
            print('没有这个名称的设计！')

    def tomorrow(self, map_events, r_queue):
        finished = []
        unfinished: list
        for index, unfinished in enumerate(self.current_work):
            if unfinished is not None:
                unfinished[1] -= 1
                if unfinished[1] <= 0:
                    finished.append(index)
                    new_part: Part = unfinished[0]
                    part_type = new_part.type_str
                    self.base.unlocked_parts[part_type].append(new_part)
                    print('你获得了新', Laboratory.parts_names[part_type], '！属性如下：')
                    attrs = [item for item in dir(new_part) if not item.startswith('__')]
                    for attr in attrs:
                        attr_val = getattr(new_part, attr)
                        if not hasattr(attr_val, '__call__'):
                            print(attr, attr_val)
        for fin in finished:
            self.current_work[fin] = None
        return map_events, r_queue


class Factory(Building):
    pipeline: None | Pipeline = None
    pipeline_set = None
    design_set = None
    pt_passed = None
    quality_modifier = None
    qm_lower_bound = 0.5
    bc_per_artifact = None
    need_to_produce = None
    level_modifier = {1: 1, 2: 0.75, 3: 0.5, 4: 0.25}
    min_per_product = None
    countdown = 0

    def __init__(self, slot, b_ptr: Base):
        super().__init__(1000, slot, 1, 'factory', 'normal', b_ptr)
        self.countdown = 0
        self.min_per_product = None
        self.need_to_produce = 0
        self.pipeline = None
        self.pipeline_set = False
        self.design_set = False
        self.pt_passed = False
        self.quality_modifier = 0

    def set_pipeline_from_file(self, filename):
        self.need_to_produce = 0
        self.pipeline = read_pipeline_from_xls(filename)
        used_area = self.pipeline.pipeline_area()
        if used_area == 0:
            self.pipeline_set = False
            self.design_set = False
            self.pt_passed = False
            self.quality_modifier = 0
            print('未检测到任何流水线模块！请重新设计流水线并导入！')
        else:
            self.pipeline_set = True
            self.design_set = False
            self.pt_passed = False
            self.quality_modifier = 0
            print('流水线已导入，占地面积：', used_area)

    def set_design_from_base(self, design_name):
        if self.pipeline_set:
            if design_name in self.base.designs:
                self.need_to_produce = 0
                design = self.base.designs[design_name]
                resource_types = []
                part_type_count = 0
                self.pipeline.set_requirement(design)
                self.bc_per_artifact = {}
                for part_id in self.pipeline.req:
                    part_type_count += 1
                    for res_type in self.pipeline.req[part_id][0]:
                        res_per_pt = self.pipeline.req[part_id][0][res_type] * self.pipeline.req[part_id][1]
                        if res_type not in self.bc_per_artifact:
                            self.bc_per_artifact.__setitem__(
                                res_type,
                                res_per_pt
                            )
                        else:
                            self.bc_per_artifact.__setitem__(
                                res_type,
                                self.bc_per_artifact[res_type] + res_per_pt
                            )
                        if res_type not in resource_types:
                            resource_types.append(res_type)
                resource_type_count = len(resource_types)
                std_area = (part_type_count + resource_type_count) * 10
                used_area = self.pipeline.pipeline_area()
                assert used_area != 0
                diff_area = 2 * std_area - used_area
                self.pipeline_set = True
                self.design_set = True
                self.pt_passed = False
                self.quality_modifier = max(Factory.qm_lower_bound, diff_area / std_area)

                print('设计"', design_name, '"已导入流水线，产线复杂度：', self.quality_modifier)
            else:
                print('找不到名为', design_name, '的设计！')
        else:
            print('流水线未导入！')

    def production_test(self):
        if self.pipeline_set and self.design_set:
            self.need_to_produce = 0
            self.min_per_product = round(Factory.level_modifier[self.level] * self.pipeline.performance_test())
            self.pt_passed = True
            print('生产测试已通过，单位产品生产耗时（分钟）：', self.min_per_product)

        else:
            self.pt_passed = False
            print('流水线未导入或载具设计未指定！')

    def produce(self, extra_amount):
        if self.pipeline_set and self.design_set and self.pt_passed:
            if extra_amount > 0:
                planned_amount = self.need_to_produce + extra_amount
                for res_type in self.bc_per_artifact:
                    if planned_amount * self.bc_per_artifact[res_type] > self.base.warehouse_basic[res_type]:
                        print(res_type, '不足！')
                        return
                for res_type in self.bc_per_artifact:
                    self.base.consume_resource(res_type, self.bc_per_artifact[res_type] * extra_amount)
                self.need_to_produce += extra_amount
                if self not in self.base.time_passed_tasks:
                    self.base.time_passed_tasks.append(self)
            else:
                print('负的新生产计划将清空目前的生产计划，已经消耗的资源将不会归还，继续？')
                if input('0.继续 1.取消') == '0':
                    self.need_to_produce = 0
        else:
            print('产线不可用，可能原因：')
            print('1.产线规划未设置 2.产品设计未导入 3.流程测试未通过')

    def able_to_produce_one_more(self):
        able = False
        if self.need_to_produce > 0:
            if len(self.base.hangar_basic) < self.base.hangar_cap:
                if self.countdown >= self.min_per_product:
                    self.countdown = 0
                    able = True
                    print('产生一件新产品！')
                else:
                    self.countdown += 1
                    print('生产进行中')
            else:
                print('机库空间不足！')
        else:
            print('计划产量为0')
        return able

    def design2artifact(self):
        # region basic params
        def health_weight_and_fuel(design: Design):
            fuel_cap = 0
            health = design.chassis_in_use.health_points
            weight_modifier = design.chassis_in_use.bare_weight_modifier
            bare_weight = 0
            for part_type in design.slots:
                for size in range(3):
                    for part in design.slots[part_type][size]:
                        if part is not None:
                            health += part.health_points
                            bare_weight += (size + 1) * 10
                        else:
                            fuel_cap += (size + 1) * 10
            bare_weight *= weight_modifier
            return health, bare_weight, fuel_cap

        def thrust_and_consumption(design: Design):
            thrust = 0
            consumption = 0
            for size in range(3):
                for part in design.slots['eng'][size]:
                    if part is not None:
                        part: Engine
                        thrust += part.max_thrust
                        consumption += part.fuel_consumption
            return thrust, consumption

        def maneuver_and_drag(design: Design):
            maneuver = 0
            drag = 0
            for size in range(3):
                for part in design.slots['loc'][size]:
                    if part is not None:
                        part: Locomotive
                        maneuver += part.maneuverability
                        drag += part.drag
            return maneuver, drag

        def sp_function(design: Design):
            funcs = []
            extra_fuel_cap = 0
            # use redundant slot for same function as extra energy source
            for size in range(3):
                for part in design.slots['avi'][size]:
                    if part is not None:
                        part: Avionics
                        if part.main_function not in funcs:
                            funcs.append(part.main_function)
                        else:
                            extra_fuel_cap += (size * 10)
                        if part.sub_function is not None:
                            if part.sub_function not in funcs:
                                funcs.append(part.sub_function)
                            else:
                                extra_fuel_cap += (size * 10)
            return funcs, extra_fuel_cap

        # endregion

        # region quality_modifier
        spf, efc = sp_function(self.pipeline.design)
        hp, bw, fc = health_weight_and_fuel(self.pipeline.design)
        hp *= self.quality_modifier
        bw *= (2 - self.quality_modifier)
        fc += efc
        fc *= self.quality_modifier
        t, c = thrust_and_consumption(self.pipeline.design)
        t *= self.quality_modifier
        c *= (2 - self.quality_modifier)
        m, d = maneuver_and_drag(self.pipeline.design)
        m *= self.quality_modifier
        d *= (2 - self.quality_modifier)

        # endregion

        params = {
            'health_points': hp,
            'bare_weight': bw,
            'fuel_capacity': fc,
            'thrust': t,
            'consumption': c,
            'maneuver': m,
            'drag': d,
            'special_functions': spf
        }
        spc = Specs(params=params)
        art = Artifact(this_specs=spc)
        return art

    def tomorrow(self, map_events, r_queue):
        if self.able_to_produce_one_more():
            art = self.design2artifact()
            self.base.hangar_basic.append(art)
            self.need_to_produce -= 1
        return map_events, r_queue


class ConstructionCrane(Building):
    progress_record = {}
    cost_dict = {
        'command_center': {'wood': 10, 'time': 1440},
        'laboratory': {'wood': 10, 'time': 1440},
        'factory': {'wood': 10, 'time': 1440}
    }
    class_dict = {
        'command_center': CommandCenter,
        'laboratory': Laboratory,
        'factory': Factory
    }

    def __init__(self, slot, base_inst):
        super().__init__(2000, slot, 1, 'construction_crane', 'normal', base_inst)
        self.progress_record = {}

    def query_cost(self, building_type):
        print(ConstructionCrane.cost_dict[building_type])
        print()
        print(self.base.warehouse_basic)

    def build_new(self, slot, building_type):
        if building_type not in ConstructionCrane.class_dict:
            print('不可建造或建筑类型代码错误！')
        else:
            if 0 <= slot < len(self.base.buildings):
                if self.base.buildings[slot] is not None:
                    print('这个位置有建筑了！')
                else:
                    for res in ConstructionCrane.cost_dict[building_type]:
                        if res != 'time':
                            if ConstructionCrane.cost_dict[building_type][res] > self.base.warehouse_basic[res]:
                                print('资源不足，无法建造！')
                                return
                    for res in ConstructionCrane.cost_dict[building_type]:
                        if res != 'time':
                            self.base.consume_resource(res, ConstructionCrane.cost_dict[building_type][res])
                    new_b_id = str(uuid.uuid4())
                    self.base.buildings[slot] = new_b_id
                    self.progress_record.__setitem__(
                        new_b_id,
                        [
                            building_type,
                            ConstructionCrane.cost_dict[building_type]['time']
                        ]
                    )
                    if self not in self.base.time_passed_tasks:
                        self.base.time_passed_tasks.append(self)
            else:
                print('基地里没有空地可供建造新建筑')

    def remove_old(self, slot):
        if 0 <= slot < len(self.base.buildings):
            if self.base.buildings[slot] is None:
                print('这个位置没有建筑！')
            else:
                removed_building: Building | None | str = self.base.buildings[slot]
                if removed_building is self:
                    print('塔吊不能拆除自己！')
                else:
                    if type(removed_building) is str:
                        building_type = self.progress_record[removed_building][0]
                        del self.progress_record[removed_building]
                    else:
                        building_type = removed_building.type_str
                        if removed_building in self.base.time_passed_tasks:
                            self.base.time_passed_tasks.remove(removed_building)
                    for res in ConstructionCrane.cost_dict[building_type]:
                        if res != 'time':
                            self.base.add_resource(res, ConstructionCrane.cost_dict[building_type][res])
                    self.base.buildings[slot] = None
                    del removed_building
        else:
            print('空地编号超出有效范围！')

    def tomorrow(self, map_events, r_queue):
        finished = []
        for unfinished in self.progress_record:
            unf_building = self.progress_record[unfinished]
            unf_building[1] -= 1
            if unf_building[1] <= 0:
                building_type = unf_building[0]
                slot = self.base.buildings.index(unfinished)
                self.base.buildings[slot] = ConstructionCrane.class_dict[building_type](
                    slot=slot,
                    b_ptr=self.base
                )
                finished.append(unfinished)
                print('新的', building_type, '在空地', slot, '完工了！')
        for fin in finished:
            del self.progress_record[fin]
        return map_events, r_queue


if __name__ == '__main__':
    slot_c = {'eng': [9, 0, 0]}
    chs = Chassis(hp=100, bc={'wood': 10}, size=-1, extra_params=[slot_c, 1.0])
    des = Design('test', chs)
    eng = Engine(10, {'wood': 10, 'steel': 10}, 0, [10, 10])
    des.slots['eng'][0][0] = eng
    des.slots['eng'][0][1] = eng
    with open('Save/test_art.bin', 'wb') as df:
        pickle.dump(des, df)
    print('Done')
