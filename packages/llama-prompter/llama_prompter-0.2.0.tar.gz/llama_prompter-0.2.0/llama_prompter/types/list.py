from typing import Any, Optional, TypeVar, get_args, get_origin

from llama_prompter.types.base import Type, TypeHandler, composed_name, type_name

T = TypeVar("T")


def _list_parser(payload: str, type_: type[T]) -> tuple[Optional[T], int]:
    start = 1  # skip first "["
    result: list[Any] = []
    arg_type = get_args(type_)[0]
    while payload[start - 1] != "]":
        if start >= len(payload):
            return None, 0
        arg, i = Type(arg_type).parse(payload[start:])
        if arg is None:
            return None, 0
        result.append(arg)
        start += i + 1  # skip comma ","
    return list(result), start  # type: ignore


TypeHandler(
    lambda x: get_origin(x) == list,
    composed_name,
    lambda x: (arg := type_name(get_args(x)[0]), f'"[" ({arg} ("," {arg})*)? "]"')[-1],
    lambda x: (arg := type_name(get_args(x)[0]), f'"[" ({arg} ("," {arg})*)? "]"')[-1],
    _list_parser,
    get_args=lambda x: [z for z in get_args(x)],
)
