import curses

from json import load
from curses import panel

from collections import OrderedDict

def load_json():
    return load(open('./test.json'), object_pairs_hook=OrderedDict)

def calc_depth(tree, depth=0):
    result = OrderedDict()
    if hasattr(tree, '__iter__'):
        for node in tree:
            result.update({node: { 'depth': depth }})
            if isinstance(tree[node], dict):
                result.update(calc_depth(tree[node], depth+1))
            elif isinstance(tree[node], list):
                for item in tree[node]:
                    result.update(calc_depth(item, depth+1))
            else:
                result.update({node: { 'depth': depth, 'value': tree[node] }})
    else:
        result.update({tree: { 'depth': depth }})
    return result

def menu(screen):
    sub_win = screen.subwin(0,0)

    custom_panel = panel.new_panel(sub_win)
    custom_panel.hide()

    panel.update_panels()

    return custom_panel

def navigate(key, cur_pos, len_items):
    return {
        curses.KEY_UP: cur_pos - 1 > 0 and (cur_pos - 1),
        curses.KEY_BTAB: cur_pos - 1 > 0 and (cur_pos - 1),
        ord('\t'): cur_pos + 1 < len_items and (cur_pos + 1),
        curses.KEY_DOWN: cur_pos + 1 < len_items and (cur_pos + 1)
    }.get(key, cur_pos)

def print_menu(win, index, item, mode):
    (node, data) = item
    win.addstr(index+1, data.get('depth')+1, "{} {}".format(node, data.get('value', '')), mode)

def print_selected(win, selected):
    None

def display(pan, items):
    win = pan.window()
    win.box()
    win.keypad(True)

    pan.top()
    pan.show()

    position = 0

    while True:
        win.refresh()
        curses.doupdate()

        depths = calc_depth(items)

        for index, item in enumerate(depths.items()):
            mode = curses.A_REVERSE if index == position else curses.A_NORMAL
            print_menu(win, index, item, mode)

        key = win.getch()

        if key in [ ord('\n'), curses.KEY_ENTER ]:
            selected = depths[depths.keys()[position]]
            print selected.get('value', depths.keys()[position])

        position = navigate(key, position, len(depths))

        panel.update_panels()
        curses.doupdate()

def main(screen):
    curses.curs_set(0)
    display(menu(screen), load_json())

curses.wrapper(main)
