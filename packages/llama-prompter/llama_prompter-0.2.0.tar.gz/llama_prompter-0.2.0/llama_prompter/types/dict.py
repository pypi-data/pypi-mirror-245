import json

from typing import Optional, TypeVar, get_args, get_origin

from llama_prompter.types.base import TypeHandler, composed_name, type_name

T = TypeVar("T")


def dict_parser(payload: str, type_: type[T]) -> tuple[Optional[T], int]:
    d, i = json.JSONDecoder().raw_decode(payload)
    return type_(**d), i


TypeHandler(
    lambda x: get_origin(x) == dict,
    composed_name,
    lambda x: (kv := f'{type_name(get_args(x)[0])} ":" {type_name(get_args(x)[1])}', f'"{{" ({kv} ("," {kv})*)? "}}"')[-1],
    lambda x: (kv := f'{type_name(get_args(x)[0])} ":" {type_name(get_args(x)[1])}', f'"{{" ({kv} ("," {kv})*)? "}}"')[-1],
    dict_parser,
    get_args=lambda x: [z for z in get_args(x)],
)
