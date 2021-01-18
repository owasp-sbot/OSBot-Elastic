
def bytes_to_string(bytes, encoding='ascii'):
    if bytes:
        return bytes.decode(encoding=encoding)
    return ""

def lower(target : str):
    if target:
        return target.lower()
    return ""

def sorted_set(target : object):
    if target:
        return sorted(set(target))
    return []

def trim(target : str):
    if target:
        return target.strip()
    return ""

def upper(target : str):
    if target:
        return target.upper()
    return ""
