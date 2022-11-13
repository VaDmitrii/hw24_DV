import os
import re
from json import JSONDecodeError
from typing import Generator, Iterator, List, Optional, Union

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_data(file_name: str) -> Generator:
    """Check file_name in data directory and read the file"""

    try:
        with open(f'{DATA_DIR}/{file_name}', 'r', encoding='utf-8') as file:
            for row in file:
                yield row
    except (FileNotFoundError, JSONDecodeError):
        return 'No such file in directory', 400


def regex(data: Iterator, reg_exp: str) -> Iterator:
    """Filter data by regular expression"""

    return filter(lambda line: re.search(f'{reg_exp}', line), data)


def filter_data(data: Iterator, value: Optional[str]) -> Iterator:
    """Filter data by value"""

    return filter(lambda l: value in l, data)


def map_data(data: Iterator, value: Union[str, int]) -> Iterator:
    """Split data byt space and return the value column"""

    map_value = int(value)
    return map(lambda l: l.split(' ')[map_value], data)


def limit_result(data: Union[Generator, Iterator], limit_value: str) -> List[str]:
    """Return limited by limit_value number of lines"""

    int_limit = int(limit_value)
    return list(data)[:int_limit]


def result_data(file_name: str, commands_dict: dict) -> Iterator:
    """Receive data and process it depending on the request
    commands and values and return processing result"""

    result: Iterator = load_data(file_name=file_name)
    if 'filter' in commands_dict.keys():
        result = filter_data(result, commands_dict.get('filter'))

    if 'map' in commands_dict.keys():
        result = map_data(result, commands_dict.get('map'))

    if 'regex' in commands_dict.keys():
        result = regex(result, commands_dict.get('regex'))

    if 'sort' in commands_dict.keys():
        if commands_dict['sort'] == 'desc':
            result = sorted(list(result), reverse=True)
        else:
            result = sorted(list(result))

    if 'limit' in commands_dict.keys():
        result = limit_result(result, commands_dict.get('limit'))
    elif "unique" in commands_dict.keys():
        result = list(set(result))
    return result
