from Vessel import *
from Building import *
from Equipment import *

nc = NomadCity(1014, 612)
nc.install_part(Command(), 0)
craft_0 = Craft()
thruster_0 = Thruster(10)
wing_0 = Wing(10)
ctrl_s_0 = CtrlSurface(10)
craft_0.install_part(thruster_0, 0)
craft_0.install_part(ctrl_s_0, 1)
craft_0.install_part(wing_0, 2)

nc.ap_basic[0] = craft_0
