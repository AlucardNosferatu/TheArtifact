from Vessel import *
from Building import *
from Room import *
from Equipment import *
from Device import *


def get_city():
    # 在地图坐标x=1014,y=612的地方生成一个浮空城
    nc = NomadCity(1014, 612)
    # 在浮空城的0号建筑槽位搭建一个指挥中心
    nc.install_part(Command(), 0)
    for i in range(2):
        cv_0 = get_cv()
        drone_0 = get_drone()
        # 把战机放进浮空城基础格纳库的i号停机坪
        nc.ap_basic[i] = cv_0
        nc.ap_basic[i + 2] = drone_0
    return nc


def get_cv():
    cv_0 = CraftCarrier()
    pro_0 = Propulsion(30)
    le_0 = LiftEngine(100)
    cv_0.install_part(pro_0, 0)
    cv_0.install_part(le_0, 1)
    return cv_0


def get_craft():
    # 创建一个新战机对象c0
    craft_0 = Craft()
    # 创建一个30单位推力的推进器
    thruster_0 = Thruster(30)
    # 创建一个100单位升力的机翼
    wing_0 = Wing(100)
    # 创建一个最大偏航力矩为10的控制面
    ctrl_s_0 = CtrlSurface(10)
    # 安装推进器到战机c0的0号零件槽位上
    craft_0.install_part(thruster_0, 0)
    # 安装控制面到战机c0的1号零件槽位上
    craft_0.install_part(ctrl_s_0, 1)
    # 安装机翼到战机c0的2号零件槽位上
    craft_0.install_part(wing_0, 2)
    # # 创建一个钻头（用于开采矿石）
    # drill_0 = Drill()
    # # 安装钻头到战机c0的3号零件槽位上
    # craft_0.install_part(drill_0, 3)
    return craft_0


def get_drone():
    drone_0 = Drone()
    acc_0 = Accelerator(30)
    elevator_0 = Elevator(100)
    sm_0 = SteerMotor(10)
    st_0 = Stabilizer()
    drone_0.install_part(acc_0, 0)
    drone_0.install_part(elevator_0, 1)
    drone_0.install_part(sm_0, 2)
    drone_0.install_part(st_0, 3)
    return drone_0


def get_task_force():
    nc = get_city()
    nc.p_list[0].create_task_force([[0, 1]])
    nc.p_list[0].create_task_force([[2, 3]])
    tf1 = nc.p_list[0].tf_ptr[0]
    tf2 = nc.p_list[0].tf_ptr[1]
    x = nc.coordinate['x']
    y = nc.coordinate['y']
    tf1.set_coordinate(x + 50, y + 50)
    tf2.set_coordinate(x - 50, y - 50)
    tf1.engage(tf2)
    print('Done')


if __name__ == '__main__':
    get_task_force()
