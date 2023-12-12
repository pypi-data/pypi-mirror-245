from typing import Annotated, Any, Union
from llama_prompter.types.base import Grammar, Type

import llama_prompter.types.base_types
import llama_prompter.types.list
import llama_prompter.types.tuple
import llama_prompter.types.dict
import llama_prompter.types.pydantic
import llama_prompter.types.annotated  # noqa: F401

__all__ = [
    "Grammar",
    "Type",
]

PrompterVarType = Union[type, Annotated[Any, ...]]
