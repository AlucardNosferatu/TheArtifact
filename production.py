import random
import uuid
from types import NoneType

import xlrd

from designs import Design, Chassis, Engine


def read_pipeline_from_xls(filename):
    workbook = xlrd.open_workbook(filename=filename)
    table: xlrd.sheet.Sheet = workbook.sheets()[0]
    size = table.name.split('-')
    size = [int(item) for item in size]
    wid, hei = size
    p = Pipeline(wid, hei)
    for i in range(wid):
        for j in range(hei):
            cell_str = table.cell_value(j, i)
            if cell_str != '':
                if cell_str in Pipeline.conv_dict:
                    p.set_block(
                        i,
                        j,
                        {'type': 'conv', 'params': [cell_str]},
                        True
                    )
                else:
                    params = cell_str.split(':')
                    type_str = params.pop(0)
                    p.set_block(
                        i,
                        j,
                        {'type': type_str, 'params': params},
                        True
                    )
    return p


def upper_cell(x, y):
    return x, y - 1


def lower_cell(x, y):
    return x, y + 1


def left_cell(x, y):
    return x - 1, y


def right_cell(x, y):
    return x + 1, y


class Pipeline:
    width = None
    height = None
    matrix = None
    matrix_res = None
    requirement = None
    design = None
    conv_dict = {
        '↑': [lower_cell, upper_cell],
        '↓': [upper_cell, lower_cell],
        '←': [right_cell, left_cell],
        '→': [left_cell, right_cell],

        '↑→': [lower_cell, right_cell],
        '↓←': [right_cell, lower_cell],
        '→↓': [left_cell, lower_cell],
        '←↑': [lower_cell, left_cell],

        '↑←': [right_cell, upper_cell],
        '↓→': [upper_cell, right_cell],
        '←↓': [upper_cell, left_cell],
        '→↑': [left_cell, upper_cell]
    }
    join_dict = {
        'u': [lower_cell, left_cell, right_cell],
        'd': [upper_cell, left_cell, right_cell],
        'l': [upper_cell, lower_cell, right_cell],
        'r': [upper_cell, lower_cell, left_cell]
    }
    fin_asm_list = None
    part_asm_list = None
    produced = None
    timer = None
    upt = None
    wasted_part = None

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.matrix = []
        self.matrix_res = []
        self.fin_asm_list = []
        self.part_asm_list = []
        for r_index in range(h):
            row: list[None | dict] = []
            row_res: list[None | str | dict] = []
            for c_index in range(self.width):
                row.append(None)
                row_res.append(None)
            self.matrix.append(row)
            self.matrix_res.append(row_res)
        self.produced = 0
        self.timer = 0
        self.upt = 0
        self.wasted_part = 0

    def reset_produced(self):
        self.produced = 0
        self.wasted_part = 0

    def reset_timer(self):
        self.timer = 0

    def set_requirement(self, design: Design):
        self.design = design
        req_list = []
        id_list = []
        self.requirement = {}

        design_chs = self.design.chassis_in_use
        req_list.append(design_chs)
        part_id = str(uuid.uuid4())
        id_list.append(part_id)
        self.requirement.__setitem__(part_id, [design_chs.build_cost, 1])

        for pt in design.slots:
            for size in range(3):
                for part in design.slots[pt][size]:
                    if part not in req_list:
                        req_list.append(part)
                        part_id = str(uuid.uuid4())
                        id_list.append(part_id)
                        self.requirement.__setitem__(part_id, [part.build_cost, 1])
                    else:
                        req_list_index = req_list.index(part)
                        part_id = id_list[req_list_index]
                        req_list.append(part)
                        id_list.append(part_id)
                        parts_count = id_list.count(part_id)
                        self.requirement.__setitem__(part_id, [part.build_cost, parts_count])
        for fin_asm in self.fin_asm_list:
            block_dict, x, y = fin_asm
            need_dict: dict[str, None | dict] = {'out': None}
            for part_id in self.requirement:
                parts_count = self.requirement[part_id][1]
                need_dict.__setitem__(part_id, {'need': parts_count, 'have': 0})
            self.set_block_res(x, y, need_dict)
        for asm_index, part_asm in enumerate(self.part_asm_list):
            block_dict, x, y = part_asm
            need_dict: dict[str, None | dict] = {'out': None}
            if block_dict['params'][0] == 'chs':
                part = self.design.chassis_in_use
                req_list_index = req_list.index(part)
                part_id = id_list[req_list_index]
                block_dict['params'] = ['chs', '-1', '0', part_id]
            else:
                p_type, size, index = block_dict['params'][:3]
                part = self.design.slots[p_type][int(size)][int(index)]
                req_list_index = req_list.index(part)
                part_id = id_list[req_list_index]
                block_dict['params'] = [p_type, size, index, part_id]

            self.set_block(x, y, block_dict)
            part_asm = [block_dict, x, y]
            self.part_asm_list[asm_index] = part_asm
            build_cost: dict[str, int] = self.requirement[part_id][0]
            for res in build_cost:
                need_dict.__setitem__(res, {'need': build_cost[res], 'have': 0})
            self.set_block_res(x, y, need_dict)

    def set_block(self, x, y, block_dict, init=False):
        self.matrix[y][x] = block_dict
        if init:
            if block_dict['type'] == 'A':
                if block_dict['params'][0] == 'fin':
                    self.fin_asm_list.append([block_dict, x, y])
                else:
                    self.part_asm_list.append([block_dict, x, y])

    def set_block_res(self, x, y, res_str: None | str | dict):
        self.matrix_res[y][x] = res_str

    def get_block(self, x, y):
        return self.matrix[y][x]

    def get_block_res(self, x, y):
        return self.matrix_res[y][x]

    def recurse_cell(self, block_dict, x, y, visited):
        # noinspection PyUnusedLocal
        res_type = None
        if [x, y] in visited:
            pass
        else:
            visited.append([x, y])
            recurse_list = []
            if block_dict['type'] == 'conv':
                src_xy = Pipeline.conv_dict[block_dict['params'][0]][0]
                x_prev, y_prev = src_xy(x, y)
                recurse_list.append([x_prev, y_prev])
                if self.get_block_res(x, y) is None:
                    prev_res = self.get_block_res(x_prev, y_prev)
                    if type(prev_res) is dict:
                        self.set_block_res(x, y, prev_res['out'])
                        prev_res['out'] = None
                        self.set_block_res(x_prev, y_prev, prev_res)
                    else:
                        self.set_block_res(x, y, prev_res)
                        self.set_block_res(x_prev, y_prev, None)
            elif block_dict['type'] == 'join':
                src_locate = Pipeline.join_dict[block_dict['params'][0]]
                joined_src = []
                for i in range(3):
                    x_prev, y_prev = src_locate[i](x, y)
                    if self.get_block(x_prev, y_prev) is not None:
                        joined_src.append([x_prev, y_prev])
                        recurse_list.append([x_prev, y_prev])

                if self.get_block_res(x, y) is None:
                    selected_src = int(block_dict['params'][1])
                    x_prev, y_prev = joined_src[selected_src]
                    selected_src = (selected_src + 1) % len(joined_src)
                    block_dict['params'][1] = str(selected_src)
                    self.set_block(x, y, block_dict)
                    prev_res = self.get_block_res(x_prev, y_prev)
                    if prev_res is None or (type(prev_res) is dict and prev_res['out'] is None):
                        possible_src = []
                        for i in range(len(joined_src)):
                            x_prev, y_prev = joined_src[i]
                            prev_res = self.get_block_res(x_prev, y_prev)
                            if prev_res is not None:
                                if type(prev_res) is str or (type(prev_res) is dict and prev_res['out'] is not None):
                                    possible_src.append([x_prev, y_prev])
                        if len(possible_src) > 0:
                            x_prev, y_prev = random.choice(possible_src)
                            prev_res = self.get_block_res(x_prev, y_prev)
                    if type(prev_res) is dict:
                        self.set_block_res(x, y, prev_res['out'])
                        prev_res['out'] = None
                        self.set_block_res(x_prev, y_prev, prev_res)
                    else:
                        self.set_block_res(x, y, prev_res)
                        self.set_block_res(x_prev, y_prev, None)
            elif block_dict['type'] == 'A':
                # region prepare recurse_list
                src_locate = [upper_cell, lower_cell, left_cell]
                joined_src = []
                for i in range(3):
                    x_prev, y_prev = src_locate[i](x, y)
                    if self.get_block(x_prev, y_prev) is not None:
                        joined_src.append([x_prev, y_prev])
                        recurse_list.append([x_prev, y_prev])
                # endregion
                res_dict = self.get_block_res(x, y)
                # region fill_req
                still_need_after_loading = []
                for res_str in res_dict:
                    if res_str != 'out':
                        for x_prev, y_prev in joined_src:
                            prev_res = self.get_block_res(x_prev, y_prev)
                            if res_dict[res_str]['need'] > res_dict[res_str]['have']:
                                if prev_res == res_str:
                                    res_dict[res_str]['have'] += 1
                                    self.set_block_res(x_prev, y_prev, None)
                                elif type(prev_res) not in [NoneType, str] and prev_res['out'] == res_str:
                                    res_dict[res_str]['have'] += 1
                                    prev_res['out'] = None
                                    self.set_block_res(x_prev, y_prev, prev_res)
                            else:
                                break
                        if res_dict[res_str]['need'] > res_dict[res_str]['have']:
                            still_need_after_loading.append(res_str)
                # endregion
                # region clear jammed resources
                for x_prev, y_prev in joined_src:
                    prev_res = self.get_block_res(x_prev, y_prev)
                    if prev_res is not None:
                        if type(prev_res) is str:
                            if prev_res not in still_need_after_loading:
                                self.set_block_res(x_prev, y_prev, None)
                                self.wasted_part += 1
                        elif type(prev_res) is dict:
                            if prev_res['out'] not in still_need_after_loading:
                                prev_res['out'] = None
                                self.set_block_res(x_prev, y_prev, prev_res)
                                self.wasted_part += 1
                # endregion
                # region release product
                if res_dict['out'] is None:
                    ready = True
                    for res_str in res_dict:
                        if res_str != 'out':
                            if res_dict[res_str]['need'] == res_dict[res_str]['have']:
                                continue
                            else:
                                ready = False
                                break
                    if ready:
                        for res_str in res_dict:
                            if res_str != 'out':
                                res_dict[res_str]['have'] = 0
                        params = block_dict['params']
                        if params[0] == 'fin':
                            res_dict['out'] = None
                            self.produced += 1
                            self.upt = self.timer / self.produced
                            # print('time:', self.timer, 'produced:', self.produced, 'UPT:', self.upt)
                        else:
                            res_dict['out'] = params[3]
                # endregion
                self.set_block_res(x, y, res_dict)
            elif block_dict['type'] == 'R':
                if self.get_block_res(x, y) is None:
                    res_type = block_dict['params'][0]
                    self.set_block_res(x, y, res_type)
            for x, y in recurse_list:
                prev_block_dict = self.get_block(x, y)
                self.recurse_cell(prev_block_dict, x, y, visited)

    def flow_1_second(self):
        for fin_asm in self.fin_asm_list:
            block_dict, x, y = fin_asm
            visited = []
            self.recurse_cell(block_dict, x, y, visited)
        self.timer += 1
        # print('time:', self.timer)

    def layout_upper_bound(self):
        for i in range(self.height):
            for j in range(self.width):
                cell = self.get_block(j, i)
                if cell is not None:
                    return i
        return -1

    def layout_lower_bound(self):
        for i in range(self.height):
            for j in range(self.width):
                cell = self.get_block(j, self.height - i - 1)
                if cell is not None:
                    return self.height - i - 1
        return -1

    def layout_left_bound(self):
        for i in range(self.width):
            for j in range(self.height):
                cell = self.get_block(i, j)
                if cell is not None:
                    return i
        return -1

    def layout_right_bound(self):
        for i in range(self.width):
            for j in range(self.height):
                cell = self.get_block(self.width - i - 1, j)
                if cell is not None:
                    return self.width - i - 1
        return -1

    def pipeline_area(self):
        upper = self.layout_upper_bound()
        lower = self.layout_lower_bound()
        left = self.layout_left_bound()
        right = self.layout_right_bound()
        if -1 not in [upper, lower, left, right]:
            dx = right - left
            dy = lower - upper
            s = dx * dy
            print('占地面积：', s)
            return s
        else:
            print('占地面积计算错误！')
            return 0

    def performance_test(self):
        self.reset_timer()
        self.reset_produced()
        while self.timer < 1440:
            self.flow_1_second()
        day_production = round(1440 / self.upt)
        print('day_production', day_production)
        return day_production


if __name__ == '__main__':
    pipe = read_pipeline_from_xls('pipeline.xls')
    pipe.pipeline_area()

    slot_c = {'eng': [2, 0, 0]}
    chs = Chassis(hp=100, bc={'wood': 10}, size=-1, extra_params=[slot_c, 1.0])
    des = Design('test', chs)
    eng = Engine(10, {'wood': 10, 'steel': 10}, 0, [10, 10])
    des.slots['eng'][0][0] = eng
    des.slots['eng'][0][1] = eng

    pipe.set_requirement(des)
    pipe.performance_test()
