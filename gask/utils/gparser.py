from .gstatus import status_code_key
import datetime


def parse(args, ids):
    arguments = args.split(' ', 1)
    data = None
    if len(arguments) > 1:
        command_argument = arguments[0]
        rest = arguments[1]
        try:
            data = gask_commands[command_argument](rest, ids)
        except KeyError:
            raise ValueError('Command ' + command_argument + ' is not supported, did you make a typo?')
        except ValueError as ex:
            raise ValueError(str(ex))
    return data


def addparse(args, ids):
    object_types = ('gask', 'issue', 'project', 'thread')
    arguments = args.split(';;')
    arguments = [arg.strip(' ') for arg in arguments]
    arguments = [arg.split(' ', 1) for arg in arguments]

    title, description, status, deadline = side_arguments(arguments)
    object_type = arguments[0][0]
    if title is None:
        if object_type not in object_types:
            raise ValueError('added type ' + object_type + ' is not supported')
        elif len(arguments[0]) < 2:
            raise ValueError('not enough arguments were supplied')
        title = arguments[0][1]

    content_type = None
    object_id = None
    project_id = None
    if ids is not None:
        content_type = convert_object_type(ids['object_type'])
        object_id = ids['object_id']
        project_id = ids['project_id']
        content_type = content_type[:-1]

    if content_type == 'project':
        content_type = ''
        object_id = ''

    data = {'title': title, 'description': description, 'project': project_id, 'content_type': content_type,
            'object_id': object_id, 'status': status,}

    if object_type == 'gask':
        data['deadline'] = deadline

    object_type += 's'
    return 'post', object_type, data, object_id


def side_arguments(arguments):
    title = description = status = deadline = None
    for arg in arguments:
        if arg[0] == 'called':
            title = arg[1]
        elif arg[0] == 'is':
            description = arg[1]
        elif arg[0] == 'for':
            pass
        elif arg[0] == 'set':
            status = status_code_key(property='status', value=arg[1])
        elif arg[0] == 'rate':
            pass
        elif arg[0] == 'due':
            deadline = parse_due(arg[1])
    return title, description, status, deadline


def parse_due(arg):
    arguments = arg.split(' ')
    if arguments[0] == 'on':
        date = arguments[1]
        if date == 'the':
            date = arguments[2]

        d = datetime.datetime.strptime(date, '%d/%m/%Y')
        t = datetime.datetime.max.time()
        date = datetime.datetime.combine(d, t).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return date

    elif arguments[0] == 'next':
        pass
    elif arguments[0] == 'in':
        count = arguments[1]
        time_type = arguments[2]
        pass


def patchparse(args, ids):
    arguments = args.split(';;')
    arguments = [arg.strip(' ') for arg in arguments]
    arguments = [arg.split(' ', 1) for arg in arguments]

    title, description, status, deadline = side_arguments(arguments)
    data = dict(title=title, description=description, status=status)
    id_ = ids['object_id']
    object_type = ''

    if ids['object_type'] is None:
        pass
    else:
        object_type = convert_object_type(ids['object_type'])

    if object_type == 'gasks':
        data['deadline'] = deadline

    return 'patch', object_type, data, id_


def convert_object_type(object_type):
    if object_type == 'GGask':
        object_type_ = 'gasks'
    elif object_type == 'GProject':
        object_type_ = 'projects'
    elif object_type == 'GIssue':
        object_type_ = 'issues'
    elif object_type == 'GThread':
        object_type_ = 'threads'
    else:
        raise ValueError("Object Not Supported")
    return object_type_


def deleteparse(args, ids):
    if args == 'this for sure':
        object_type_ = convert_object_type(ids['object_type'])
        return 'delete', object_type_, None, ids['object_id']


def moveparse(args, ids):
    pass


def timeit(args, ids):
    arg = args.strip(' ')
    if arg == 'start':
        if ids['object_type'] == 'GGask':
            object_type_ = 'timed'
            data = {'parent': ids['object_id'], }
            return 'post', object_type_, data, None,
        raise ValueError(convert_object_type(ids['object_type']) + " don't have a deadline")
    elif arg == 'stop':
        object_type_ = 'me/?last_entry=true&'
        return 'patch', object_type_, None, ''
    else:
        raise ValueError("Wrong argument " + args + " received")


gask_commands = {
    'add': addparse,
    'patch': patchparse,
    'delete': deleteparse,
    'move': moveparse,
    'timed': timeit
}
