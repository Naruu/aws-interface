
from cloud.response import Response
from cloud.permission import Permission, NeedPermission
from cloud.message import error
from cloud.database.get_policy_code import match_policy_after_get_policy_code


# Define the input output format of the function.
# This information is used when creating the *SDK*.
info = {
    'input_format': {
        'session_id': 'str',
        'item': 'dict',
        'partition': 'str',
        'read_groups': 'list',
        'write_groups': 'list',
    },
    'output_format': {
        'error?': {
            'code': 'int',
            'message': 'str'
        }
    }
}


@NeedPermission(Permission.Run.Database.create_item)
def do(data, resource):
    body = {}
    params = data['params']
    user = data['user']

    user_id = user.get('id', None)

    partition = params.get('partition', None)
    item = params.get('item', {})
    read_groups = params.get('read_groups', [])
    write_groups = params.get('write_groups', [])

    read_groups = list(set(read_groups))
    write_groups = list(set(write_groups))

    item['read_groups'] = read_groups
    item['write_groups'] = write_groups
    item['owner'] = user_id
    # Check partition has been existed
    if resource.db_get_item(partition):
        if match_policy_after_get_policy_code(resource, 'create', partition, user, item):
            resource.db_put_item(partition, item)
            body['item_id'] = item.get('id', None)
            return Response(body)
        else:
            body['error'] = error.PERMISSION_DENIED
            return Response(body)

    body['error'] = error.NO_SUCH_PARTITION
    return Response(body)
