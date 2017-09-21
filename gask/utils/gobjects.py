import datetime
import ast
from .gutils import parse_time


class GProject(object):
    def __init__(self, **kwargs):
        parameters = [
            'id', 'title', 'status', 'description', 'created_at', 'gasks', 'issues',
            'threads', 'owner', 'teams'
        ]

        self.gask_objects = []
        self.issue_objects = []
        self.thread_objects = []

        if 'data' in kwargs:
            data = kwargs['data']
            self.id = data['id']
            self.title = data['title']
            self.status = data['status']
            self.description = data['description']
            self.created_at = datetime.datetime.strptime(
                data['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
            self.gasks = data['gasks']
            self.issues = data['issues']
            self.threads = data['threads']
            self.owner = data['owner']
            self.teams = data['teams']

        elif (parameter in kwargs for parameter in parameters):
            self.id = kwargs['id']
            self.title = kwargs['title']
            self.status = kwargs['status']
            self.description = kwargs['description']
            self.created_at = datetime.datetime.strptime(
                kwargs['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
            self.gasks = kwargs['gasks']
            self.issues = kwargs['issues']
            self.threads = kwargs['threads']
            self.owner = kwargs['owner']
            self.teams = kwargs['teams']

        else:
            raise TypeError("parameters don't match")

    def get_children(self):
        return self.gask_objects + self.issue_objects + self.thread_objects

    def __str__(self):
        return self.title


class GUser(object):
    def __init__(self, **kwargs):
        if 'data' in kwargs:
            data = kwargs.get('data')
        else:
            raise ValueError
        self.id = data.get('id', None)
        self.username = data.get('username', None)
        self.first_name = data.get('first_name', None)
        self.last_name = data.get('last_name', None)
        self.time_entries = data.get('time_entries', None)
        self.email = data.get('email', None)
        self.last_time_entry = None
        if not self.id or not self.username:
            raise ValueError('Missing id or username, corrupted data')

    def get_time_entries(self):
        return self.time_entries


class GTimeEntry(object):
    def __init__(self, **kwargs):
        if 'data' in kwargs:
            data = kwargs.get('data')
        else:
            raise ValueError
        try:
            self.id = data['id']
        except KeyError:
            raise ValueError('No id provided')
        self.start_time = data['start_time']
        self.end_time = data['end_time']
        self.parent = data['parent']


class GObject(object):
    def __init__(self, *args, **kwargs):
        parameters = [
            'id', 'title', 'status', 'description', 'created_at', 'gasks',
            'issues', 'threads', 'owner', 'project'
        ]

        self.gask_objects = []
        self.issue_objects = []
        self.thread_objects = []

        if 'data' in kwargs:
            data = kwargs['data']
            self.id = data['id']
            self.title = data['title']
            self.status = data['status']
            self.description = data['description']
            self.created_at = datetime.datetime.strptime(
                data['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
            self.gasks = data['gasks']
            self.issues = data['issues']
            self.threads = data['threads']
            self.owner = data['owner']
            self.project = data['project']

        elif (parameter in kwargs for parameter in parameters):
            self.id = kwargs['id']
            self.title = kwargs['title']
            self.status = kwargs['status']
            self.description = kwargs['description']
            self.created_at = datetime.datetime.strptime(
                kwargs['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
            self.gasks = kwargs['gasks']
            self.issues = kwargs['issues']
            self.threads = kwargs['threads']
            self.owner = kwargs['owner']
            self.project = kwargs['project']

        else:
            raise TypeError('Parameters are wrong')

    def __str__(self):
        return self.title

    def get_children(self):
        return self.gask_objects + self.issue_objects + self.thread_objects


class GGask(GObject):

    def __init__(self, *args, **kwargs):
        GObject.__init__(self, *args, **kwargs)
        parameters = ['time_entries', 'deadline']
        if 'data' in kwargs:
            data = kwargs['data']
            self.time_entries = data['time_entries']
            self.deadline_datetime = data['deadline']
            self.deadline = None
            if self.deadline_datetime is not None:
                deadline_str = str(self.deadline_datetime)
                self.deadline_datetime = datetime.datetime.strptime(deadline_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                self.deadline = self.deadline_datetime.strftime("%d/%m/%Y %H:%M:%S")

        elif (parameter in kwargs for parameter in parameters):
            self.time_entries = kwargs['time_entries']
            self.deadline_datetime = kwargs['deadline']
            self.deadline = None
            if self.deadline_datetime is not None:
                deadline_str = str(self.deadline_datetime)
                self.deadline_datetime = datetime.datetime.strptime(deadline_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                self.deadline = self.deadline_datetime.strftime("%d/%m/%Y %H:%M:%S")

        else:
            raise TypeError("parameters don't match")

    def __str__(self):
        return self.title

    def list(self):
        return self.gask_objects + self.issue_objects + self.thread_objects


class GIssue(GObject):

    def __init__(self, *args, **kwargs):
        GObject.__init__(self, *args, **kwargs)

    def __str__(self):
        return self.title

    def list(self):
        return self.gask_objects + self.issue_objects + self.thread_objects


class GThread(GObject):

    def __init__(self, *args, **kwargs):
        GObject.__init__(self, *args, **kwargs)

    def list(self):
        return self.gask_objects + self.issue_objects + self.thread_objects

    def __str__(self):
        return self.title


def create_gobject_data(prefix='', object_name='', enter_function=None,
                        color=None, indent=None, object_id=None,
                        object_title=None, object_type=None,
                        type_=None, project_id=None, scrollable=True):

    if type_ == 'root':
        if object_type == 'GGask':
            color = 'blue'
            object_name = 'G: ' + object_name
        elif object_type == 'GIssue':
            color = 'red'
            object_name = '𐐤: ' + object_name
        elif object_type == 'GThread':
            color = 'purple'
            object_name = 'T: ' + object_name
        elif object_type == 'GProject':
            color = 'green'
            object_name = 'Π: ' + object_name
    else:
        if object_type == 'GGask':
            color = 'blue'
        elif object_type == 'GIssue':
            color = 'red'
        elif object_type == 'GThread':
            color = 'purple'
        elif object_type == 'GProject':
            color = 'green'

        if type_ == 'status':
            object_name = 'S: ' + object_name
        elif type_ == 'description':
            object_name = 'D: ' + object_name
        elif type_ == 'id':
            object_name = 'ID: ' + object_name
        elif type_ == 'deadline':
            object_name = '⏳: ' + object_name
        elif type_ == 'created_at':
            object_name = '⏰: ' + object_name
        elif type_ == 'time_entries':
            time_entries = object_name
            days, hours, mins, secs = time_entries_delta(time_entries)

            days_str = ''
            if days > 0:
                days_str = str(days) + ' days '
            hours_str = ''
            if hours > 0:
                hours_str = str(hours) + ' hours '
            mins_str = ''
            if mins > 0:
                mins_str = str(mins) + ' minutes '
            secs_str = str(secs) + ' seconds'

            object_name = 'TS: ' + days_str + hours_str + mins_str + secs_str

    gobject_data = {
        'prefix': prefix + ' ',
        'entry': object_name,
        'function': enter_function,
        'color': color,
        'indent': indent,
        'scrollable': scrollable,
        'ids': {
            'object_id': object_id,
            'object_name': object_title,
            'object_type': object_type,
            'type': type_,
            'project_id': project_id,
        }
    }
    return gobject_data


def time_entries_delta(time_entries):
    try:
        time_entries = ast.literal_eval(time_entries)
    except ValueError:
        pass

    secs = 0
    for entry in time_entries:
        start_time = datetime.datetime.strptime(entry['start_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if entry['end_time'] is None:
            break

        end_time = datetime.datetime.strptime(entry['end_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        delta_time = end_time - start_time
        secs += delta_time.total_seconds()

    days, hours, mins, secs = parse_time(secs)
    return int(days), int(hours), int(mins), int(secs)


def post_object(session_manager, root_object, data, object_type):
    content_type = ''
    object_id = ''
    if root_object is not None:
        object_id = root_object.id
        if isinstance(root_object, GGask):
            content_type = 'gask'
        elif isinstance(root_object, GIssue):
            content_type = 'issue'
        elif isinstance(root_object, GThread):
            content_type = 'thread'
        elif isinstance(root_object, GProject):
            content_type = 'project'
        else:
            raise TypeError("object is not GObject")

    if 'content_type' not in data:
        data['content_type'] = content_type
    if 'object_id' not in data:
        data['object_id'] = object_id
    if data['content_type'] == 'project':
        data['content_type'] = ''
        data['object_id'] = ''

    r = session_manager.post(data=data, url_suffix='/' + object_type + '/')
    return r


def patch_object(session_manager, data, object_type, id_):
    r = session_manager.patch(data=data, url_suffix='/' + object_type + '/' + id_ + '/')
    return r


def delete_object(session_manager, data, object_type, id_):
    r = session_manager.delete(data=data, url_suffix='/' + object_type + '/' + id_ + '/')
    return r
