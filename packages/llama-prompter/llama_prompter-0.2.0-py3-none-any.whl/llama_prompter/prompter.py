import re
import inspect

from typing import Any, Optional, Union
from llama_cpp.llama_grammar import LlamaGrammar

from llama_prompter.types import Grammar, PrompterVarType, Type

TEMPLATE_VAR_RE = re.compile(r"(?<!{){([a-zA-Z_]+):([^{}]*)}(?!})")


class Variable:
    def __init__(self, name: str, type_: PrompterVarType) -> None:
        self._name = name
        self._type = type_


def get_caller_symbols() -> tuple[dict[str, str], dict[str, str]]:
    frame = inspect.currentframe()
    if frame is None or frame.f_back is None or frame.f_back.f_back is None:
        raise Exception("Could not retrieve caller's symbols")
    return frame.f_back.f_back.f_globals, frame.f_back.f_back.f_locals


class Prompter:
    def __init__(self, template: str) -> None:
        self._prompt = ""
        self._sequences: list[Union[str, Variable]] = []
        caller_g, caller_l = get_caller_symbols()
        matches = [x for x in TEMPLATE_VAR_RE.finditer(template)]
        for i, m in enumerate(matches):
            if i == 0:
                self._prompt = template[0 : m.start(0)]  # noqa: E203
            else:
                self._sequences.append(template[matches[i - 1].end(0) : m.start(0)])  # noqa: E203
            type_ = eval(m[2], caller_g, caller_l)
            assert isinstance(type_, type)
            var = Variable(m[1], type_)
            self._sequences.append(var)
        if matches and matches[-1].end(0) < len(template):
            self._sequences.append(template[matches[-1].end(0) :])  # noqa: E203
        self._grammar = (
            LlamaGrammar.from_string(Grammar.GBNF.from_types([x._type if isinstance(x, Variable) else x for x in self._sequences]), verbose=False)
            if self._sequences
            else None
        )

    @property
    def prompt(self) -> str:
        return self._prompt

    @property
    def grammar(self) -> Optional[LlamaGrammar]:
        return self._grammar

    def decode_response(self, response: str) -> dict[str, Any]:
        variables: dict[str, Any] = {}
        start = 0
        for i in self._sequences:
            if isinstance(i, str):
                if not response[start:].startswith(i):
                    raise Exception("Could not decode")
                start += len(i)
            elif isinstance(i, Variable):
                obj, idx = Type(i._type).parse(response[start:])
                variables[i._name] = obj
                start += idx
        return variables
