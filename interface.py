from tkinter import Tk, Canvas, LabelFrame, Frame, Scrollbar, StringVar, Entry, Scale, HORIZONTAL, \
    Radiobutton, Checkbutton, BooleanVar
from BTree import *
from random import randint
from copy import deepcopy
from tkinter.ttk import Combobox, Spinbox, Style, Label, Button
from tkinter.messagebox import showinfo


btree = BTree()
possible_degree = [3, 4, 5, 6, 7]

MAXVALUE = 9999
MINVALUE = -9999

xbox = 50
ybox = 20
xgap = 16
ygap = 50

number_of_cycle = 4
steps_in_cycle = 10
animation_speed = 640
pulse_step_speed = animation_speed // (number_of_cycle * steps_in_cycle)
canvas_text_size = 12

history = [(deepcopy(btree), [])]
history_pos = 0

actions_history = []


def create():
    global btree, actions_history
    btree = BTree(m=int(max_deg_combo.get()))
    actions_history = []
    history_update()
    show()


def history_update():
    global btree, history_pos, history
    if len(history) == history_pos - 1:
        history.append((deepcopy(btree), deepcopy(actions_history)))
        history_pos += 1
    else:
        history[history_pos + 1:] = [(deepcopy(btree), deepcopy(actions_history))]
        history_pos = len(history) - 1


def history_undo():
    global btree, history_pos, history, actions_history
    if history_pos:
        history_pos -= 1
        btree = deepcopy(history[history_pos][0])
        actions_history = deepcopy(history[history_pos][1])
        show()


def history_redo():
    global btree, history_pos, history, actions_history
    if len(history) > history_pos + 1:
        history_pos += 1
        btree = deepcopy(history[history_pos][0])
        actions_history = deepcopy(history[history_pos][1])
        show()


def show(t=None):
    t = get_tree(t)
    if t.get_root().have_any_keys() or t.get_root().have_any_child():
        generate_coordinates(t)
        canvas.delete('all')
        show_nodes(t)
    else:
        canvas.delete('all')


def get_tree(t=None):
    global btree
    if t is None:
        return btree
    return t


def generate_coordinates(t=None):
    t = get_tree(t)
    num_of_levels = t.get_height()
    all_nodes = t.get_all_nodes()
    max_h = num_of_levels * ybox + (num_of_levels - 1) * ygap
    max_w = (len(all_nodes[-1]) - 1) * xgap + sum([node.number_of_keys() * xbox for node in all_nodes[-1]])

    check_canvas_size(max_w, max_h)

    level_h = int(max_h / (num_of_levels - 1)) if num_of_levels > 1 else 0
    start_x = int(canvas.cget('width')) / 2 - max_w / 2
    start_y = int(canvas.cget('height')) / 2 + max_h / 2

    generate_coordinates_leaves(all_nodes[-1], start_x, start_y)
    generate_coordinates_parents(all_nodes[:-1], level_h)
    root.after(0, lambda: canvas.configure(scrollregion=canvas.bbox("all")))


def show_nodes(t):
    all_nodes = t.get_all_nodes()
    for row in all_nodes:
        for node in row:
            show_rectangle(node)
            show_text(node)
            show_branches(node)


def check_canvas_size(max_w, max_h):
    if max_h > int(canvas.cget('height')):
        canvas.config(height=max_h + 2*(ybox+ygap))
    if max_w > int(canvas.cget('width')):
        canvas.config(width=max_w + 2*(xbox+xgap))
    canvas_scroll_configure()


def generate_coordinates_leaves(level, start_x, start_y):
    for node in level:
        node.set_coordinates([
            start_x,
            start_y - ybox / 2,
            start_x + node.number_of_keys() * xbox,
            start_y + ybox / 2
        ])
        start_x = node.get_coordinate_xr() + xgap


def generate_coordinates_parents(all_parent_nodes, level_h):
    for level in reversed(all_parent_nodes):
        for parent in level:
            children_mid_x = get_middle_children_x_coordinate(parent)
            bottom_y = generate_parent_bottom_y(parent, level_h)
            x_deviation = parent.number_of_keys() * xbox / 2
            parent.set_coordinates([
                children_mid_x - x_deviation,
                bottom_y - ybox,
                children_mid_x + x_deviation,
                bottom_y
            ])


def show_rectangle(node: BTreeNode):
    coor = node.get_coordinates().values()
    if all(coor):
        canvas.create_rectangle(*coor)


def show_text(node: BTreeNode):
    if node.have_any_keys():
        text_gap = node.get_x_span() / (node.number_of_keys() * 2)
        start_x = node.get_coordinate_xl()

        for i, key in enumerate(node.get_keys()):
            canvas.create_text(
                start_x + text_gap + i * xbox,
                node.get_middle_y_coordinates(),
                font=("Pursia", canvas_text_size),
                text=key
            )


def show_branches(node: BTreeNode):
    for i, child in enumerate(node.get_children()):
        canvas.create_line(
            node.get_coordinate_xl() + i * xbox,
            node.get_middle_y_coordinates(),
            child.get_middle_x_coordinates(),
            child.get_coordinate_yu(),
        )


def canvas_scroll_configure():
    root.update()
    canvas.configure(scrollregion=canvas.bbox("all"))


def get_middle_children_x_coordinate(parent: BTreeNode):
    return (parent.get_first_child().get_coordinate_xl() + parent.get_last_child().get_coordinate_xr()) / 2


def generate_parent_bottom_y(parent, level_h):
    return parent.get_first_child().get_coordinate_yd() - level_h


def add():
    global btree
    if check_spinbox_value(add_sb):
        value = get_spinbox_value(add_sb)
        actions_history.append(lambda: btree.add_key(value))
        split_path = btree.add_key(value)
        run_animation(lambda: show_add(split_path))
        history_update()


def check_spinbox_value(spinbox):
    val = spinbox.get()
    try:
        val = int(val)
        if MINVALUE <= val <= MAXVALUE:
            return True
        else:
            show_info_window()
            return False
    except ValueError:
        show_info_window()
        return False


def run_animation(action):
    if is_animation_on():
        get_animation_speed()
        action()
    else:
        show(btree)


def is_animation_on():
    return animation_state.get()


def show_add(split_path):
    disable_all_buttons()
    root.after(0, show_path)
    root.after((len(btree.get_searching_path()) + 2) * animation_speed, lambda: show_split_path(split_path))
    root.after((len(btree.get_searching_path() + split_path) + 2) * animation_speed, show)
    root.after((len(btree.get_searching_path() + split_path) + 2) * animation_speed,
               enable_all_buttons)


def disable_buttons(button):
    for but in button:
        but['state'] = 'disabled'


def enable_buttons(button):
    for but in button:
        but['state'] = 'normal'


def get_animation_speed():
    global animation_speed, pulse_step_speed
    animation_speed = speed_s.get()
    pulse_step_speed = animation_speed // (number_of_cycle * steps_in_cycle)


def show_path():
    if is_animation_on() and btree.get_root().number_of_keys():
        show_path_util(0)


def show_path_util(n):
    searching_path = btree.get_searching_path()
    if n < len(searching_path):
        node = searching_path[n]
        if node.is_coordinates_set():
            change_node_color(node, '#ff0000')
            highlight_node_pulse(node)
            root.after(animation_speed, lambda: show_path_util(n + 1))


def highlight_node_pulse(node):
    coordinates = node.get_coordinates().values()
    highlight_node_pulse_expand(coordinates, 0, 1)


def highlight_node_pulse_expand(coordinates, cycle, i, colors=('#FFB9B9', '#FF0000')):
    if cycle < number_of_cycle:
        if i <= steps_in_cycle // 2:
            canvas.create_rectangle(
                *[coor-i if j < 2 else coor+i for j, coor in enumerate(coordinates)],
                outline=colors[0]
            )
            root.after(
                pulse_step_speed,
                lambda: highlight_node_pulse_expand(coordinates, cycle, i+1, colors)
            )
        else:
            root.after(
                pulse_step_speed,
                lambda: highlight_node_pulse_contract(coordinates, cycle, i, colors)
            )


def highlight_node_pulse_contract(coordinates, cycle, i, colors):
    if cycle < number_of_cycle:
        if i >= 1:
            canvas.create_rectangle(
                *[coor-i if j < 2 else coor+i for j, coor in enumerate(coordinates)],
                outline=colors[1]
            )
            root.after(pulse_step_speed, lambda: highlight_node_pulse_contract(coordinates, cycle, i-1, colors))
        else:
            root.after(pulse_step_speed, lambda: highlight_node_pulse_expand(coordinates, cycle+1, 1, colors))


def change_node_color(node, color):
    canvas.create_rectangle(*node.get_coordinates().values(), outline=color)


def show_split_path(split_path):
    if is_animation_on() and len(split_path) > 0:
        show_split_path_util(split_path, 0)


def show_split_path_util(split_path, n):
    if n < len(split_path):
        # split_path[n].show_complex_with_coordinates()
        show(split_path[n])
        root.after(speed_s.get(), lambda: show_split_path_util(split_path, n + 1))


def add_random():
    add_sb.set(randint(-100, 100))
    add()


def find():
    run_animation(lambda: show_find())


def show_find():
    if check_spinbox_value(find_sb):
        disable_all_buttons()

        node, i = btree.search(get_spinbox_value(find_sb))
        show_path()

        delay = (len(btree.searching_path) + 1) * animation_speed
        if i is not None:
            root.after(delay, lambda: highlight_key(node, i))
            delay += 2 * animation_speed

        delay += animation_speed
        root.after(delay, show)
        root.after(delay, enable_all_buttons)


def highlight_key(node, i):
    if node is not None and i < node.number_of_keys():
        coor = list(node.get_coordinates().values())
        coor[0] += i * xbox
        coor[2] = coor[0] + xbox
        # canvas.create_rectangle(*coor, outline='#00ff00')
        highlight_node_pulse_expand(coor, 0, 0, [ '#8BFF99', '#00C317'])


def clear():
    create()


def delete():
    if check_spinbox_value(delete_sb):
        value = get_spinbox_value(delete_sb)
        actions_history.append(lambda: btree.delete_key(value))
        btree.delete_key(value)
        run_animation(show_delete)
        history_update()


def show_delete():
    # btree.show_complex()
    disable_all_buttons()
    show_path()
    # root.after((len(btree.get_searching_path()) + 1) * animation_speed, lambda: show_split_path(split_path))
    root.after((len(btree.get_searching_path()) + 1) * animation_speed, show)
    root.after((len(btree.get_searching_path()) + 1) * animation_speed,
               enable_all_buttons)


def delete_all():
    if check_spinbox_value(delete_sb):
        value = get_spinbox_value(delete_sb)
        actions_history.append(lambda: btree.delete_all_keys(value))
        btree.delete_all_keys(value)
        run_animation(show_delete)
        history_update()


def get_spinbox_value(spinbox):
    if check_spinbox_value(spinbox):
        return int(spinbox.get())


def get_branch(node):
    pass  # TODO


def convert():
    global btree, actions_history
    btree = BTree(m=int(max_deg_combo.get()))
    for action in actions_history:
        action()
    history_update()
    show()


def zoom_in():
    global xbox, ybox, xgap, ygap, canvas_text_size
    if xbox < 100:
        xbox += 5
        ybox += 2
        xgap += 2
        ygap += 5
        canvas_text_size += 1
        show()


def zoom_out():
    global xbox, ybox, xgap, ygap, canvas_text_size
    if xbox > 30:
        xbox -= 5
        ybox -= 2
        xgap -= 2
        ygap -= 5
        canvas_text_size -= 1
        show()


def show_info_window():
    showinfo("Value error", f"The entered value must be an integer between {MINVALUE} and {MAXVALUE}")


def disable_all_buttons():
    all_buttons = [create_b, convert_b, undo_b, redo_b,
                   clear_b, add_b, delete_b, add_random_b,
                   delete_all_b, find_b, zoom_in_b, zoom_out_b]
    disable_buttons(all_buttons)


def enable_all_buttons():
    all_buttons = [create_b, convert_b, undo_b, redo_b,
                   clear_b, add_b, delete_b, add_random_b,
                   delete_all_b, find_b, zoom_in_b, zoom_out_b]
    enable_buttons(all_buttons)


# INTERFACE
root = Tk()
root.title('BTree')
root.geometry('1280x720')
root.resizable(False, False)
root.option_add('*Font', 'Arial 11')

# STYLE
root.style = Style()
# root.style.configure('TLabel', font=('Arial', '14', 'bold'))
# root.style.configure('Title.TLabel', padding=200)
root.style.configure('TButton', width=14, padding=(9, 2), cursor='man')
root.style.configure('TSpinbox', width=5)

# FRAMES
title_f = Frame(root)
menu_lf = LabelFrame(root, height=100, text='Menu')
canvas_lf = LabelFrame(root, text='Visualisation')

title_f.pack(fill='both', padx=20, pady=10)
menu_lf.pack(fill='x', padx=20, pady=0)
canvas_lf.pack(fill="both", padx=20, pady=20)

# TITLE
title_l = Label(title_f, text='BTree Visualisation', font=('Arial', '14', 'bold'))
title_l.pack(pady=(12, 2))

# MENU
# menu frames
menu_lf_subf = Frame(menu_lf)
menu_lf_subf.pack(fill='both', padx=10, pady=(4, 10))

frame_width = [365, 602, 176]
frame_height = 90

menu_lf_create = LabelFrame(
    menu_lf_subf,
    text='',
    width=frame_width[0],
    height=frame_height
)
menu_lf_actions = LabelFrame(
    menu_lf_subf,
    text='',
    width=frame_width[1],
    height=frame_height
)
menu_lf_animation = LabelFrame(
    menu_lf_subf,
    text='',
    width=frame_width[2],
    height=frame_height
)

menu_lf_create.pack(side='left', padx=10, pady=10, ipadx=5)
menu_lf_actions.pack(side='left', padx=10, pady=10, ipadx=5)
menu_lf_animation.pack(side='left', padx=10, pady=10, ipadx=5)

menu_lf_animation.grid_propagate(0)
menu_lf_actions.grid_propagate(0)
menu_lf_create.grid_propagate(0)

# menu create
max_deg_l = Label(menu_lf_create, text='Max Deg.')

max_deg = StringVar()
max_deg_combo = Combobox(menu_lf_create,  cursor='hand2', textvariable=max_deg, width=2)
max_deg_combo['state'] = 'readonly'
max_deg_combo['values'] = possible_degree
max_deg_combo['cursor'] = 'hand2'
max_deg_combo.set(possible_degree[0])

create_b = Button(menu_lf_create, text='Create New', command=create, cursor='hand2')
convert_b = Button(menu_lf_create, text='Convert', command=convert, cursor='hand2')
undo_b = Button(menu_lf_create, text='Undo', command=history_undo, cursor='hand2')
redo_b = Button(menu_lf_create, text='Redo', command=history_redo, cursor='hand2')
clear_b = Button(menu_lf_create, text='Clear All', command=clear, cursor='hand2')

max_deg_l.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))
max_deg_combo.grid(row=0, column=1, padx=(0, 5), pady=(10, 5))
create_b.grid(row=0, column=2, padx=(5, 5), pady=(10, 5))
convert_b.grid(row=0, column=3, padx=(5, 10), pady=(10, 5))
undo_b.grid(row=1, column=0, columnspan=2, padx=(10, 5), pady=(5, 10))
redo_b.grid(row=1, column=2, padx=(5, 5), pady=(5, 10))
clear_b.grid(row=1, column=3, padx=(5, 10), pady=(5, 10))


# menu actions
# buttons
add_b = Button(menu_lf_actions, text='Add', command=add, cursor='hand2')
delete_b = Button(menu_lf_actions, text='Delete', command=delete, cursor='hand2')
find_b = Button(menu_lf_actions, text='Find', command=find, cursor='hand2')
add_random_b = Button(menu_lf_actions, text='Add random', command=add_random, cursor='hand2')
delete_all_b = Button(menu_lf_actions, text='Delete All', command=delete_all, cursor='hand2')
zoom_in_b = Button(menu_lf_actions, text='Zoom in', command=zoom_in, cursor='hand2')
zoom_out_b = Button(menu_lf_actions, text='Zoom out', command=zoom_out, cursor='hand2')

# spinbox
add_sb_value = StringVar(value=0)
delete_sb_value = StringVar(value=0)
find_sb_value = StringVar(value=0)

add_sb = Spinbox(
    menu_lf_actions,
    from_=MINVALUE,
    to=MAXVALUE,
    textvariable=add_sb_value,
    width=11
)
delete_sb = Spinbox(
    menu_lf_actions,
    from_=MINVALUE,
    to=MAXVALUE,
    textvariable=delete_sb_value,
    width=11
)
find_sb = Spinbox(
    menu_lf_actions,
    from_=MINVALUE,
    to=MAXVALUE,
    textvariable=find_sb_value,
    width=11
)

# menu actions grid
add_b.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))
add_sb.grid(row=0, column=1, padx=5, pady=(10, 5))
add_random_b.grid(row=0, column=2, padx=5, pady=(10, 5))
find_b.grid(row=0, column=3, padx=5, pady=(10, 5))
find_sb.grid(row=0, column=4, padx=(5, 10), pady=(10, 5))
delete_b.grid(row=1, column=0, padx=(10, 5), pady=(5, 10))
delete_sb.grid(row=1, column=1, padx=5, pady=(5, 10))
delete_all_b.grid(row=1, column=2, padx=5, pady=(5, 10))
zoom_in_b.grid(row=1, column=3, padx=5, pady=(5, 10))
zoom_out_b.grid(row=1, column=4, padx=(5, 10), pady=(5, 10))

# menu animation
speed_l = Label(
    menu_lf_animation,
    text='Animation Speed',
    style='TLabel'
)
speed_s = Scale(
    menu_lf_animation,
    orient=HORIZONTAL,
    showvalue=False,
    from_=1600,
    to=40,
    resolution=40,
    cursor='hand2'
)
speed_s.set(animation_speed)

animation_state = BooleanVar(value=1)
animation_c = Checkbutton(
    menu_lf_animation,
    text='Animation',
    variable=animation_state,
    onvalue=True,
    offvalue=False,
    cursor='hand2'
)

speed_l.grid(row=0, column=0, padx=25, pady=(5, 0))
speed_s.grid(row=1, column=0, padx=25, pady=(2, 0))
animation_c.grid(row=2, column=0, padx=25, pady=(1, 7))

# CANVAS
canvas_f = Frame(canvas_lf)
canvas_f.pack(side="left", fill="both", padx=10, pady=10)

canvas = Canvas(canvas_f, borderwidth=0, bg='white', width=1200, height=413)

canvas_xscroll = Scrollbar(canvas_f, orient='horizontal', command=canvas.xview)
canvas_yscroll = Scrollbar(canvas_f, orient='vertical', command=canvas.yview)

canvas.configure(xscrollcommand=canvas_xscroll.set)
canvas.configure(yscrollcommand=canvas_yscroll.set)
canvas.configure(scrollregion=canvas.bbox("all"))

canvas_xscroll.pack(side='bottom', fill='x')
canvas_yscroll.pack(side='right', fill='y')
canvas.pack(side='left', fill='both', expand=True)


root.mainloop()
