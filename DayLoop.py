from Base import Base, ConstructionCrane


def display_stat():
    pass


def build_module():
    pass


def design_module():
    pass


def tasks_module():
    pass


def factory_module():
    pass


def after_1_day():
    for obj in time_passed_tasks:
        obj.tomorrow()


def first_day(base_inst: Base):
    print('今天是第1天')
    input('按任意键继续')
    print('送你一个塔吊，不然你啥都建不了')
    slot_index = base_inst.next_building_slot()
    base_inst.buildings[slot_index] = ConstructionCrane(base_inst)
    input('按任意键继续')
    print('再给你一些物资')
    base_inst.add_resource('wood', 100)
    base_inst.add_resource('concrete', 101)
    input('按任意键继续')


if __name__ == '__main__':
    day_count = 0
    time_passed_tasks = []
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
                after_1_day()
            else:
                if com == 'stats':
                    display_stat()
                elif com == 'build':
                    build_module()
                elif com == 'design':
                    design_module()
                elif com == 'tasks':
                    tasks_module()
                elif com == 'factory':
                    factory_module()
                else:
                    print('指令错误')
