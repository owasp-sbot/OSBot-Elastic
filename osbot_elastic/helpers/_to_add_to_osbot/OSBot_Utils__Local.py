
def bytes_to_string(bytes, encoding='ascii'):
    if bytes:
        return bytes.decode(encoding=encoding)
    return ""

def sorted_set(target):
    if target:
        return sorted(set(target))
    return []
