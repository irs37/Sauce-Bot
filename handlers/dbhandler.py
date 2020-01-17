from tinydb import TinyDB, Query
import handlers.model as model

line_db = TinyDB('line_db.json')
user_ref = line_db.table('users')
group_ref = line_db.table('groups')
Search = Query()

u_id = 'U2e91a820fc12fa78c55ded8731cd3698'


def set_user(user_id):
    from handlers.lineHandler import get_profile
    temp = get_profile(user_id)
    user = model.User(user_id=temp.user_id, name=temp.display_name)
    user_ref.insert(user.to_dict())


def set_user_name(user_id):
    from handlers.lineHandler import get_profile
    temp = get_profile(user_id)
    user_ref.update({'name': temp.display_name}, Search.user_id == temp.user_id)


def set_group(group_id, user_id=None):
    if not user_ref.contains(Search.user_id == user_id) and user_id is not None:
        set_user(user_id)
    group = model.Group(group_id=group_id)
    group_ref.insert(group.to_dict())


def set_group_user(group_id, user_id):
    temp = get_group_users(group_id)
    if user_id in temp:
        return
    else:
        temp.append(user_id)
        group_ref.update({'users': temp}, Search.group_id == group_id)


def set_user_mode(user_id, mode: model.Mode):
    user_ref.update({'mode': mode.value}, Search.user_id == user_id)


def set_group_mode(group_id, mode: model.Mode):
    group_ref.update({'mode': mode.value}, Search.group_id == group_id)


def set_user_last_img(user_id, img):
    user_ref.update({'last_img': img}, Search.user_id == user_id)


def set_user_glast_img(user_id, img):
    user_ref.update({'glast_img': img}, Search.user_id == user_id)


def set_group_last_img(user_id, group_id, img):
    set_user_glast_img(user_id, img)
    group_ref.update({'last_img': img}, Search.group_id == group_id)


def get_user_mode(user_id):
    return user_ref.get(Search.user_id == user_id)['mode']


def get_group_mode(group_id):
    return group_id.get(Search.group_id == group_id)['mode']


def get_user_last_img(user_id):
    return user_ref.get(Search.user_id == user_id)['last_img']


def get_user_glast_img(name):
    return user_ref.get(Search.name == name)['glast_img']


def get_group_last_img(group_id):
    return group_id.get(Search.group_id == group_id)['last_img']


def get_group_users(group_id):
    return group_ref.get(Search.group_id == group_id)['users']
