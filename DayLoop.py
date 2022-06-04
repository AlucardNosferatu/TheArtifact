from Base import Base, ConstructionCrane


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
    pass


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
