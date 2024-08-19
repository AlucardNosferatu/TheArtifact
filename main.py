from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP

from Engine.Core import Core
from Mechanism.Game import Game, Button

upper_left = False
lower_right = False
cam = None


def update_jet(jet, jet_name, recent_input):
    global upper_left, lower_right
    # 这里应根据游戏逻辑处理参数和输入，返回draw_dict
    # 示例draw_dict为一个包含待绘制内容的字典
    res = jet.render()
    for event in recent_input:
        e = event[0]
        timestamp = event[1]
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            upper_left = True
        elif e.type == MOUSEBUTTONUP and e.button == 1:
            upper_left = False
        if e.type == MOUSEBUTTONDOWN and e.button == 3:
            lower_right = True
        elif e.type == MOUSEBUTTONUP and e.button == 3:
            lower_right = False
        if upper_left:
            cam.world_x += 10
            cam.world_y += 10
        if lower_right:
            cam.world_x -= 10
            cam.world_y -= 10
        res = jet.render()
    return jet_name, res


if __name__ == '__main__':
    game = Game()
    core = Core(game_obj=game)

    # cam = Camera(screen=core.renderer.screen)
    # cam.world_x = 2048
    # cam.world_y = 2048
    # jet1 = EntitySprite(image_path='Assets/F-5E.png', cam=cam, world_x=2080, world_y=2080)
    # jet2 = EntitySprite(image_path='Assets/F-5E.png', cam=cam, world_x=2048, world_y=2112)
    #
    #
    # def update_jet1(params, recent_input):
    #     return update_jet(jet=jet1, jet_name='jet1', recent_input=recent_input)
    #
    #
    # def update_jet2(params, recent_input):
    #     return update_jet(jet=jet2, jet_name='jet2', recent_input=recent_input)
    #
    #
    # game.load_routine(func=update_jet1)
    # game.load_routine(func=update_jet2)
    jet_button = Button(btn_name='jet_button', image_path='Assets/F-5E2.png', x=640, y=360, game=game)


    def button_callback(params, recent_input):
        print('clicked')
        game.remove_routine(func=button_callback)
        return None, None


    jet_button.reg_callback(callback=button_callback)
    core.engine_run()
