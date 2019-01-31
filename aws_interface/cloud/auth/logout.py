from cloud.aws import *


def do(data, boto3):
    response = {}
    recipe = data['recipe']
    params = data['params']
    app_id = data['app_id']

    session_id = params.get('session_id', None)

    table_name = '{}-{}'.format(recipe['recipe_type'], app_id)

    dynamo = DynamoDB(boto3)
    dynamo.delete_item(table_name, 'session', session_id)
    response['message'] = '로그아웃 되었습니다.'
    return response
