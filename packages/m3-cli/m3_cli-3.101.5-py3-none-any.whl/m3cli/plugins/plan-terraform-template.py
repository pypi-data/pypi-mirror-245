"""
The custom logic for the command m3 plan-terraform-template.
This logic is created to convert parameters from the Human readable format to
appropriate for M3 SDK API request.
"""


def create_custom_request(request):
    request.parameters['task'] = 'PLAN'
    if request.parameters.get('variables'):
        variables = request.parameters.pop('variables')
        value = list(variables.values())[0]
        if ',' in value:
            type = 'LIST'
            value = value.replace(' ', '').strip('][').split(',')
        elif '=' in value:
            type = 'MAP'
            temp = value.replace(' ', '').split('=')
            value = {temp[0]: temp[-1]}
        else:
            type = 'STRING'
        name = list(variables.keys())[0]
        request.parameters['variables'] = {
            name: {
                'type': type,
                'value': value,
                'sensitive': True,
                'name': name
            }
        }
    return request
