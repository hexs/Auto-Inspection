import configparser
from typing import Union
from func.TextColor import *


def ini_str_to_python_variable(string: str) -> Union[str, int, float, list, dict, tuple, set]:
    try:
        return eval(string)
    except Exception as e:
        return string


def ini_str_to_python_variable_and_print(string: str):
    try:
        re_turn = eval(string)
        return f'{re_turn} {CYAN}{type(re_turn)}{ENDC}'
    except Exception as e:
        return YELLOW + string + ENDC


def dict_to_ini(d, filename):
    config = configparser.ConfigParser()
    for section, options in d.items():
        config[section] = options
    with open(filename, 'w') as configfile:
        config.write(configfile)


def ini_to_dict(filename, show=None):
    config = configparser.ConfigParser()
    config.read(filename)
    ini_dict = {}
    for section in config.sections():
        section_dict = {}
        for option in config.options(section):
            section_dict[option] = ini_str_to_python_variable(config.get(section, option))
        ini_dict[section] = section_dict
    if show:
        ini_dict_for_print = {}
        for section in config.sections():
            section_dict = {}
            for option in config.options(section):
                section_dict[option] = ini_str_to_python_variable_and_print(config.get(section, option))
            ini_dict_for_print[section] = section_dict
        for k, v in ini_dict_for_print.items():
            print(f'{k}')
            for kk, vv in v.items():
                print(f'    {kk:20}, {vv}')
    return ini_dict


d = {
    'd1': {
        'option1': 4,
        'option2': 5,
        'option3': 8,
        'option4': 9,
    },
    'd2': {
        'option1': 4,
        'option2': 5,
        'option3': 18,
        'option4': 19
    },
    'd3': {
        'option1': 4,
        'option2': 5,
        'option3': 18,
        'option4': 19
    }
}
intersec = set(d['d1'].items())
for k,v in d.items():
    intersec = intersec.intersection(set(v.items()))

print(dict(intersec))

