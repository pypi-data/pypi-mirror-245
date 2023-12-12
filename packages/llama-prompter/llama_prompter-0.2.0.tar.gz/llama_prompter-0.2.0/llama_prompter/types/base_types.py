import re

from typing import Any, Callable, Optional, TypeVar

from llama_prompter.types.base import TypeHandler

T = TypeVar("T")


def _regex_parser(regex: str, cast: Callable[[str], Any]) -> Callable[[str, type[T]], tuple[Optional[T], int]]:
    r = re.compile(regex)

    def _parser_callback(payload: str, type_: type[T]) -> tuple[Optional[T], int]:
        m = r.match(payload)
        if not m:
            return None, 0
        return cast(m.group(1)), len(m.group(0))

    return _parser_callback


TypeHandler(
    bool,
    "boolean",
    r'"true" / "false"',
    '("true" | "false")',
    _regex_parser(r"(true|false)", lambda x: x == "true"),
)
TypeHandler(
    float,
    "float",
    r"~'-?[0-9]*(.[0-9]*)?'",
    '("-"? ([0-9]*) ("." [0-9]+))',
    _regex_parser(r"(\-?[0-9]*\.[0-9]+)", float),
)
TypeHandler(
    int,
    "integer",
    r"~'-?[0-9]+'",
    '("-"? ([0-9]+))',
    _regex_parser(r"(\-?[0-9]+)", int),
)
TypeHandler(
    str,
    "string",
    r"~'\"[0-9 a-z]*\"'i",
    '"\\"" ([^"\\\\] | "\\\\" (["\\\\/bfnrt] | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F]))* "\\""',
    _regex_parser(r'"((?:\\.|[^"\\])*)"', str),
)
