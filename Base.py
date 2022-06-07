import random
import uuid

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
    base_ptr = None

    def __init__(self, hp, slot, lv, ts, stat, b_ptr: Base):
        self.level = lv
        self.health_point = hp
        self.slot = slot
        self.type_str = ts
        self.stat = stat
        self.base_ptr = b_ptr


class CommandCenter(Building):
    map_event_detected = []
    radar_radius = 0

    def __init__(self, slot, b_ptr: Base):
        super().__init__(2000, slot, 1, 'command_center', 'normal', b_ptr)
        self.radar_radius = 750

    def scan_events(self, global_events: list[MapEvent]):
        self.map_event_detected.clear()
        for event in global_events:
            if event.get_distance(self.base_ptr.coordinate) < self.radar_radius:
                self.map_event_detected.append(event)

    def deploy_task_force(self):
        raise NotImplementedError('未授予部队指挥权！')


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
        'loc': ['wood', 'ti'],
        'avi': ['e-device']
    }
    experience_modifier = 0.0
    avi_function = [radar_scan, jammer, irst_scan]
    parts_names = {
        'chs': '载具骨架',
        'eng': '引擎',
        'wpn': '发射器',
        'whd': '弹头',
        'loc': '机动部件',
        'avi': '电子设备'
    }
    current_work: list[None | list[Part | int]] = None
    need_days = 0

    def __init__(self, slot, b_ptr: Base):
        super().__init__(2000, slot, 1, 'laboratory', 'normal', b_ptr)
        self.experience_modifier = 1.0
        self.current_work = [None, None, None]
        self.need_days = 7

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

        def gen_ep(sz, pt):
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
                func1 = random.choice(Laboratory.avi_function)
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
            ep = gen_ep(size, part_type)
            new_part = Laboratory.part_class_dict[part_type](hp=hp, bc=bc, size=size, extra_params=ep)
        else:
            new_part = Laboratory.part_class_dict[part_type](hp=hp, bc=bc, size=size)

        work_slot_index = self.current_work.index(None)
        self.current_work[work_slot_index] = [new_part, self.need_days]
        if self not in self.base_ptr.time_passed_tasks:
            self.base_ptr.time_passed_tasks.append(self)

    def dispose_old_part(self, part_type, part_index):
        self.base_ptr.unlocked_parts[part_type].pop(part_index)

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
        if len(self.base_ptr.unlocked_parts['chs']) <= 0:
            print('必须有至少一款载具骨架才能设计！')
            return
        name: None | str = None
        while name is None:
            name = input('设计命名（或输入ABORT中止设计）：')
            if name == 'ABORT':
                return
            elif name in self.base_ptr.loaded_designs:
                print('同名设计已存在！')
                name = None

        chs_selected_index = 0
        while True:
            print('第一阶段：选择', self.parts_names['chs'])
            chs_selected = self.base_ptr.unlocked_parts['chs'][chs_selected_index]
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
                chs_selected_index += len(self.base_ptr.unlocked_parts['chs'])
                chs_selected_index %= len(self.base_ptr.unlocked_parts['chs'])
            elif choice == '1':
                chs_selected_index += 1
                chs_selected_index += len(self.base_ptr.unlocked_parts['chs'])
                chs_selected_index %= len(self.base_ptr.unlocked_parts['chs'])
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
                    while len(self.base_ptr.unlocked_parts[pt]) > 0:
                        print('第二阶段：选择', self.parts_names[pt], '插槽尺寸：', i)
                        pt_selected = self.base_ptr.unlocked_parts[pt][pt_selected_index]
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
                            pt_selected_index += len(self.base_ptr.unlocked_parts[pt])
                            pt_selected_index %= len(self.base_ptr.unlocked_parts[pt])
                        elif choice == '1':
                            pt_selected_index += 1
                            pt_selected_index += len(self.base_ptr.unlocked_parts[pt])
                            pt_selected_index %= len(self.base_ptr.unlocked_parts[pt])
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
        self.base_ptr.loaded_designs.__setitem__(new_design.name, new_design)

    def delete_old_design(self, design_name):
        if design_name in self.base_ptr.loaded_designs:
            del self.base_ptr.loaded_designs[design_name]
        else:
            print('没有这个名称的设计！')

    def tomorrow(self):
        finished = []
        unfinished: list
        for index, unfinished in enumerate(self.current_work):
            if unfinished is not None:
                unfinished[1] -= 1
                if unfinished[1] <= 0:
                    finished.append(index)
                    new_part: Part = unfinished[0]
                    part_type = new_part.type_str
                    self.base_ptr.unlocked_parts[part_type].append(new_part)
                    print('你获得了新', Laboratory.parts_names[part_type], '！属性如下：')
                    attrs = [item for item in dir(new_part) if not item.startswith('__')]
                    for attr in attrs:
                        attr_val = getattr(new_part, attr)
                        if not hasattr(attr_val, '__call__'):
                            print(attr, attr_val)
        for fin in finished:
            self.current_work[fin] = None


class ConstructionCrane(Building):
    progress_record = {}
    cost_dict = {
        'command_center': {'wood': 10, 'time': 2},
        'laboratory': {'wood': 10, 'time': 2},

    }
    class_dict = {
        'command_center': CommandCenter,
        'laboratory': Laboratory
    }

    def __init__(self, slot, base_inst):
        super().__init__(2000, slot, 1, 'construction_crane', 'normal', base_inst)
        self.progress_record = {}

    def query_cost(self, building_type):
        print(ConstructionCrane.cost_dict[building_type])
        print()
        print(self.base_ptr.warehouse_basic)

    def build_new(self, slot, building_type):
        if building_type not in ConstructionCrane.class_dict:
            print('不可建造或建筑类型代码错误！')
        else:
            if 0 <= slot < len(self.base_ptr.buildings):
                if self.base_ptr.buildings[slot] is not None:
                    print('这个位置有建筑了！')
                else:
                    for res in ConstructionCrane.cost_dict[building_type]:
                        if res != 'time':
                            if ConstructionCrane.cost_dict[building_type][res] > self.base_ptr.warehouse_basic[res]:
                                print('资源不足，无法建造！')
                                return
                    for res in ConstructionCrane.cost_dict[building_type]:
                        if res != 'time':
                            self.base_ptr.consume_resource(res, ConstructionCrane.cost_dict[building_type][res])
                    new_b_id = str(uuid.uuid4())
                    self.base_ptr.buildings[slot] = new_b_id
                    self.progress_record.__setitem__(
                        new_b_id,
                        [
                            building_type,
                            ConstructionCrane.cost_dict[building_type]['time']
                        ]
                    )
                    if self not in self.base_ptr.time_passed_tasks:
                        self.base_ptr.time_passed_tasks.append(self)
            else:
                print('基地里没有空地可供建造新建筑')

    def remove_old(self, slot):
        if 0 <= slot < len(self.base_ptr.buildings):
            if self.base_ptr.buildings[slot] is None:
                print('这个位置没有建筑！')
            else:
                removed_building: Building | None | str = self.base_ptr.buildings[slot]
                if removed_building is self:
                    print('塔吊不能拆除自己！')
                else:
                    if type(removed_building) is str:
                        building_type = self.progress_record[removed_building][0]
                        del self.progress_record[removed_building]
                    else:
                        building_type = removed_building.type_str
                    for res in ConstructionCrane.cost_dict[building_type]:
                        if res != 'time':
                            self.base_ptr.add_resource(res, ConstructionCrane.cost_dict[building_type][res])
                    self.base_ptr.buildings[slot] = None
                    del removed_building
        else:
            print('空地编号超出有效范围！')

    def tomorrow(self):
        finished = []
        for unfinished in self.progress_record:
            unf_building = self.progress_record[unfinished]
            unf_building[1] -= 1
            if unf_building[1] <= 0:
                building_type = unf_building[0]
                slot = self.base_ptr.buildings.index(unfinished)
                self.base_ptr.buildings[slot] = ConstructionCrane.class_dict[building_type](
                    slot=slot,
                    b_ptr=self.base_ptr
                )
                finished.append(unfinished)
                print('新的', building_type, '在空地', slot, '完工了！')
        for fin in finished:
            del self.progress_record[fin]


class Factory(Building):
    pipeline: None | Pipeline = None
    pipeline_set = None
    design_set = None
    pt_passed = None
    quality_modifier = None
    qm_lower_bound = 0.5
    production_per_day = None
    build_cost_per_artifact = None

    def __init__(self, hp, slot, lv, ts, stat, b_ptr: Base):
        super().__init__(hp, slot, lv, ts, stat, b_ptr)
        self.pipeline = None
        self.pipeline_set = False
        self.design_set = False
        self.pt_passed = False
        self.quality_modifier = 0
        self.production_per_day = 0

    def set_pipeline_from_file(self, filename='pipeline.xls'):
        self.pipeline = read_pipeline_from_xls(filename)
        used_area = self.pipeline.pipeline_area()
        if used_area == 0:
            self.pipeline_set = False
            self.design_set = False
            self.pt_passed = False
            self.quality_modifier = 0
            self.production_per_day = 0
            print('未检测到任何流水线模块！请重新设计流水线并导入！')
        else:
            self.pipeline_set = True
            self.design_set = False
            self.pt_passed = False
            self.quality_modifier = 0
            self.production_per_day = 0
            print('流水线已导入，占地面积：', used_area)

    def set_design_from_base(self, design_name):
        if self.pipeline_set:
            if design_name in self.base_ptr.loaded_designs:
                design = self.base_ptr.loaded_designs[design_name]
                resource_types = []
                part_type_count = 0
                self.pipeline.set_requirement(design)
                for part_id in self.pipeline.requirement:
                    part_type_count += 1
                    for res_type in self.pipeline.requirement[part_id][0]:
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
                self.production_per_day = 0
                print('设计“', design_name, '”已导入流水线，产线复杂度：', self.quality_modifier)
            else:
                print('找不到名为', design_name, '的设计！')
        else:
            print('流水线未导入！')

    def production_test(self):
        if self.pipeline_set and self.design_set:
            self.production_per_day = self.pipeline.performance_test()
            if self.production_per_day > 0:
                self.pt_passed = True
                print('生产测试已通过，日产量：', self.production_per_day)
            else:
                self.pt_passed = False
                print('生产测试未通过！无法在一天时间内产出至少一件产品！')
        else:
            self.pt_passed = False
            print('流水线未导入或载具设计未指定！')


if __name__ == '__main__':
    print('Done')
