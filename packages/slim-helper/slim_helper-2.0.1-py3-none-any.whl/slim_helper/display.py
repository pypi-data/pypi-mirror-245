import math


def si_prefix(value: float | int) -> tuple[int, str, str]:
    r"""convert number to SI metric prefix

    Args:
        value (float|int): value
    Returns:
        tuple[int,str,str]: converted_value,symbol,name
    """

    if 1 < abs(value) < 10:
        return value, "", ""
    SI_P = (
        (30, "Q", "quetta"),
        (27, "R", "ronna"),
        (24, "Y", "yotta"),
        (21, "Z", "zetta"),
        (18, "E", "exa"),
        (15, "P", "peta"),
        (12, "T", "tera"),
        (9, "G", "giga"),
        (6, "M", "mega"),
        (3, "K", "kilo"),
        (2, "h", "hecto"),
        (1, "da", "deca"),
    )
    SI_N = (
        (-1, "d", "deci"),
        (-2, "c", "centi"),
        (-3, "m", "milli"),
        (-6, "µ", "micro"),
        (-9, "n", "nano"),
        (-12, "p", "pico"),
        (-15, "f", "femto"),
        (-18, "a", "atto"),
        (-21, "z", "zepto"),
        (-24, "y", "yocto"),
        (-27, "r", "ronto"),
        (-30, "q", "quecto"),
    )
    prefixes = None
    if abs(value) > 1:
        prefixes = SI_P
    else:
        prefixes = SI_N
    prefix = None
    for p in prefixes:
        prefix = p
        if abs(value) // (10 ** p[0]) > 0:
            break
    return value / (10 ** prefix[0]), prefix[1], prefix[2]


def iec_prefix(value: int) -> tuple[int, str, str]:
    r"""convert number to IEC metric prefix

    Args:
        value (int): value
    Returns:
        tuple[int,str,str]: converted_value,symbol,name
    """
    if value < 0:
        raise ValueError("IEC standard does not support negative value")
    if value < (2**10):
        return value, "", ""
    IEC_60027_2 = (
        (80, "Yi", "yobi"),
        (70, "Zi", "zebi"),
        (60, "Ei", "exbi"),
        (50, "Pi", "pebi"),
        (40, "Ti", "tebi"),
        (30, "Gi", "gibi"),
        (20, "Mi", "mebi"),
        (10, "Ki", "kibi"),
    )
    prefixes = IEC_60027_2
    prefix = None
    for p in prefixes:
        prefix = p
        if value // (2 ** p[0]) > 0:
            break
    return value / (2 ** prefix[0]), prefix[1], prefix[2]
