
# ---------------------------------------------------------
# вн.сервис отобразить список строкой
def list_str(listing: any, sep=', ') -> str:
    string = ''
    if not listing: return ''
    for item in listing:
        string += str(item) + sep
    return string[:-len(sep)]
