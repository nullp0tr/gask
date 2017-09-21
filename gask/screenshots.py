from guiask import *
from gask.utils.gparser import parse
from gask.utils.gstatus import status_code_text
from gask.utils.gobjects import *
import gtree
from gask.utils.gcommands import *
from gask import session_manager



def update_project_screenshot(screen):
    projects = build_projects(session_manager.session_client, session_manager.url)
    screenshot = project_t_screenshot(projects, 'main_tree', children_property='get_children', detailed=False,
                                      headline='tree')
    screen.unload()
    screen.load(me_profile_screenshot(None))
    screen.load(screenshot)
    screen.paintframe()
    ids = screen.get_current_ids()
    obj = None
    if ids is not None:
        nested_ids = ids['ids']
        if nested_ids is not None:
            obj = nested_ids['obj']
    screen.updates('detail_tree', me_profile_screenshot(obj))


def _login(screen, username, password):
    request = session_manager.login(
        username=username, password=password, next_url='/gasks/')
    if request.status_code == 200:
        r = session_manager.session_client.get('http://127.0.0.1:8000/gasks/')
        if r.status_code == 200:
            update_project_screenshot(screen)
            return

        screenshot = login_screenshot()
        screen.unload()
        screen.load(screenshot)


def get_input_field():
    return TerminalInputListItem(name='Enter Command')


def login_screenshot():
    username_entry = {
        'entry': 'Username: ',
        'align_to_center': True,
        'has_input': True
    }
    password_entry = {
        'entry': 'Password: ',
        'align_to_center': True,
        'hidden': True,
        'has_input': True
    }

    headline_screenshot = HeadlineListScreenshot(name='headline_screenshot_1', headline='Gask',
                                                 font=gbigchar.big_square_char_font, scale=2,
                                                 list_entries=[username_entry, password_entry],
                                                 input_handler=login_input_handler, color='blue',
                                                 align_vertically=True)
    return headline_screenshot


def me_profile_screenshot(obj):
    me_profile = build_me_profile(session_manager.session_client, session_manager.url)
    days, hours, mins, secs = time_entries_delta(me_profile.time_entries)
    time_spent = ''
    if days > 0:
        time_spent += str(days) + ' days '
    if hours > 0:
        time_spent += str(hours) + ' hours '
    if mins > 0:
        time_spent += str(mins) + ' minutes '
    if secs > 0:
        time_spent += str(secs) + ' seconds'

    username = {
        'prefix': 'active usr ───↠ ',
        'entry': me_profile.username + '\n',
        'scrollable': False,
        'color': 'green2'
    }
    currently_working_on_color = 'red1'
    currently_working_on = str(me_profile.last_time_entry)
    if currently_working_on != 'noting..':
        currently_working_on_color = 'green2'
    last_time_entry = {
        'prefix': 'working on ───↠ ',
        'entry': str(me_profile.last_time_entry) + '\n',
        'scrollable': False,
        'color': currently_working_on_color
    }
    time_spent = {
        'prefix': 'time spent ───↠ ',
        'entry': time_spent + '\n',
        'scrollable': False,
        'color': 'green2'
    }

    obj_list = []
    if obj is not None:
        obj_list = [obj, ]

    profile_screenshot = project_t_screenshot(obj_list, 'detail_tree',
                                              detailed=True, scrollable=False,
                                              extras=[username, last_time_entry, time_spent])
    return profile_screenshot


def login_input_handler(**kwargs):
    try:
        char = kwargs['char']
        screenshot = kwargs['screenshot']
        selected_entry = kwargs['selected_entry']
        screen = kwargs['screen']
    except KeyError:
        raise ValueError("Proper arguments not received")

    if selected_entry is None:
        return
    ch = char
    current_input_field = screenshot.drawables[selected_entry]
    if ch == TKeys.ENTER_CR:
        screenshot.drawables[selected_entry].fulfilled = True
        screen.scrolldown()
        if selected_entry == 2:
            username = screenshot.drawables[selected_entry - 1].input
            password = screenshot.drawables[selected_entry].input
            _login(screen, username=username, password=password)

    elif ch == TKeys.CTRL_F:
        screen.scrolldown()

    elif ch == TKeys.CTRL_R:
        screen.scrollup()

    elif not current_input_field.fulfilled:
        current_input_field.addtodrawable(tobeadded=ch)
    else:
        pass


def project_t_screenshot(object_, screenshot_name, children_property=None, detailed=False, headline=None,
                         scrollable=True, extras=None):
    uniarrows = {0: '↠', 1: '⇀', 2: '⇁', 3: '⇢', 4: '→', 5: '⇒'}
    extra_children_properties = []
    if detailed:
        extra_children_properties = ['status', 'description', 'id', 'deadline', 'time_entries']

    t = gtree.tree(object_, children_property=children_property, extra_children_properties=extra_children_properties,
                   addtoprefix=lambda **kwargs: uniarrows[kwargs['level'] % 6], editfield=status_code_text)
    project_tree = []
    nonroot_objects_counter = 0
    node_extra_properties = []
    object_type = None
    if extras is not None:
        for extra in extras:
            project_tree.append(extra)
    for i, node in enumerate(t):
        prefix, _, obj = node
        type_ = None
        try:
            object_id = obj.id
            object_type = obj.__class__.__name__
            type_ = 'root'
            node_extra_properties.clear()
            for _, extra_property in enumerate(extra_children_properties):
                if hasattr(obj, extra_property):
                    node_extra_properties.append(extra_property)
            nonroot_objects_counter = 0
        except AttributeError:
            object_id = None

        try:
            project_id = obj.project
        except AttributeError:
            try:
                project_id = obj.id
            except AttributeError:
                project_id = None

        all_attrs = (len(node_extra_properties) == nonroot_objects_counter)
        if type_ is None and not all_attrs:
            type_ = node_extra_properties[nonroot_objects_counter]
            nonroot_objects_counter += 1

        gobject_data = create_gobject_data(prefix=prefix, object_name=str(obj), scrollable=scrollable,
                                           object_id=object_id, object_type=object_type,
                                           object_title=str(obj), type_=type_, project_id=project_id)
        gobject_data['ids']['obj'] = obj
        project_tree.append(gobject_data)

    if not project_tree:
        pass

    headline_screenshot = HeadlineListScreenshot(name=screenshot_name,
                                                 headline=headline, list_entries=project_tree, scale=1,
                                                 font=big_square_char_font, align_vertically=True,
                                                 input_handler=project_tree_input_handler, color='blue')
    return headline_screenshot


def project_tree_input_handler(**kwargs):
    try:
        ch = kwargs['char']
        identifiers = kwargs['ids']
        screen = kwargs['screen']
    except KeyError:
        raise ValueError("Proper arguments not received")

    if ch == TKeys.CTRL_R:
        if screen.screenshot_in_focus['highlighted'] is not None:
            screen.scrollup()
            ids = screen.get_current_ids()
            screen.updates('detail_tree', me_profile_screenshot(ids['ids']['obj']))

    elif ch == TKeys.CTRL_F:
        if screen.screenshot_in_focus['highlighted'] is not None:
            screen.scrolldown()
            ids = screen.get_current_ids()
            screen.updates('detail_tree', me_profile_screenshot(ids['ids']['obj']))

    elif TKeys.CTRL_A in ch:
        input_field = get_input_field()
        screen.screenshot_in_focus['screenshot'].append_drawable(input_field)

    elif TKeys.ENTER_CR == ch:
        args = input("Enter command: ")
        try:
            result = parse(args, identifiers)
        except ValueError as ex:
            input(ex)
            return

        if result is not None:
            method, object_type, data, id_ = result

            if method == 'post':
                r = post_object(session_manager, None, data, object_type)
                update_project_screenshot(screen)
            elif method == 'patch':
                r = patch_object(session_manager, data, object_type, str(id_))
                update_project_screenshot(screen)
            elif method == 'delete':
                r = delete_object(session_manager, None, object_type, str(id_))
                update_project_screenshot(screen)
        else:
            input('Not enough arguments')
