from Base import Base, ConstructionCrane, Laboratory


def display_stat(base_inst: Base):
    pass


def build_module(base_inst: Base):
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


def design_module(base_inst: Base):
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
                print('0.显示所有零件 1.显示所有设计 2.研究新零件 3.销毁旧零件')
                research_com = input('4.中止研究 5.创建新设计 6.销毁旧设计 7.返回')
                if research_com == '0':
                    print(base_inst.unlocked_parts)
                elif research_com == '1':
                    print(base_inst.loaded_designs)
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
                    print('设计中心暂不可用')
                elif research_com == '6':
                    print('设计中心暂不可用')
                elif research_com == '7':
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


def tasks_module(base_inst: Base):
    pass


def factory_module(base_inst: Base):
    pass


def after_1_day(base_inst: Base):
    for obj in base_inst.time_passed_tasks:
        obj.tomorrow()


def first_day(base_inst: Base):
    print('今天是第1天')
    input('按任意键继续')
    print('送你一个塔吊，不然你啥都建不了')
    slot_index = base_inst.next_building_slot()
    base_inst.buildings[slot_index] = ConstructionCrane(slot_index, base_inst)
    input('按任意键继续')
    print('再给你一些物资')
    base_inst.add_resource('wood', 100)
    base_inst.add_resource('concrete', 101)
    input('按任意键继续')


if __name__ == '__main__':
    day_count = 0
    NewBase = Base()
    while True:
        if day_count == 0:
            first_day(NewBase)
            day_count += 1
        else:
            print('今天是第' + str(day_count + 1) + '天')
            com = input('输入指令')
            if com == 'tomorrow':
                day_count += 1
                after_1_day(NewBase)
            else:
                if com == 'stats':
                    display_stat(NewBase)
                elif com == 'build':
                    build_module(NewBase)
                elif com == 'design':
                    design_module(NewBase)
                elif com == 'tasks':
                    tasks_module(NewBase)
                elif com == 'factory':
                    factory_module(NewBase)
                else:
                    print('指令错误')
