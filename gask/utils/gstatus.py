status_codes = {
    0: 'active',
    1: 'on hold',
    2: 'dead'
}


def status_code_text(**kwargs):
    if 'property' in kwargs:
        if kwargs['property'] == 'status':
            return status_codes[kwargs['value']]
        return kwargs['value']


def status_code_key(**kwargs):
    if 'property' in kwargs:
        if kwargs['property'] == 'status':
            for key in status_codes:
                if status_codes[key] == kwargs['value']:
                    return key
    return None
