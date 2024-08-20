from Engine.Core import Core
from Mechanism.Game import Game
from Mechanism.Graphic import Button, Camera, EntitySprite

if __name__ == '__main__':
    game = Game()
    core = Core(game_obj=game)

    cam = Camera(screen=core.renderer.screen)
    cam.world_x = 2048
    cam.world_y = 2048


    def btn_up(params, recent_input):
        print('up')
        cam.world_y -= 16
        game.remove_routine(func=btn_up)
        return None, None


    def btn_down(params, recent_input):
        print('down')
        cam.world_y += 16
        game.remove_routine(func=btn_down)
        return None, None


    def btn_left(params, recent_input):
        print('left')
        cam.world_x -= 16
        game.remove_routine(func=btn_left)
        return None, None


    def btn_right(params, recent_input):
        print('right')
        cam.world_x += 16
        game.remove_routine(func=btn_right)
        return None, None


    up = Button(name='up', image_path='Assets/btn.png', x=640, y=8, game=game)
    down = Button(name='down', image_path='Assets/btn.png', x=640, y=712, game=game)
    left = Button(name='left', image_path='Assets/btn.png', x=8, y=360, game=game)
    right = Button(name='right', image_path='Assets/btn.png', x=1272, y=360, game=game)
    up.reg_callback(callback=btn_up)
    down.reg_callback(callback=btn_down)
    left.reg_callback(callback=btn_left)
    right.reg_callback(callback=btn_right)
    jet = EntitySprite(name='jet', image_path='Assets/F-5E.png', cam=cam, world_x=2048, world_y=2048, game=game)

    core.engine_run()
