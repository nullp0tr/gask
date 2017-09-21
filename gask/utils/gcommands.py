from .gobjects import GGask, GTimeEntry, GUser, GProject, GThread, GIssue
import json


def build_me_profile(session, url):
    req = session.get(url + '/me/')
    profile_ = json.loads(req.text)
    profile = GUser(data=profile_)
    req = session.get(url + '/me/?last_entry=true&')
    last_entry_ = json.loads(req.text)
    try:
        last_entry_ = GTimeEntry(data=last_entry_)
    except ValueError:
        last_entry_ = None
    if last_entry_ is not None and last_entry_.end_time is None:
        req = session.get(url + '/gasks/' + str(last_entry_.parent))
        last_gask = json.loads(req.text)
        last_entry = last_gask['title']
        profile.last_time_entry = last_entry
        return profile
    profile.last_time_entry = 'noting..'
    return profile


def build_projects(session, url):
    req = session.get(url + '/projects/')
    projects_ = json.loads(req.text)
    projects = []
    for project_ in projects_:
        project = GProject(data=project_)
        for gask in project.gasks:
            req = session.get(url + '/gasks/' + str(gask))
            data = json.loads(req.text)
            gask_object = GGask(data=data)
            build_rgask_object(
                root_gask_object=gask_object, url=url, session=session)
            project.gask_objects.append(gask_object)

        for issue in project.issues:
            req = session.get(url + '/issues/' + str(issue))
            data = json.loads(req.text)
            issue_object = GIssue(data=data)
            build_rgask_object(
                root_gask_object=issue_object, url=url, session=session)
            project.issue_objects.append(issue_object)

        for thread in project.threads:
            req = session.get(url + '/threads/' + str(thread))
            data = json.loads(req.text)
            thread_object = GThread(data=data)
            build_rgask_object(
                root_gask_object=thread_object, url=url, session=session)
            project.thread_objects.append(thread_object)

        projects.append(project)
    return projects


# Root gask objects are issues, threads and gasks themselves
def build_rgask_object(root_gask_object, url, session):
    for gask in root_gask_object.gasks:
        prefix = '/gasks/'
        req = session.get(url + prefix + str(gask))
        data = json.loads(req.text)
        gask_object = GGask(data=data)
        build_rgask_object(
            root_gask_object=gask_object, url=url, session=session)
        root_gask_object.gask_objects.append(gask_object)

    for issue in root_gask_object.issues:
        prefix = '/issues/'
        req = session.get(url + prefix + str(issue))
        data = json.loads(req.text)
        issue_object = GIssue(data=data)
        build_rgask_object(
            root_gask_object=issue_object, url=url, session=session)
        root_gask_object.issue_objects.append(issue_object)

    for thread in root_gask_object.threads:
        prefix = '/threads/'
        req = session.get(url + prefix + str(thread))
        data = json.loads(req.text)
        thread_object = GThread(data=data)
        build_rgask_object(
            root_gask_object=thread_object, url=url, session=session)
        root_gask_object.thread_objects.append(thread_object)
