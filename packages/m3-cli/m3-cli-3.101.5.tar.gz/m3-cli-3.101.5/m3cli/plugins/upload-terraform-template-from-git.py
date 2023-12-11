"""The custom logic for the command m3 upload-terraform-template-from-git."""
import json


def create_custom_request(request):
    parameters = request.parameters
    approval_params = ['reviewers', 'approvalRule']
    approval_values = [p for p in approval_params
                       if request.parameters.get(p) is not None]
    approval_len = len(approval_values)
    if approval_len != 0:
        if approval_len != len(approval_params):
            raise AssertionError(
                'Parameters: "--approver", "--approval-policy '
                'are required if the template needs review')
        request.parameters['needReview'] = True
    parameters['gitUsername'] = 'TOKEN'
    return request


def create_custom_response(request, response):
    try:
        response = json.loads(response)
    except json.decoder.JSONDecodeError:
        return response

    if response.get('success'):
        return 'Specified template was successfully uploaded'

    error_message = response.get('errorMessage')
    if error_message:
        return f'Some error happened during template uploading,' \
               f' reason - {error_message}'

    return response
