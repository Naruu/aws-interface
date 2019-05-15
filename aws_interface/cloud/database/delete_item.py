
from cloud.response import Response
from cloud.util import has_write_permission, database_can_not_access_to_item

# Define the input output format of the function.
# This information is used when creating the *SDK*.
info = {
    'input_format': {
        'session_id': 'str',
        'item_id': 'str',
    },
    'output_format': {
        'success': 'bool',
        'message': 'str',
    }
}


def do(data, resource):
    body = {}
    params = data['params']
    user = data['user']

    item_id = params.get('item_id', None)

    item = resource.db_get_item(item_id)
    if database_can_not_access_to_item(item):
        body['success'] = False
        body['message'] = 'Database cannot access to system item'
        return Response(body)

    if has_write_permission(user, item):
        resource.db_delete_item(item_id)
        body['success'] = True
    else:
        body['success'] = False
        body['message'] = 'permission denied'
    return Response(body)
