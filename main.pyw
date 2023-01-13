import pygame
from interface import *
from wave_function.wave_functions import *
from wave_function.wave_show import *
from wave_function.operators import *
from camera import Camera
from threading import Thread

pygame.init()
pygame.font.init()

menu = Group({})
canvas = Group({})
params = Group({})
game = Group({})
screen = Group({})

main_array = {'menu': menu, 'canvas': canvas, 'params': params, 'game': game, 'screen': screen, 'center': V(400, 300),
              'bg_color': [0, 0, 0], 'button_inner': V(60, 19), 'text_inner': V(60, 30), 'menu_color': [34, 65, 76],
              'menu_border_color': [130, 130, 130], 'menu_border_r': V(5, 5), 'go': False, 'cube': [8, 8, 8]}
# name_points: {points: list[{'mod': float, 'point': list[float], 'vector': list[float]}], cube: list[float],
#               'scalar_operator': scalar_operator, 'wave_function': wave_function
#               'finding_points': Bool, 'zn': float | Complex, 'max_col': int, 'min_delta': float}

points_density = {'points': [], 'cube': main_array['cube'], 'scalar_operator': density, 'wave_function': None,
                  'finding_points': False, 'zn': None, 'max_col': None, 'min_delta': None}
th1 = Thread(target=find_points, args=(points_density,)).start()

vectors_pulse = {'vectors': [], 'cube': main_array['cube'], 'vector_operator': operator_imag_vector(gradient),
                 'wave_function': None, 'finding_vectors': False, 'zn': None, 'max_col': None, 'min_delta': None}
th2 = Thread(target=find_vectors, args=(vectors_pulse,)).start()

window = Display({'pos': Pos(main_array['center'], main_array['center']),
                  'bg_color': main_array['bg_color']})

menu_plane = Element({'father': window, 'pos': Pos(main_array['center'], V(100, 200)), 'update': True,
                      'frame_array': [{'fun': fun_rect_border(main_array['menu_border_color'],
                                                              main_array['menu_border_r'], main_array['menu_color'])}],
                      'is_listen': True, 'is_draw': True, 'listened': {},
                      'functions': {}})
text_menu = Text({'father': menu_plane, 'pos': Pos(V(100, 40), V(60, 19))}, 'МЕНЮ')
button_canvas = Button({'father': menu_plane, 'pos': Pos(V(100, 100), V(60, 19))}, 'Холст')
button_canvas.set_click_action(change_group(menu, canvas))
button_params = Button({'father': menu_plane, 'pos': Pos(V(100, 170), V(80, 19))}, 'Визуализация')
button_params.set_click_action(change_group(menu, params))
button_exit = Button({'father': menu_plane, 'pos': Pos(V(100, 360), V(60, 19))}, 'Выход')
button_exit.set_click_action(window_exit)
menu.add_elements({'plane': menu_plane})

canvas_plane = Element({'father': window, 'pos': Pos(main_array['center'], V(280, 200)), 'update': True,
                        'frame_array': [{'fun': fun_rect_border(main_array['menu_border_color'],
                                                                main_array['menu_border_r'],
                                                                main_array['menu_color'])}],
                        'is_listen': True, 'is_draw': True, 'listened': {},
                        'functions': {}})
rect = Element({'father': canvas_plane, 'pos': Pos(V(280, 200), V(260, 140)),
                'update': True,
                'frame_array': [{'fun': fun_rect([100, 100, 100])},
                                {'fun': fun_rect([200, 200, 200])}],
                'is_listen': True, 'is_draw': True, 'listened': {},
                'functions': {'1': fun_attention, '2': fun_paint}})

text = Text({'father': canvas_plane, 'pos': Pos(V(280, 30), V(60, 19))}, 'Холст')
button = Button({'father': canvas_plane, 'pos': Pos(V(150, 368), V(60, 19))}, 'Очистить')
button.set_click_action(clear(rect))
canvas_exit = Button({'father': canvas_plane, 'pos': Pos(V(430, 368), V(60, 19))}, 'Назад')
canvas_exit.set_click_action(change_group(canvas, menu))
canvas.add_elements({'plane': canvas_plane})

params_plane = Element({'father': window, 'pos': Pos(main_array['center'], V(400, 300)), 'update': True,
                        'frame_array': [{'fun': fun_rect_border(main_array['menu_border_color'],
                                                                main_array['menu_border_r'],
                                                                main_array['menu_color'])}],
                        'is_listen': True, 'is_draw': True, 'listened': {},
                        'functions': {}})

canvas_exit_2 = Button({'father': params_plane, 'pos': Pos(V(70, 30), V(60, 19))}, 'Назад')
canvas_exit_2.set_click_action(change_group(params, menu))
text_hydrogen = Text({'father': params_plane, 'pos': Pos(V(180, 80), V(180, 19))}, 'Выберите волновую функцию -')
choice_hydrogen = ChoiceBox({'father': params_plane, 'pos': Pos(V(420, 80), V(60, 19))}, hydrogen_functions)

text_density = Text({'father': params_plane, 'pos': Pos(V(130, 130), V(180, 19))}, 'Отобразить плотность')
text_pulse = Text({'father': params_plane, 'pos': Pos(V(130, 180), V(180, 19))}, 'Отобразить импульс')

box_density = CheckBox({'father': params_plane, 'pos': Pos(V(270, 130), V(15, 15))})
box_pulse = CheckBox({'father': params_plane, 'pos': Pos(V(270, 180), V(15, 15))})

Text({'father': params_plane, 'pos': Pos(V(450, 130), V(180, 19))}, 'Колличество точек')
Text({'father': params_plane, 'pos': Pos(V(450, 180), V(180, 19))}, 'Колличество векторов')

input_density = Input({'father': params_plane, 'pos': Pos(V(640, 130), V(60, 19))})
input_pulse = Input({'father': params_plane, 'pos': Pos(V(640, 180), V(60, 19))})

Text({'father': params_plane, 'pos': Pos(V(350, 260), V(180, 19))}, 'Сгущать вокруг значения')
Text({'father': params_plane, 'pos': Pos(V(350, 310), V(180, 19))}, 'Сгущать вокруг значения')
Text({'father': params_plane, 'pos': Pos(V(500, 360), V(180, 19))},
     'Если хотите найти максимальные плотность и импульс')
Text({'father': params_plane, 'pos': Pos(V(500, 380), V(180, 19))}, 'укажите большое число ~10')

input_density_zn = Input({'father': params_plane, 'pos': Pos(V(550, 260), V(60, 19))})
input_pulse_zn = Input({'father': params_plane, 'pos': Pos(V(550, 310), V(60, 19))})

button_rego = Button({'father': params_plane, 'pos': Pos(V(260, 500), V(240, 25))},
                     'Применить параметры')
button_go = Button({'father': params_plane, 'pos': Pos(V(650, 500), V(100, 25))}, 'К Визувлизации')
button_go.set_click_action(change_group(params, screen))

button_rego.set_click_action(sum_function(
    copy_information(
        ['points', 'wave_function', 'finding_points', 'zn', 'max_col', 'min_delta'],
        [[], choice_hydrogen, box_density, input_density_zn, input_density, 100],
        points_density),
    copy_information(
        ['vectors', 'wave_function', 'finding_vectors', 'zn', 'max_col', 'min_delta'],
        [[], choice_hydrogen, box_pulse, input_pulse_zn, input_pulse, 100],
        vectors_pulse),
    copy_information(['go'], [True], main_array),
    change_group(params, screen)
))

params.add_elements({'plane': params_plane})

camera_plane = Element({'father': window, 'pos': Pos(main_array['center'], V(400, 300)), 'update': True,
                        'frame_array': [{'fun': fun_rect_border(main_array['menu_border_color'],
                                                                main_array['menu_border_r'],
                                                                main_array['menu_color'])}],
                        'is_listen': True, 'is_draw': True, 'listened': {},
                        'functions': {}})
button_back = Button({'father': camera_plane, 'pos': Pos(V(70, 30), V(60, 19))}, 'Назад')
button_back.set_click_action(sum_function(
    change_group(screen, params),
    copy_information(['finding_points'], [False], points_density),
    copy_information(['finding_vectors'], [False], vectors_pulse)
))
screen.add_elements({'plane': camera_plane})

camera = Camera((~camera_plane)['frame'], [0, 0, 0])

params.activate()
clock = pygame.time.Clock()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            choice_hydrogen.change_choice(event)
            input_density.change_text(event)
            input_pulse.change_text(event)
            input_density_zn.change_text(event)
            input_pulse_zn.change_text(event)
    window.step()
    if screen.state:
        camera.key_step()
        camera.set_matrix()
        camera.clear()
        camera.rend_xyz()
        if points_density['finding_points']:
            camera.color = [0, 0, 255]
            for point in points_density['points']:
                camera.rend_point2(point['point'])
        if vectors_pulse['finding_vectors']:
            camera.color = [0, 255, 0]
            for vector in vectors_pulse['vectors']:
                camera.rend_vector(vector['vector'])
    pygame.display.set_caption(str(clock.get_fps()))
    pygame.display.flip()
