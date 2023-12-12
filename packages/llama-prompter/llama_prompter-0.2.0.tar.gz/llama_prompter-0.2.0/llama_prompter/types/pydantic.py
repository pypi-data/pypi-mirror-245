from pydantic import BaseModel

from llama_prompter.types.base import TypeHandler, composed_name, type_name
from llama_prompter.types.dict import dict_parser


def _basemodel_bnf(type_: type) -> str:
    assert issubclass(type_, BaseModel)
    return '"{" ' + ' "," '.join([f'"\\"{n}\\":" {type_name(f.annotation)}' for n, f in type_.model_fields.items() if f.annotation]) + ' "}"'


def _basemodel_getargs(type_: type) -> list[type]:
    assert issubclass(type_, BaseModel)
    return [f.annotation for _, f in type_.model_fields.items() if f.annotation]


TypeHandler(
    lambda x: hasattr(x, "__subclasses__") and issubclass(x, BaseModel),
    composed_name,
    _basemodel_bnf,
    _basemodel_bnf,
    dict_parser,
    get_args=_basemodel_getargs,
)
