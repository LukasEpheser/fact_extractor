def make_bytes(code):
    if isinstance(code, bytes):
        return code
    elif isinstance(code, str):
        return code.encode('utf-8')
    else:
        return bytes(code)


def make_unicode_string(code):
    if isinstance(code, str):
        return code.encode(errors='replace').decode()
    elif isinstance(code, bytes):
        return code.decode(errors='replace')
    else:
        return code.__str__()


def remove_uneccessary_spaces(input_string):
    tmp = input_string.split()
    tmp = ' '.join(tmp)
    return tmp
