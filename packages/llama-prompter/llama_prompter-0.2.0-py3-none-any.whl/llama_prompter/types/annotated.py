from typing import Annotated, Optional, TypeVar, get_args, get_origin

from llama_prompter.types.base import TypeHandler, Type, composed_name

T = TypeVar("T")


def _annotated_ebnf(type_: type) -> str:
    orig_type, annotation = get_args(type_)
    if orig_type == str:
        for metadata in annotation.metadata:
            if hasattr(metadata, "pattern"):
                return r"~'\"" + str(metadata.pattern) + "\"'"
    assert False


def _annotated_gbnf(type_: type) -> str:
    orig_type, annotation = get_args(type_)
    if orig_type == str:
        for metadata in annotation.metadata:
            if hasattr(metadata, "pattern"):
                return '"\\"" (' + str(metadata.pattern) + ') "\\""'
    assert False


def _annotated_parser(payload: str, type_: type[T]) -> tuple[Optional[T], int]:
    return Type(get_args(type_)[0]).parse(payload)


TypeHandler(
    lambda x: get_origin(x) == Annotated,
    composed_name,
    _annotated_ebnf,
    _annotated_gbnf,
    _annotated_parser,
)
