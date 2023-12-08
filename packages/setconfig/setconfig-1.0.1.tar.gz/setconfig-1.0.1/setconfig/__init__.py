"""
Developed by Alex Ermolaev (Abionics)
Email: abionics.dev@gmail.com
License: MIT
"""

__version__ = '1.0.1'

from dataclasses import is_dataclass
from types import SimpleNamespace
from typing import TypeVar, Type, Any

import yaml
from dacite import from_dict
from pydantic import BaseModel

T = TypeVar('T')


def load_config(
        filename: str = 'config.yaml',
        data_class: Type[T] = None,
) -> T:
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
    return load_config_dict(data, data_class)


def load_config_stream(
        stream: Any,
        data_class: Type[T] = None,
) -> T:
    data = yaml.safe_load(stream)
    return load_config_dict(data, data_class)


def load_config_dict(
        data: dict,
        data_class: Type[T] = None,
) -> T:
    if data_class is None:
        return parse_simple(data)
    if is_dataclass(data_class):
        return from_dict(data_class, data)
    if issubclass(data_class, BaseModel):
        return data_class.model_validate(data)
    raise TypeError(f'Unsupported data class: {data_class}')


def parse_simple(data: Any) -> Any:
    if isinstance(data, dict):
        parsed = {
            key: parse_simple(value)
            for key, value in data.items()
        }
        return SimpleNamespace(**parsed)
    if isinstance(data, list | tuple):
        return data.__class__((
            parse_simple(item)
            for item in data
        ))
    return data
