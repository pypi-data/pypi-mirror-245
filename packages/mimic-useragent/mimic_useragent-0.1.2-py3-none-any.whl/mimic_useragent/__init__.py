"""
Mimic user agent, permite generar un agente de usuario aleatorio o fijo segun
una seed dada.
"""

import random


def mimic_user_agent(seed=None):
    """
    Retorna un 'user_agent' aleatorio

    Argumentos:
        seed = int or None (default).

    Returns
        Retorna string con user agent aleatorio.
    """

    OS_PLATFORM = {
        "win": (
            "Windows NT 5.1",  # Windows XP
            "Windows NT 6.1",  # Windows 7
            "Windows NT 6.2",  # Windows 8
            "Windows NT 6.3",  # Windows 8.1
            "Windows NT 10.0",  # Windows 10
        ),
        "linux": (
            "X11; Linux",
            "X11; Ubuntu; Linux",
        )
    }
    OS_CPU = {
        "win": (
            "x86",  # 32bit
            "Win64; x64",  # 64bit
            "WOW64",  # 32bit process on 64bit system
        ),
        "linux": (
            "i686",  # 32bit
            "x86_64",  # 64bit
            "i686 on x86_64",  # 32bit process on 64bit system
        )
    }

    USER_AGENT = (
        'Mozilla/5.0 (None; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Mozilla/5.0 (None; rv:104.0) Gecko/20100101 Firefox/104.0',
        'Mozilla/5.0 (None; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Mozilla/5.0 (None; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Mozilla/5.0 (None; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Mozilla/5.0 (None; rv:108.0) Gecko/20100101 Firefox/108.0',
        'Mozilla/5.0 (None; rv:109.0) Gecko/20100101 Firefox/109.0',
        'Mozilla/5.0 (None; rv:110.0) Gecko/20100101 Firefox/110.0',
        'Mozilla/5.0 (None; rv:111.0) Gecko/20100101 Firefox/111.0',
        'Mozilla/5.0 (None; rv:112.0) Gecko/20100101 Firefox/112.0',
        'Mozilla/5.0 (None; rv:113.0) Gecko/20100101 Firefox/113.0',
        'Mozilla/5.0 (None; rv:114.0) Gecko/20100101 Firefox/114.0',
    )

    random.seed(seed)

    os_plat = random.choice(list(OS_PLATFORM.keys()))
    os_choice = random.choice(OS_PLATFORM[os_plat])
    cpu = random.choice(OS_CPU[os_plat])

    if os_plat == "win":
        user_agent = random.choice(USER_AGENT).replace(
                                                "None", f'{os_choice}; {cpu}'
                                                )
    else:
        user_agent = random.choice(USER_AGENT).replace(
                                                "None", f'{os_choice}; {cpu}'
                                                )

    return user_agent
