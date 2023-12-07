
SRTLEN = 16
IWLEN = 9

def iwPrint(srtname:str, *args, sep=' ', end='\n', file=None, level=None):
    """
    info Warning Print
    :param srtname: source name
    :param args:
    :param sep:
    :param end:
    :param file:
    :param level: None, 'info', 'warning'
    """
    srtname = f"[{srtname}]"
    level = level or 'info'
    iwmsc = f"[{level.upper()}]"
    # print(f'{srtname:^{SRTLEN}}{iwmsc:^{IWLEN}}', *args, sep=sep, end=end, file=file)  # 居中srtname和iwmsc
    print(f'{srtname:<{SRTLEN}}{iwmsc:<{IWLEN}}', *args, sep=sep, end=end, file=file)

def iPrint(srtname:str, *args, sep=' ', end='\n', file=None):
    iwPrint(srtname, *args, sep=sep, end=end, file=file, level='info')

def wPrint(srtname:str, *args, sep=' ', end='\n', file=None):
    iwPrint(srtname, *args, sep=sep, end=end, file=file, level='warning')

