from Vessel import *
from Building import *
from Equipment import *

# 在地图坐标x=1014,y=612的地方生成一个浮空城
nc = NomadCity(1014, 612)
# 在浮空城的0号建筑槽位搭建一个指挥中心
nc.install_part(Command(), 0)
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
# 创建一个钻头（用于开采矿石）
drill_0 = Drill()
# 安装钻头到战机c0的3号零件槽位上
craft_0.install_part(drill_0, 3)
# 把战机放进浮空城基础格纳库的0号停机坪
nc.ap_basic[0] = craft_0
