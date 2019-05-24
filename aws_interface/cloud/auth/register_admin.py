
from cloud.crypto import *
from cloud.response import Response
from cloud.permission import Permission, NeedPermission
from cloud.message import Error


# Define the input output format of the function.
# This information is used when creating the *SDK*.
info = {
    'input_format': {
        'email': 'str',
        'password': 'str',
        'extra': 'map'
    },
    'output_format': {
        'error?': {
            'code': 'int',
            'message': 'str',
        }
    }
}


@NeedPermission(Permission.Run.Auth.register_admin)
def do(data, resource):
    body = {}
    params = data['params']

    email = params['email']
    password = params['password']
    extra = params.get('extra', {})

    salt = Salt.get_salt(32)
    password_hash = hash_password(password, salt)

    partition = 'user'
    default_group_name = 'admin'

    instructions = [
        (None, ('email', 'eq', email))
    ]
    items, end_key = resource.db_query('user', instructions)
    users = items
    if len(users) > 0:
        body['error'] = Error.existing_account
        return Response(body)
    else:
        item = {
            'email': email,
            'password_hash': password_hash,
            'salt': salt,
            'group': default_group_name,
            'extra': extra,
            'login_method': 'email_login',
        }
        resource.db_put_item(partition, item)
        return Response(body)
