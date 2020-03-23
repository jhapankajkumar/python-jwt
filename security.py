from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'pankaj', 'asdf'),
    User(2, 'jyoti', 'abcd')
]

user_table = {u.username: u for u in users}
user_id_table = {u.id: u for u in users}


def authenticate(username, password):
    user = user_table.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return user_id_table.get(user_id, None)