from Vessel import *
import cocos
from cocos.actions import *


def get_city():
    # 在地图坐标x=1014,y=612的地方生成一个浮空城
    nc = Vessel('huge', 1014, 612)
    # 在浮空城的0号建筑槽位搭建一个指挥中心
    nc.install_part(Command(), 0)
    nc.enable_part(0)
    for i in range(2):
        cv_0 = get_cv()
        drone_0 = get_drone()
        # 把战机放进浮空城基础格纳库的i号停机坪
        nc.ap_basic[i] = cv_0
        nc.ap_basic[i + 2] = drone_0
    return nc


def get_cv():
    cv_0 = Vessel('large')
    pro_0 = Propulsion(30, 30)
    le_0 = LiftEngine(100)
    sg_0 = SentryGun(45)
    cv_0.install_part(pro_0, 0)
    cv_0.enable_part(0)
    cv_0.install_part(le_0, 1)
    cv_0.enable_part(1)
    cv_0.install_part(sg_0, 2)
    cv_0.enable_part(2)
    return cv_0


def get_craft():
    # 创建一个新战机对象c0
    craft_0 = Vessel('medium')
    # 创建一个30单位推力的推进器
    thruster_0 = Thruster(30)
    # 创建一个100单位升力的机翼
    wing_0 = Wing(100)
    # 创建一个最大偏航力矩为10的控制面
    ctrl_s_0 = CtrlSurface(10)
    # 安装推进器到战机c0的0号零件槽位上
    craft_0.install_part(thruster_0, 0)
    craft_0.enable_part(0)
    # 安装控制面到战机c0的1号零件槽位上
    craft_0.install_part(ctrl_s_0, 1)
    craft_0.enable_part(1)
    # 安装机翼到战机c0的2号零件槽位上
    craft_0.install_part(wing_0, 2)
    craft_0.enable_part(2)
    # # 创建一个钻头（用于开采矿石）
    # drill_0 = Drill()
    # # 安装钻头到战机c0的3号零件槽位上
    # craft_0.install_part(drill_0, 3)
    return craft_0


def get_drone():
    drone_0 = Vessel('small')
    acc_0 = Accelerator(30)
    elevator_0 = Elevator(100)
    sm_0 = SteerMotor(10)
    st_0 = Stabilizer()
    gun12d7_0 = Gun12d7(50, 45, 20)
    drone_0.install_part(acc_0, 0)
    drone_0.enable_part(0)
    drone_0.install_part(elevator_0, 1)
    drone_0.enable_part(1)
    drone_0.install_part(sm_0, 2)
    drone_0.enable_part(2)
    drone_0.install_part(st_0, 3)
    drone_0.enable_part(3)
    drone_0.install_part(gun12d7_0, 4)
    drone_0.enable_part(4)
    return drone_0


def get_task_force():
    nc = get_city()
    nc.p_list[0].create_task_force([[0, 2]])
    nc.p_list[0].create_task_force([[1, 3]])
    tf1 = nc.p_list[0].tf_ptr[0]
    tf2 = nc.p_list[0].tf_ptr[1]
    x = nc.guard_force.coordinate['x']
    y = nc.guard_force.coordinate['y']
    tf1.set_coordinate(x + 10, y + 10)
    tf2.set_coordinate(x - 10, y - 10)
    tf2.engage(tf1)
    print('Done')


class HelloWorld(cocos.layer.ColorLayer):
    def __init__(self):
        super().__init__(64, 64, 224, 255)
        sprite = cocos.sprite.Sprite('F-5E.png')
        sprite.position = 320, 240
        sprite.scale = 3
        self.add(sprite, z=1)
        scale = ScaleBy(3, duration=2)
        sprite.do(Repeat(scale + Reverse(scale)))


if __name__ == '__main__':
    # get_task_force()
    cocos.director.director.init()
    hello_layer = HelloWorld()
    hello_layer.do(RotateBy(360, duration=10))
    main_scene = cocos.scene.Scene(hello_layer)
    cocos.director.director.run(main_scene)
