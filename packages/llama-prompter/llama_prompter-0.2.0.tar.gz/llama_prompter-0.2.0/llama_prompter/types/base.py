from enum import Enum, auto
from pydantic.fields import FieldInfo
from pydantic._internal._fields import PydanticGeneralMetadata
from typing import Any, Callable, Dict, Optional, TypeVar, Union, get_args, get_origin

T = TypeVar("T")


class Grammar(Enum):
    EBNF = auto()
    GBNF = auto()

    def rule(self, name: str, definition: str) -> str:
        if self == Grammar.EBNF:
            return f"{name} = {definition}"
        elif self == Grammar.GBNF:
            return f"{name} ::= {definition}"
        assert False

    def from_types(self, types_: list[Union[str, type]]) -> str:
        rules: dict[str, str] = {}

        def _rec_type_to_grammar(type_: type) -> str:
            basetype = Type(type_)
            if basetype.name in rules:
                return basetype.name
            rules[basetype.name] = basetype.definition(self)
            for arg in basetype.args:
                _rec_type_to_grammar(arg)
            return basetype.name

        rules["root"] = " ".join([_rec_type_to_grammar(x) if not isinstance(x, str) else f'"{x}"' for x in types_])
        return "\n".join([self.rule(n, r) for n, r in rules.items()])


class TypeHandler:
    _BASE_TYPES: dict[type, "TypeHandler"] = {}
    _COMPOSED_TYPES: list["TypeHandler"] = []

    @classmethod
    def get(cls, type_: type) -> Optional["TypeHandler"]:
        if type_ in cls._BASE_TYPES:
            return cls._BASE_TYPES[type_]
        for t in cls._COMPOSED_TYPES:
            if callable(t._type_match) and t._type_match(type_):
                return t
        return None

    def __init__(
        self,
        type_match: Union[type, Callable[[type], bool]],
        name: Union[str, Callable[[type], str]],
        ebnf: Union[str, Callable[[type], str]],
        gbnf: Union[str, Callable[[type], str]],
        parser: Callable[[str, type[T]], tuple[Optional[T], int]],
        get_args: Optional[Callable[[type], list[type]]] = None,
    ) -> None:
        self._type_match = type_match
        self._name = name
        self._ebnf = ebnf
        self._gbnf = gbnf
        self._parser = parser
        self._get_args = get_args
        if type(type_match) is type:
            self._BASE_TYPES[type_match] = self
        else:
            assert callable(type_match)
            self._COMPOSED_TYPES.append(self)

    def name(self, type_: type) -> str:
        return self._name(type_) if callable(self._name) else self._name

    def ebnf(self, type_: type) -> str:
        return self._ebnf(type_) if callable(self._ebnf) else self._ebnf

    def gbnf(self, type_: type) -> str:
        return self._gbnf(type_) if callable(self._gbnf) else self._gbnf

    def parse(self, payload: str, type_: type[T]) -> tuple[Optional[T], int]:
        return self._parser(payload, type_)

    def args(self, type_: type) -> list[type]:
        return self._get_args(type_) if self._get_args else []


class Type:
    def __init__(self, type_: type) -> None:
        handler = TypeHandler.get(type_)
        if not handler:
            raise Exception('Unsupported type "%r"' % type_)
        self._type = type_
        self._handler = handler
        self._name = self._handler.name(self._type)
        self._args = self._handler.args(self._type)

    @property
    def name(self) -> str:
        return self._name

    @property
    def args(self) -> list[type]:
        return self._args

    def definition(self, grammar: Grammar) -> str:
        if grammar == Grammar.EBNF:
            return self._handler.ebnf(self._type)
        elif grammar == Grammar.GBNF:
            return self._handler.gbnf(self._type)
        assert False

    def parse(self, payload: str) -> tuple[Any, int]:
        obj, i = self._handler.parse(payload, self._type)
        if obj is None:
            raise Exception('Could not parse type "%r" in payload:\n%s' % (self._type, payload))
        return obj, i


# Pydantic annotated types need a proper rule name in our BNF.
# Since such type may contain a lot of information, we prefer to number them (Fieldinfo1,...)
# We keep a dict of previously seen FieldInfo with an associated counter.
# Unfortunately, FieldInfo doesn't hash properly, we have to implement our how hash function.
FIELD_HASHES: Dict[int, int] = {}


def _hash_fieldinfo(field: FieldInfo) -> int:
    hashes = []
    for m in field.metadata:
        if isinstance(m, PydanticGeneralMetadata):
            hashes.append(hash(frozenset([(k, v) for k, v in m.__dict__.items()])))
        else:
            hashes.append(hash(m))
    return hash(frozenset(hashes))


def composed_name(type_: type[T]) -> str:
    orig = get_origin(type_)
    if orig:
        return str(orig.__name__.lower() + "".join([type_name(a).title() for a in get_args(type_)]))
    return type_.__name__.lower()


def type_name(type_: type) -> str:
    if isinstance(type_, FieldInfo):
        h = _hash_fieldinfo(type_)
        if h not in FIELD_HASHES:
            FIELD_HASHES[h] = len(FIELD_HASHES.keys())
        return f"Fieldinfo{FIELD_HASHES[h]}"
    return Type(type_).name
