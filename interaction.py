import os
import pickle
import random
import time

import pygame

from base import ConstructionCrane, Laboratory, Factory, CommandCenter
from map import Base, ResourceSite, MapEvent


def interaction_everyday(r_queue, map_events, day_count, surface_img_dict):
    if day_count == 0:
        com = None
        while com not in ['0', '1']:
            com = input('0.新游戏 1.继续游戏')
            if com == '0':
                map_events = interaction_first_day(map_events)
                day_count += 1
                break
            elif com == '1':
                loaded = game_load()
                if None in loaded:
                    com = None
                else:
                    map_events, surface_img_dict, day_count, r_queue = loaded
            else:
                print('指令错误！')
    else:
        print('今天是第' + str(day_count + 1) + '天')
        com = input('输入指令')
        if com == 'tomorrow':
            map_events, r_queue, surface_img_dict = after_1_day(
                map_events,
                r_queue,
                surface_img_dict
            )
            day_count += 1
        else:
            base_inst = map_events[0]
            assert type(base_inst) is Base
            if com == 'stats':
                display_stat(base_inst)
            elif com == 'build':
                module_build(base_inst)
            elif com == 'design':
                module_design(base_inst)
            elif com == 'tasks':
                r_queue, surface_img_dict = module_tasks(
                    base_inst,
                    r_queue,
                    map_events,
                    surface_img_dict
                )
            elif com == 'produce':
                module_factory(base_inst)
            elif com == 'save':
                game_save(map_events, surface_img_dict, day_count, r_queue)
            elif com == 'load':
                loaded = game_load()
                if None in loaded:
                    print('读档发生错误！')
                else:
                    map_events, surface_img_dict, day_count, r_queue = loaded
                    return r_queue, map_events, day_count, surface_img_dict
            else:
                print('指令错误')
    return r_queue, map_events, day_count, surface_img_dict


def display_stat(base_inst: Base):
    print('基地物资：')
    print(base_inst.warehouse_basic)
    print('物资存储上限：')
    print(base_inst.warehouse_cap)


def module_build(base_inst: Base):
    crane_list = []
    for i in range(len(base_inst.buildings)):
        if type(base_inst.buildings[i]) is ConstructionCrane:
            crane_list.append(base_inst.buildings[i])
    if len(crane_list) <= 0:
        print('基地里没有塔吊！')
    else:
        print(crane_list)
        crane_no = input('输入塔吊编号')
        if crane_no.isdigit() and 0 <= int(crane_no) < len(crane_list):
            selected_crane: ConstructionCrane = crane_list[int(crane_no)]
            flag = True
            while flag:
                building_com = input('0.显示所有建筑 1.建造新建筑 2.拆除旧建筑 3.返回')
                if building_com == '0':
                    print(base_inst.buildings)
                elif building_com == '1':
                    slot_index = base_inst.next_building_slot()
                    building_type = input('请输入建筑类型代号')
                    selected_crane.build_new(slot_index, building_type)
                elif building_com == '2':
                    slot_index = input('请输入建筑槽位编号')
                    if slot_index.isdigit():
                        selected_crane.remove_old(int(slot_index))
                    else:
                        print('输入有误！')
                        continue
                elif building_com == '3':
                    break
                else:
                    print('输入有误！')
                    continue
                building_com = '-1'
                while building_com not in ['0', '1']:
                    building_com = input('0.继续 1.返回')
                    if building_com == '0':
                        flag = True
                        break
                    elif building_com == '1':
                        flag = False
                        break
                    else:
                        print('输入有误！')
        else:
            print('输入有误！')


def module_design(base_inst: Base):
    lab_list = []
    for i in range(len(base_inst.buildings)):
        if type(base_inst.buildings[i]) is Laboratory:
            lab_list.append(base_inst.buildings[i])
    if len(lab_list) <= 0:
        print('基地里没有实验室！')
    else:
        print(lab_list)
        lab_no = input('输入实验室编号')
        if lab_no.isdigit() and 0 <= int(lab_no) < len(lab_list):
            selected_lab: Laboratory = lab_list[int(lab_no)]
            flag = True
            while flag:
                print('0.显示所有零件 1.显示所有设计 2.研究新零件 3.销毁旧零件 4.中止研究')
                research_com = input('5.创建新设计 6.销毁旧设计 7.从文件读取设计 8.保存设计到文件 9.返回')
                if research_com == '0':
                    print(base_inst.unlocked_parts)
                elif research_com == '1':
                    print(base_inst.designs)
                elif research_com == '2':
                    part_type = input('请输入零件类型代号')
                    if part_type in selected_lab.part_class_dict:
                        selected_lab.research_new_part(part_type)
                    else:
                        print('输入有误！')
                        continue
                elif research_com == '3':
                    part_type = input('请输入零件类型代号')
                    if part_type in selected_lab.part_class_dict:
                        print('该类零件如下：')
                        for p in base_inst.unlocked_parts[part_type]:
                            attrs = [item for item in dir(p) if not item.startswith('__')]
                            for attr in attrs:
                                attr_val = getattr(p, attr)
                                if not hasattr(attr_val, '__call__'):
                                    print(attr, attr_val)
                        slot_index = input('请输入待删零件编号')
                        if slot_index.isdigit():
                            selected_lab.dispose_old_part(part_type=part_type, part_index=int(slot_index))
                        else:
                            print('输入有误！')
                            continue
                    else:
                        print('输入有误！')
                        continue
                elif research_com == '4':
                    print('正在进行的研究如下：')
                    for work in selected_lab.current_work:
                        print(work)
                    slot_index = input('请输入待中止研究编号')
                    if slot_index.isdigit():
                        selected_lab.terminate_ongoing_res(work_index=int(slot_index))
                    else:
                        print('输入有误！')
                        continue
                elif research_com == '5':
                    selected_lab.compose_new_design()
                elif research_com == '6':
                    print(base_inst.designs.keys())
                    name = input('输入要删除的设计名称')
                    selected_lab.delete_old_design(design_name=name)
                elif research_com == '7':
                    bin_filepath = input('请输入设计图纸的文件名称：')
                    selected_lab.load_design_from_file(bin_filepath)
                elif research_com == '8':
                    print(base_inst.designs.keys())
                    name = input('输入要保存的设计名称')
                    selected_lab.save_design_to_file(name)
                elif research_com == '9':
                    break
                else:
                    print('输入有误！')
                    continue
                research_com = '-1'
                while research_com not in ['0', '1']:
                    research_com = input('0.继续 1.返回')
                    if research_com == '0':
                        flag = True
                        break
                    elif research_com == '1':
                        flag = False
                        break
                    else:
                        print('输入有误！')
        else:
            print('输入有误！')


def module_tasks(base_inst: Base, r_queue, map_events, surface_img_dict):
    cc_list = []
    for i in range(len(base_inst.buildings)):
        if type(base_inst.buildings[i]) is CommandCenter:
            cc_list.append(base_inst.buildings[i])
    if len(cc_list) <= 0:
        print('基地里没有指挥中心！')
    else:
        print(cc_list)
        cc_no = input('输入指挥中心编号')
        if cc_no.isdigit() and 0 <= int(cc_no) < len(cc_list):
            selected_cc: CommandCenter = cc_list[int(cc_no)]
            flag = True
            while flag:
                strategy_com = input('0.立刻扫描一次 1.开关持续扫描 2.组建战术群 3.返回')
                if strategy_com == '0':
                    r_queue = selected_cc.scan_events(global_events=map_events, r_queue=r_queue)
                    r_queue, surface_img_dict = surfaces_render_queue(r_queue, surface_img_dict)
                elif strategy_com == '1':
                    selected_cc.toggle_continuous_scan()
                elif strategy_com == '2':
                    pass
                elif strategy_com == '3':
                    break
                else:
                    print('输入有误！')
                    continue
                strategy_com = '-1'
                while strategy_com not in ['0', '1']:
                    strategy_com = input('0.继续 1.返回')
                    if strategy_com == '0':
                        flag = True
                        break
                    elif strategy_com == '1':
                        flag = False
                        break
                    else:
                        print('输入有误！')
            r_queue = selected_cc.clear_scanned(r_queue)
        else:
            print('输入有误！')
    return r_queue, surface_img_dict


def module_factory(base_inst: Base):
    factory_list = []
    for i in range(len(base_inst.buildings)):
        if type(base_inst.buildings[i]) is Factory:
            factory_list.append(base_inst.buildings[i])
    if len(factory_list) <= 0:
        print('基地里没有工厂！')
    else:
        print(factory_list)
        fac_no = input('输入工厂编号')
        if fac_no.isdigit() and 0 <= int(fac_no) < len(factory_list):
            selected_fac: Factory = factory_list[int(fac_no)]
            flag = True
            while flag:
                produce_com = input('0.开始生产 1.产线规划导入 2.产品设计导入 3.生产流程测试 4.返回')
                if produce_com == '0':
                    amount_str = input('请输入计划生产的产品个数：')
                    if amount_str.isdigit():
                        selected_fac.produce(int(amount_str))
                    else:
                        print('输入有误！')
                        continue
                elif produce_com == '1':
                    xls_filepath = input('请输入产线图纸的文件名称：')
                    if os.path.exists(xls_filepath):
                        selected_fac.set_pipeline_from_file(xls_filepath)
                    else:
                        print('文件', xls_filepath, '不存在！')
                        continue
                elif produce_com == '2':
                    design_name = input('请输入记录在案的设计名称：')
                    selected_fac.set_design_from_base(design_name)
                elif produce_com == '3':
                    selected_fac.production_test()
                elif produce_com == '4':
                    break
                else:
                    print('输入有误！')
                    continue
                produce_com = '-1'
                while produce_com not in ['0', '1']:
                    produce_com = input('0.继续 1.返回')
                    if produce_com == '0':
                        flag = True
                        break
                    elif produce_com == '1':
                        flag = False
                        break
                    else:
                        print('输入有误！')
        else:
            print('输入有误！')


def map_events_update(map_events):
    # todo
    x = random.randint(0, 2028)
    y = random.randint(0, 1223)
    new_event = ResourceSite(x, y, 'wood', 5000)
    map_events.append(new_event)

    if len(map_events) > 10:
        del map_events[1]
    return map_events


def after_1_day(map_events, r_queue, surface_img_dict):
    for i in range(1440):
        time.sleep(0.01)
        h = int(i / 60)
        m = i % 60
        if m % 10 == 0:
            map_events = map_events_update(map_events)
            print('时间：', h, '点', m, '分')
        r_queue, surface_img_dict = surfaces_render_queue(r_queue, surface_img_dict)
        for event in map_events:
            event: MapEvent
            for obj in event.time_passed_tasks:
                map_events, r_queue = obj.tomorrow(map_events, r_queue)
    return map_events, r_queue, surface_img_dict


def interaction_first_day(map_events):
    base_inst = Base(1014, 612)
    print('今天是第1天')
    input('按任意键继续')
    print('送你一个塔吊，不然你啥都建不了')
    slot_index = base_inst.next_building_slot()
    base_inst.buildings[slot_index] = ConstructionCrane(slot_index, base_inst)
    input('按任意键继续')
    print('再给你一些物资')
    base_inst.add_resource('wood', 100)
    base_inst.add_resource('steel', 100)
    base_inst.add_resource('e-device', 100)
    input('按任意键继续')
    map_events.append(base_inst)
    return map_events


def img_dict_conv_d2p(s_img_dict):
    p_dict = {}
    for img_id in s_img_dict:
        rect = s_img_dict[img_id][1].center
        path = s_img_dict[img_id][2]
        p_list = [rect, path]
        p_dict.__setitem__(img_id, p_list)
    return p_dict


def img_dict_conv_p2d(p_dict):
    s_img_dict = {}
    for img_id in p_dict:
        rect_center = p_dict[img_id][0]
        path = p_dict[img_id][1]
        surface = pygame.image.load(path)
        rect = surface.get_rect(center=rect_center)
        s_img_dict.__setitem__(img_id, [surface, rect, path])
    return s_img_dict


def game_save(map_events: list[MapEvent], surface_img_dict, dc, r_queue):
    hms = os.path.exists('Save/map_events.bin')
    his = os.path.exists('Save/img_dict.bin')
    hds = os.path.exists('Save/day_count.bin')
    hrs = os.path.exists('Save/r_queue.bin')
    if hms and his and hds and hrs:
        save_com = input('0.覆盖存档 1.取消保存')
        if save_com == '0':
            with open('Save/map_events.bin', 'wb') as f:
                pickle.dump(map_events, f)
            with open('Save/img_dict.bin', 'wb') as f:
                pickle_img_dict = img_dict_conv_d2p(surface_img_dict)
                pickle.dump(pickle_img_dict, f)
            with open('Save/day_count.bin', 'wb') as f:
                pickle.dump(dc, f)
            with open('Save/r_queue.bin', 'wb') as f:
                pickle.dump(r_queue, f)
            print('存档保存完毕。')
        elif save_com == '1':
            print('存档作业已中止。')
        else:
            print('指令错误，存档作业已中止。')
    else:
        with open('Save/map_events.bin', 'wb') as f:
            pickle.dump(map_events, f)
        with open('Save/img_dict.bin', 'wb') as f:
            pickle_img_dict = img_dict_conv_d2p(surface_img_dict)
            pickle.dump(pickle_img_dict, f)
        with open('Save/day_count.bin', 'wb') as f:
            pickle.dump(dc, f)
        with open('Save/r_queue.bin', 'wb') as f:
            pickle.dump(r_queue, f)
        print('存档保存完毕。')


def game_load():
    hms = os.path.exists('Save/map_events.bin')
    his = os.path.exists('Save/img_dict.bin')
    hds = os.path.exists('Save/day_count.bin')
    hrs = os.path.exists('Save/r_queue.bin')
    if hms and his and hds and hrs:
        with open('Save/map_events.bin', 'rb') as f:
            map_events = pickle.load(f)
        with open('Save/img_dict.bin', 'rb') as f:
            pickle_img_dict = pickle.load(f)
            surface_img_dict = img_dict_conv_p2d(pickle_img_dict)
        with open('Save/day_count.bin', 'rb') as f:
            dc = pickle.load(f)
        with open('Save/r_queue.bin', 'rb') as f:
            r_queue = pickle.load(f)
        print('存档读取完毕。')
        return map_events, surface_img_dict, dc, r_queue
    else:
        print('没有存档文件或存档文件不完整，读档作业已中止')
        return None, None, None, None


def surfaces_render_queue(r_queue, surface_img_dict):
    for render_task in r_queue:
        task_type = render_task[0]
        img_id = render_task[1]
        img_path = render_task[2]
        img_pos = render_task[3]
        if task_type == 'load_new':
            new_img = pygame.image.load(img_path)
            new_rect = new_img.get_rect()
            new_rect.center = tuple(img_pos)
            surface_img_dict[img_id] = [new_img, new_rect, img_path]
        elif task_type == 'move_old':
            surface_img_dict[img_id][1] = tuple(img_pos)
        elif task_type == 'delete_old':
            del surface_img_dict[img_id]
    r_queue.clear()
    return r_queue, surface_img_dict
