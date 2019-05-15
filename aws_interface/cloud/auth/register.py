
from cloud.crypto import *
from cloud.response import Response
import cloud.auth.get_email_login as get_email_login

# Define the input output format of the function.
# This information is used when creating the *SDK*.
info = {
    'input_format': {
        'email': 'str',
        'password': 'str',
        'extra': 'map'
    },
    'output_format': {
        'message': 'str',
    }
}


def do(data, resource):
    body = {}
    params = data['params']

    email = params['email']
    password = params['password']
    extra = params.get('extra', {})

    salt = Salt.get_salt(32)
    password_hash = hash_password(password, salt)

    partition = 'user'
    login_conf = get_email_login.do(data, resource)['body']['item']
    default_group_name = login_conf['default_group_name']
    enabled = login_conf['enabled']
    if enabled == 'true':
        enabled = True
    elif enabled == 'false':
        enabled = False

    if not enabled:
        body['error'] = '4'
        body['message'] = '이메일 로그인이 비활성화 상태입니다.'
        return Response(body)

    instructions = [
        (None, ('email', 'eq', email))
    ]
    items, end_key = resource.db_query(partition, instructions)
    users = list(items)
    if len(users) > 0:
        body['message'] = '이미 가입된 회원이 존재합니다.'
        body['error'] = '1'
        return Response(body)
    else:
        item = {
            'email': email,
            'passwordHash': password_hash,
            'salt': salt,
            'groups': [default_group_name],
            'loginMethod': 'email_login',
        }
        # Put extra value in the item
        for key in extra:
            if key not in item:
                item[key] = extra[key]
        resource.db_put_item(partition, item)
        body['message'] = '회원가입에 성공하였습니다.'
        return Response(body)
