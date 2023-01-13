import math
import pygame
import copy
import re


class V:
    def __init__(self, *args):
        if isinstance(args[0], list | tuple):
            self.x = args[0][0]
            self.y = args[0][1]
        else:
            self.x = args[0]
            self.y = args[1]

    def __add__(self, other):
        return V(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return V(self.x - other.x, self.y - other.y)

    def __iadd__(self, other):
        return self

    def __isub__(self, other):
        return self - other

    def __neg__(self):
        self.x -= self.x
        self.y -= self.y

    def __pow__(self, power, modulo=None):
        k = math.pow(math.hypot(self.x, self.y), power - 1)
        self.x *= k
        self.y *= k

    def __mul__(self, other):
        return V(self.x * other, self.y * other)

    def __imul__(self, other):
        return self * other

    def __abs__(self):
        return math.hypot(self.x)

    def __str__(self):
        return f'{self.x}, {self.y}'

    def lis(self):
        return [self.x, self.y]

    def x(self):
        return V(self.x, 0)

    def y(self):
        return V(0, self.y)


null = V([0, 0])


class Pos:
    def __init__(self, center, inner):
        self.center = center
        self.inner = inner
        self.size = self.inner * 2
        self.position = self.center - self.inner

    def update(self):
        # center, inner -> position, size
        self.size = self.inner * 2
        self.position = self.center - self.inner

    def in_area(self, vector: V):
        if null.x <= vector.x <= self.size.x and null.y <= vector.y <= self.size.y:
            return True
        else:
            return False

    def copy(self):
        return Pos(self.center, self.inner)

    def scale(self, scale):
        self.inner *= scale
        self.update()
        return self


class Frames:
    def __init__(self, array: list[dict]):
        self.array = array
        self.current_frame = 0

    # ссылка на словарь фрейма
    def get_frame(self):
        return self.array[self.current_frame]

    # array.dict -> array.Surface
    # frame_dict[fun, pos, surf]
    def update_frames(self):
        for frame_dict in self.array:
            frame_dict.update({'frame': frame_dict['fun'](frame_dict)})

    def set_pos(self, pos):
        for i in self.array:
            i.update({'pos': pos.copy()})

    def __getitem__(self, item):
        return self.array[item]


def fun_rect(color):
    def fun(array):
        s = pygame.Surface(array['pos'].size.lis())
        s.fill(color)
        return s

    return fun


def fun_rect_border(border_color, border_r: V, back_color):
    def fun(array):
        border = pygame.Surface(array['pos'].size.lis())
        border.fill(border_color)
        pos = array['pos'].copy()
        pos.inner -= border_r
        pos.update()
        back = pygame.Surface(pos.size.lis())
        back.fill(back_color)
        border.blit(back, border_r.lis())
        return border

    return fun


def fun_attention(element):
    if element['listened'].get('mouse_attention'):
        element['frame_class'].current_frame = 1
    else:
        element['frame_class'].current_frame = 0


def fun_paint(element):
    if element['listened'].get('mouse_attention') and element['listened'].get('mouse_click'):
        pygame.draw.circle(
            element['frame_class'][1]['frame'], [0, 0, 0], element['listened']['mouse_position'], 1)


def clear(element):
    def fun(el):
        if el['listened'].get('button_click'):
            element['frame_class'].update_frames()

    return fun


def change_group(old_group, new_group):
    def fun(element):
        if element['listened'].get('button_click'):
            old_group.deactivate()
            new_group.activate()
            element['listened']['button_click'] = False

    return fun


def window_exit(element):
    if element['listened'].get('button_click'):
        pygame.quit()


def copy_information(keys: list[str], el: list, todo):
    def fun(element):
        if element['listened'].get('button_click'):
            for i in range(min(len(keys), len(el))):
                if isinstance(el[i], (Input, CheckBox, ChoiceBox)):
                    todo.update({keys[i]: el[i].get_information()})
                else:
                    todo.update({keys[i]: el[i]})
    return fun


def sum_function(*functions):
    def fun(element):
        for f in functions:
            f(element)
    return fun


def fun_text(frame_dict):
    if frame_dict.get('text'):
        s = pygame.font.SysFont(frame_dict.get('name'), frame_dict.get('size'),
                                frame_dict.get('bold'), frame_dict.get('italic')).render(
            frame_dict.get('text'), frame_dict.get('antialias'), frame_dict.get('color'))
        frame_dict['pos'].inner = V([i / 2 for i in s.get_size()])
        frame_dict['pos'].update()
        return s
    else:
        return fun_rect([10, 60, 160])(frame_dict)


def fun_text_attention(element):
    if element['listened'].get('mouse_attention'):
        element['frame_array'][0]['size'] += 1
    else:
        element['frame_array'][0]['size'] = 24
    element['frame_class'].update_frames()


def fun_button(frame_dict):
    s = pygame.font.SysFont(frame_dict.get('name'), frame_dict.get('size'),
                            frame_dict.get('bold'), frame_dict.get('italic')).render(
        frame_dict.get('text'), frame_dict.get('antialias'), frame_dict.get('color'))

    pos = frame_dict['pos'].copy()
    pos = Pos(pos.inner, pos.inner)
    pos.update()

    border = pygame.Surface(pos.size.lis())
    border.fill(frame_dict['border_color'])

    pos.inner -= V(frame_dict['border_r'], frame_dict['border_r'])
    pos.update()

    back = pygame.Surface(pos.size.lis())
    back.fill(frame_dict['back_color'])

    text_pos = Pos(pos.inner, V([i / 2 for i in s.get_size()]))

    back.blit(s, text_pos.position.lis())
    border.blit(back, pos.position.lis())
    return border


def listen_button(element):
    if element['frame_class'].current_frame == 0:
        if element['listened'].get('mouse_attention'):
            if not element['listened'].get('mouse_click'):
                element['frame_class'].current_frame = 1

    elif element['frame_class'].current_frame == 1:
        if not element['listened'].get('mouse_attention'):
            element['frame_class'].current_frame = 0
        if element['listened'].get('mouse_click'):
            element['frame_class'].current_frame = 2

    elif element['frame_class'].current_frame == 2:
        if not element['listened'].get('mouse_click'):
            element['listened'].update({'button_click': True})
            element['frame_class'].current_frame = 0
        if not element['listened'].get('mouse_attention'):
            element['frame_class'].current_frame = 0


def fun_off_box(frame_dict):
    pos = frame_dict['pos'].copy()
    pos = Pos(pos.inner, pos.inner)
    pos.update()

    border = pygame.Surface(pos.size.lis())
    border.fill(frame_dict['border_color'])

    pos.inner -= V(frame_dict['border_r'], frame_dict['border_r'])
    pos.update()

    back = pygame.Surface(pos.size.lis())
    back.fill(frame_dict['back_color'])

    border.blit(back, pos.position.lis())
    return border


def fun_on_box(frame_dict):
    pos = frame_dict['pos'].copy()
    pos = Pos(pos.inner, pos.inner)
    pos.update()

    border = pygame.Surface(pos.size.lis())
    border.fill(frame_dict['border_color'])

    pos.inner -= V(frame_dict['border_r'], frame_dict['border_r'])
    pos.update()

    pos_check = Pos(pos.inner, pos.inner)
    pos_check.inner -= V(frame_dict['check_r'], frame_dict['check_r'])
    pos_check.update()

    back = pygame.Surface(pos.size.lis())
    back.fill(frame_dict['back_color'])

    check = pygame.Surface(pos_check.size.lis())
    check.fill(frame_dict['check_color'])

    back.blit(check, pos_check.position.lis())

    border.blit(back, pos.position.lis())
    return border


def listen_box(element):
    if not element.state:
        if element['frame_class'].current_frame == 0:
            if element['listened'].get('mouse_attention'):
                if not element['listened'].get('mouse_click'):
                    element['frame_class'].current_frame = 1

        elif element['frame_class'].current_frame == 1:
            if not element['listened'].get('mouse_attention'):
                element['frame_class'].current_frame = 0
            if element['listened'].get('mouse_click'):
                element['frame_class'].current_frame = 2

        elif element['frame_class'].current_frame == 2:
            if not element['listened'].get('mouse_click'):
                element.state = True
                element['frame_class'].current_frame = 3
            if not element['listened'].get('mouse_attention'):
                element['frame_class'].current_frame = 0
    else:
        if element['frame_class'].current_frame == 3:
            if element['listened'].get('mouse_attention'):
                if not element['listened'].get('mouse_click'):
                    element['frame_class'].current_frame = 4

        elif element['frame_class'].current_frame == 4:
            if not element['listened'].get('mouse_attention'):
                element['frame_class'].current_frame = 3
            if element['listened'].get('mouse_click'):
                element['frame_class'].current_frame = 5

        elif element['frame_class'].current_frame == 5:
            if not element['listened'].get('mouse_click'):
                element.state = False
                element['frame_class'].current_frame = 0
            if not element['listened'].get('mouse_attention'):
                element['frame_class'].current_frame = 3


class Theme:
    def __init__(self, array):
        array.update({'suns': []})
        self.array = array

    def __getitem__(self, item):
        return self.array[item]

    def __setitem__(self, key, value):
        self.array.update({key: value})

    def activate(self):
        for el in self['suns']:
            for i in range(len(el['theme'][el.__class__.__name__])):
                el['frame_array'][i].update(el['theme'][el.__class__.__name__][i])
            if el['update']:
                el['frame_class'].set_pos(el['pos'])
                el['frame_class'].update_frames()
                el['surf'] = (~el)['frame'].copy()
    def update(self, array:dict):
        self.array.update(array)

main_theme = Theme({
    'Text': [{'name': 'serif', 'size': 24, 'bold': False, 'italic': False,
              'antialias': True, 'color': [255, 255, 255]}],
    'Button': [
        {'name': 'serif', 'size': 24,
         'bold': False, 'italic': False, 'antialias': True, 'color': [255, 255, 255],
         'border_color': [0, 255, 0], 'border_r': 2, 'back_color': [14, 129, 94]},
        {'name': 'serif', 'size': 24,
         'bold': False, 'italic': False, 'antialias': True, 'color': [255, 255, 255],
         'border_color': [10, 255, 0], 'border_r': 2, 'back_color': [30, 150, 110]},
        {'name': 'serif', 'size': 21,
         'bold': False, 'italic': False, 'antialias': True, 'color': [255, 255, 255],
         'border_color': [50, 255, 0], 'border_r': 2, 'back_color': [100, 140, 100]}
    ],
    'CheckBox': [
        {'border_color': [0, 255, 0], 'border_r': 2, 'back_color': [14, 129, 94]},
        {'border_color': [10, 255, 0], 'border_r': 2, 'back_color': [30, 150, 110]},
        {'border_color': [50, 255, 0], 'border_r': 4, 'back_color': [100, 140, 100]},
        {'border_color': [0, 255, 0], 'border_r': 2, 'back_color': [14, 129, 94],
         'check_r': 3, 'check_color': [140, 240, 159]},
        {'border_color': [10, 255, 0], 'border_r': 2, 'back_color': [30, 150, 110],
         'check_r': 3, 'check_color': [200, 255, 189]},
        {'border_color': [50, 255, 0], 'border_r': 4, 'back_color': [100, 140, 100],
         'check_r': 3, 'check_color': [230, 225, 189]}
    ],
    'Element': [],
    'ChoiceBox': [{'name': 'serif', 'size': 24, 'bold': False, 'italic': False, 'antialias': True,
                   'color': [255, 255, 255], 'border_color': [0, 40, 110], 'border_r': 2, 'back_color': [0, 80, 94]},
                  {'name': 'serif', 'size': 24, 'bold': False, 'italic': False, 'antialias': True,
                   'color': [255, 255, 255], 'border_color': [0, 40, 130], 'border_r': 2, 'back_color': [0, 109, 104]},
                  {'name': 'serif', 'size': 24, 'bold': False, 'italic': False, 'antialias': True,
                   'color': [255, 255, 255], 'border_color': [0, 40, 110], 'border_r': 5, 'back_color': [0, 109, 104]}],
    'Input': [{'name': 'serif', 'size': 24, 'bold': False, 'italic': False, 'antialias': True,
               'color': [255, 255, 255], 'border_color': [190, 40, 110], 'border_r': 2, 'back_color': [84, 80, 94]},
              {'name': 'serif', 'size': 24, 'bold': False, 'italic': False, 'antialias': True,
               'color': [255, 255, 255], 'border_color': [210, 40, 130], 'border_r': 2, 'back_color': [54, 109, 104]},
              {'name': 'serif', 'size': 24, 'bold': False, 'italic': False, 'antialias': True,
               'color': [255, 255, 255], 'border_color': [190, 40, 110], 'border_r': 5, 'back_color': [54, 109, 104]}]
})


# array[father, suns, surf, pos, frame_array:list[frame_dict], frame_class, is_draw, is_listen,
#       dict(functions), listened]
# functions[mouse_click, mouse_attention, mouse_position]
class Element:
    def __init__(self, array):
        self.array = array
        self['father']['suns'].append(self)
        self['suns'] = []
        self['frame_class'] = Frames(self['frame_array'])
        self['theme'] = main_theme
        self['theme']['suns'].append(self)
        for i in range(min(len(self['frame_array']), len(self['theme'][self.__class__.__name__]))):
            self['frame_array'][i].update(self['theme'][self.__class__.__name__][i])
        if array.get('update'):
            self['frame_class'].set_pos(self['pos'])
            self['frame_class'].update_frames()
            self['surf'] = (~self)['frame'].copy()

    def __invert__(self):
        return self['frame_class'].get_frame()

    def draw(self):
        if self['is_draw']:
            self['surf'] = (~self)['frame'].copy()
            for sun in self['suns']:
                sun.draw()
            self['father']['surf'].blit(self['surf'], (~self)['pos'].position.lis())

    def listen(self):
        if self['is_listen']:
            self.clear_listened()
            for sun in self['suns']:
                sun.listen()
            mp = self.find_mouse()
            if self['pos'].in_area(mp):
                self['listened'].update({
                    'mouse_attention': True, 'mouse_position': mp.lis()})
            self['listened'].update({'mouse_click': pygame.mouse.get_pressed()[0]})

    def action(self):
        if self['is_listen']:
            for sun in self['suns']:
                sun.action()
        for key in self['functions']:
            self['functions'][key](self)

    def clear_listened(self):
        for key in self['listened']:
            self['listened'][key] = False

    def find_mouse(self):
        if self['surf'] is pygame.display.get_surface():
            return V(list(pygame.mouse.get_pos()))

        elif self['father'] is None:
            print('Нет дисплея')
            return [0, 0]

        else:
            return self['father'].find_mouse() - self['pos'].position

    def update_theme(self, theme):
        for i in range(min(len(self['frame_array']), len(theme[self.__class__.__name__]))):
            self['frame_array'][i].update(theme[self.__class__.__name__][i])
        self['frame_class'].update_frames()

    def __getitem__(self, item):
        return self.array[item]

    def __setitem__(self, key, value):
        self.array.update({key: value})


class Display(Element):
    def __init__(self, array):
        self.array = array
        self['surf'] = pygame.display.set_mode(array['pos'].size.lis())
        self['suns'] = []
        self['father'] = None

    def draw(self):
        self['surf'].fill(self['bg_color'])
        for sun in self['suns']:
            sun.draw()

    def listen(self):
        for sun in self['suns']:
            sun.listen()

    def action(self):
        for sun in self['suns']:
            sun.action()

    def step(self):
        self.listen()
        self.action()
        self.draw()


class Text(Element):
    def __init__(self, array, text):
        array.update({
            'update': True, 'is_listen': True, 'is_draw': True, 'listened': {}, 'functions': {},
            'frame_array': [{'fun': fun_text, 'text': text}],
        })
        super().__init__(array)


class Button(Element):

    def __init__(self, array, text):
        array.update({
            'update': True, 'is_listen': True, 'is_draw': True, 'listened': {},
            'functions': {'1': listen_button},
            'frame_array': [
                {'fun': fun_button, 'pos': array['pos'].copy(), 'text': text},
                {'fun': fun_button, 'pos': array['pos'].copy(), 'text': text},
                {'fun': fun_button, 'pos': array['pos'].copy().scale(0.9), 'text': text}
            ],
        })
        super().__init__(array)

    def set_click_action(self, fun):
        self['functions'].update({'click_action': fun})


class CheckBox(Element):
    def __init__(self, array, state=False):
        self.state = state

        array.update({
            'update': True, 'is_listen': True, 'is_draw': True, 'listened': {},
            'functions': {'1': listen_box},
            'frame_array': [
                {'fun': fun_off_box, 'border_color': [0, 255, 0], 'border_r': 2, 'back_color': [14, 129, 94]},
                {'fun': fun_off_box, 'border_color': [10, 255, 0], 'border_r': 2, 'back_color': [30, 150, 110]},
                {'fun': fun_off_box, 'border_color': [50, 255, 0], 'border_r': 4, 'back_color': [100, 140, 100]},
                {'fun': fun_on_box, 'border_color': [0, 255, 0], 'border_r': 2, 'back_color': [14, 129, 94],
                 'check_r': 3, 'check_color': [140, 240, 159]},
                {'fun': fun_on_box, 'border_color': [10, 255, 0], 'border_r': 2, 'back_color': [30, 150, 110],
                 'check_r': 3, 'check_color': [200, 255, 189]},
                {'fun': fun_on_box, 'border_color': [50, 255, 0], 'border_r': 4, 'back_color': [100, 140, 100],
                 'check_r': 3, 'check_color': [230, 225, 189]}
            ],
        })
        super().__init__(array)
        if self.state:
            self['frame_class'].current_frame = 3

    def get_information(self):
        return self.state


class Input(Element):
    def __init__(self, array, text="", data=int):
        self.data = data
        self.text = text
        self.state = False
        if data == int:
            self.re = r'[0-9]'
        elif data == float:
            self.re = r'[0-9.]'
        elif data == complex:
            self.re = r'[0-9.j]'
        else:
            self.re = r'[\w ,.]'

        def fun_input(frame_dict):
            s = pygame.font.SysFont(frame_dict.get('name'), frame_dict.get('size'),
                                    frame_dict.get('bold'), frame_dict.get('italic')).render(
                self.text, frame_dict.get('antialias'), frame_dict.get('color'))

            pos = frame_dict['pos'].copy()
            pos = Pos(pos.inner, pos.inner)
            pos.update()

            border = pygame.Surface(pos.size.lis())
            border.fill(frame_dict['border_color'])

            pos.inner -= V(frame_dict['border_r'], frame_dict['border_r'])
            pos.update()

            back = pygame.Surface(pos.size.lis())
            back.fill(frame_dict['back_color'])

            text_pos = Pos(pos.inner, V([i / 2 for i in s.get_size()]))

            back.blit(s, text_pos.position.lis())
            border.blit(back, pos.position.lis())
            return border

        def listen_input(element):
            if not self.state:
                if element['frame_class'].current_frame == 0:
                    if element['listened'].get('mouse_attention'):
                        if not element['listened'].get('mouse_click'):
                            element['frame_class'].current_frame = 1
                elif element['frame_class'].current_frame == 1:
                    if not element['listened'].get('mouse_attention'):
                        element['frame_class'].current_frame = 0
                    if element['listened'].get('mouse_click'):
                        element['frame_class'].current_frame = 2
                        self.state = True
            else:
                if element['listened'].get('mouse_click') and not element['listened'].get('mouse_attention'):
                    self.state = False
                    element['frame_class'].current_frame = 0

        array.update({
            'update': True, 'is_listen': True, 'is_draw': True, 'listened': {},
            'functions': {'1': listen_input},
            'frame_array': [
                {'fun': fun_input, 'pos': array['pos'].copy()},
                {'fun': fun_input, 'pos': array['pos'].copy()},
                {'fun': fun_input, 'pos': array['pos'].copy()}
            ]
        })

        super().__init__(array)

    def change_text(self, event):
        symbol = event.unicode
        if self.state:
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                self.state = False
                self['frame_class'].current_frame = 0

            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self['frame_class'].update_frames()

            if re.match(self.re, symbol):
                self.text += symbol
                self['frame_class'].update_frames()

    def get_information(self):
        if self.data == int or self.data == float or self.data == complex:
            if len(self.text) > 0:
                return self.data(self.text)
            else:
                return self.data(0)
        elif self.data == str:
            return self.text


class ChoiceBox(Element):
    def __init__(self, array, choice_dict):
        self.choice_dict = choice_dict
        self.current = 0
        self.state = False

        def fun_choice(frame_dict):
            keys = list(self.choice_dict)
            text = keys[self.current]
            if self.current == 0:
                text = '   ' + text + ' >'
            elif self.current == len(keys)-1:
                text = '< ' + text + '   '
            else:
                text = '< ' + text + ' >'

            s = pygame.font.SysFont(frame_dict.get('name'), frame_dict.get('size'),
                                    frame_dict.get('bold'), frame_dict.get('italic')).render(
                text, frame_dict.get('antialias'),
                frame_dict.get('color'))

            pos = frame_dict['pos'].copy()
            pos = Pos(pos.inner, pos.inner)
            pos.update()

            border = pygame.Surface(pos.size.lis())
            border.fill(frame_dict['border_color'])

            pos.inner -= V(frame_dict['border_r'], frame_dict['border_r'])
            pos.update()

            back = pygame.Surface(pos.size.lis())
            back.fill(frame_dict['back_color'])

            text_pos = Pos(pos.inner, V([i / 2 for i in s.get_size()]))

            back.blit(s, text_pos.position.lis())
            border.blit(back, pos.position.lis())
            return border

        def listen_choice(element):
            if not self.state:
                if element['frame_class'].current_frame == 0:
                    if element['listened'].get('mouse_attention'):
                        if not element['listened'].get('mouse_click'):
                            element['frame_class'].current_frame = 1
                elif element['frame_class'].current_frame == 1:
                    if not element['listened'].get('mouse_attention'):
                        element['frame_class'].current_frame = 0
                    if element['listened'].get('mouse_click'):
                        element['frame_class'].current_frame = 2
                        self.state = True
            else:
                if element['listened'].get('mouse_click') and not element['listened'].get('mouse_attention'):
                    self.state = False
                    element['frame_class'].current_frame = 0

        array.update({
            'update': True, 'is_listen': True, 'is_draw': True, 'listened': {},
            'functions': {'1': listen_choice},
            'frame_array': [
                {'fun': fun_choice, 'pos': array['pos'].copy()},
                {'fun': fun_choice, 'pos': array['pos'].copy()},
                {'fun': fun_choice, 'pos': array['pos'].copy()}
            ]
        })

        super().__init__(array)

    def change_choice(self, event):
        if self.state:
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                self.state = False
                self['frame_class'].current_frame = 0
            else:
                if event.key == pygame.K_RIGHT:
                    if self.current < len(self.choice_dict) - 1:
                        self.current += 1
                        self['frame_class'].update_frames()
                elif event.key == pygame.K_LEFT:
                    if self.current > 0:
                        self.current -= 1
                        self['frame_class'].update_frames()

    def get_information(self):
        return list(self.choice_dict.values())[self.current]


class Group:
    def __init__(self, array: dict):
        self.array = array
        self.state = False
        self.deactivate()

    def add_elements(self, array: dict):
        self.array.update(array)
        if self.state:
            self.activate()
        else:
            self.deactivate()

    def activate(self):
        self.state = True
        for key in self.array:
            self[key]['is_draw'] = True
            self[key]['is_listen'] = True

    def deactivate(self):
        self.state = False
        for key in self.array:
            self[key]['is_draw'] = False
            self[key]['is_listen'] = False

    def __getitem__(self, item):
        return self.array[item]

    def __setitem__(self, key, value):
        self.array.update({key: value})
