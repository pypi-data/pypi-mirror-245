from typing import Any, Optional, TypeVar, get_args, get_origin

from llama_prompter.types.base import Type, TypeHandler, composed_name, type_name

T = TypeVar("T")


def _tuple_parser(payload: str, type_: type[T]) -> tuple[Optional[T], int]:
    start = 1  # skip first "["
    result: list[Any] = []
    for arg_type in get_args(type_):
        if start >= len(payload):
            return None, 0
        arg, i = Type(arg_type).parse(payload[start:])
        if arg is None:
            return None, 0
        result.append(arg)
        start += i + 1  # skip comma ","
    return tuple(result), start  # type: ignore


TypeHandler(
    lambda x: get_origin(x) == tuple,
    composed_name,
    lambda x: '"[" ' + ' "," '.join([type_name(a) for a in get_args(x)]) + ' "]"',
    lambda x: '"[" ' + ' "," '.join([type_name(a) for a in get_args(x)]) + ' "]"',
    _tuple_parser,
    get_args=lambda x: [z for z in get_args(x)],
)
