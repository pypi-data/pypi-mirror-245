from datetime import datetime
from enum import Enum
from typing import Any, Callable, Iterable, List, Literal, Mapping, Self

from pydantic_core import core_schema

BaseTypes = (
    int
    | float
    | bool
    | str
    | ObjectId
    | MaxKey
    | MinKey
    | Symbol
    | JavaScriptCodeWithScope
    | BinarySubtype
    | Binary
    | JavaScriptCode
    | Decimal128
    | Regex
    | Timestamp
    | datetime
    | Undefined
    | None
)
CollectionTypes = (
    List[BaseTypes | CollectionTypes]
    | Mapping[str, BaseTypes | CollectionTypes]
    | Document
)

DocumentTypes = Document | Mapping[str, CollectionTypes | BaseTypes]

class Direction(Enum):
    ASCENDING: 1
    DESCENDING: -1

class FieldSort:
    field: str
    direction: Direction

class FieldProjection:
    field: str
    include: bool

class Projection:
    field_projections: list[FieldProjection]
    include_id: bool = True

UpdateOperators = Literal[
    "$set",
    "$inc",
    "$push",
    "$unset",
    "$replaceRoot",
    "$rename",
    "$addToSet",
    "$pop",
    "$pull",
]

Update = Mapping[UpdateOperators, Mapping[str, CollectionTypes | BaseTypes]]

FilterTypes = int | float | bool | str | Mapping[str, "FilterTypes"]
Filter = Mapping[str, FilterTypes]

class Document:
    def __init__(
        self,
        dict: dict[str, BaseTypes | CollectionTypes] | None = None,
        **kwargs: BaseTypes | CollectionTypes,
    ) -> None: ...
    def copy(self) -> Self: ...
    def clear(self) -> None: ...
    def len(self) -> int: ...
    def __len__(self) -> int: ...
    def is_empty(self) -> bool: ...
    def contains(self, key: str) -> bool: ...
    def __contains__(self, key: str) -> bool: ...
    def get(self, key: str) -> BaseTypes | CollectionTypes | None: ...
    def __getitem__(self, key: str) -> BaseTypes | CollectionTypes: ...
    def set(self, key: str, value: BaseTypes | CollectionTypes) -> None: ...
    def __setitem__(self, key: str, value: BaseTypes | CollectionTypes) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def keys(self) -> list[str]: ...
    def values(self) -> list[BaseTypes | CollectionTypes]: ...
    def items(self) -> list[tuple[str, BaseTypes | CollectionTypes]]: ...
    def __iter__(self) -> Iterable[tuple[str, BaseTypes | CollectionTypes]]: ...

Document.__annotations__["del"] = Callable[[str], None]

class DocumentIter:
    def __next__(self) -> tuple[str, BaseTypes | CollectionTypes] | None: ...
    def __repr__(self) -> str: ...
    def __len__(self) -> int: ...

class MaxKey:
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class MinKey:
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class Undefined:
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class Symbol:
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    @property
    def symbol(self) -> str: ...
    @symbol.setter
    def symbol(self, symbol: str) -> None: ...

class JavaScriptCode:
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    @property
    def code(self) -> str: ...
    @code.setter
    def code(self, code: str) -> None: ...

class JavaScriptCodeWithScope:
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    @property
    def code(self) -> str: ...
    @code.setter
    def code(self, code: str) -> None: ...
    @property
    def scope(self) -> Document: ...
    @scope.setter
    def scope(self, scope: Document) -> None: ...

class Timestamp:
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    @property
    def timestamp(self) -> int: ...

class Regex:
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    @property
    def pattern(self) -> str: ...
    @pattern.setter
    def pattern(self, code: str) -> None: ...
    @property
    def options(self) -> str: ...
    @options.setter
    def options(self, options: str) -> None: ...

class BinarySubtype:
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    @property
    def value(self) -> str: ...

class Binary:
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    @property
    def bytes(self) -> bytes: ...
    @property
    def value(self) -> str: ...
    @property
    def subtype(self) -> BinarySubtype: ...
    @subtype.setter
    def subtype(self, subtype) -> None: ...

class ObjectId:
    def __init__(self) -> Self: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    @property
    def value(self) -> str: ...
    @classmethod
    def is_valid(cls: Self, value: str) -> bool: ...
    @staticmethod
    def from_str(value: str) -> Self: ...

class PydanticObjectId:
    @classmethod
    def validate_object_id(cls, v: Any, handler) -> ObjectId: ...
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type, _handler
    ) -> core_schema.CoreSchema: ...
    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler): ...

class Decimal128:
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    @property
    def bytes(self) -> bytes: ...
    @property
    def value(self) -> str: ...

class IndexOptions:
    def __init__(
        self,
        name: str | None = None,
        sparse: bool | None = None,
        unique: bool | None = None,
        default_language: str | None = None,
        language_override: str | None = None,
        weigths: Document | None = None,
        bits: int | None = None,
        max: float | None = None,
        min: float | None = None,
        bucket_size: int | None = None,
        partial_filter_expression: Document | None = None,
        wildcard_projection: Document | None = None,
        hidden: bool | None = None,
    ) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def name(self) -> str | None: ...
    @name.setter
    def name(self, name: str) -> None: ...
    @property
    def sparse(self) -> bool | None: ...
    @sparse.setter
    def sparse(self, sparse: bool) -> None: ...
    @property
    def unique(self) -> bool | None: ...
    @unique.setter
    def unique(self, unique: bool) -> None: ...
    @property
    def default_language(self) -> str | None: ...
    @default_language.setter
    def default_language(self, default_language: str) -> None: ...
    @property
    def language_override(self) -> str | None: ...
    @language_override.setter
    def language_override(self, language_override: str) -> None: ...
    @property
    def weigths(self) -> Document | None: ...
    @weigths.setter
    def weigths(self, weigths: Document) -> None: ...
    @property
    def bits(self) -> int | None: ...
    @bits.setter
    def bits(self, bits: int) -> None: ...
    @property
    def max(self) -> float | None: ...
    @max.setter
    def max(self, max: float) -> None: ...
    @property
    def min(self) -> float | None: ...
    @min.setter
    def min(self, min: float) -> None: ...
    @property
    def bucket_size(self) -> int | None: ...
    @bucket_size.setter
    def bucket_size(self, bucket_size: int) -> None: ...
    @property
    def partial_filter_expression(self) -> Document | None: ...
    @partial_filter_expression.setter
    def partial_filter_expression(
        self, partial_filter_expression: Document
    ) -> None: ...
    @property
    def wildcard_projection(self) -> Document | None: ...
    @wildcard_projection.setter
    def wildcard_projection(self, wildcard_projection: Document) -> None: ...
    @property
    def hidden(self) -> bool | None: ...
    @hidden.setter
    def hidden(self, hidden: bool) -> None: ...

class IndexModel:
    def __init__(
        self,
        keys: dict[str, BaseTypes | CollectionTypes],
        options: IndexOptions | None = None,
    ) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def keys(self) -> Document: ...
    @keys.setter
    def keys(self, keys: Document) -> None: ...
    @property
    def options(self) -> IndexOptions | None: ...
    @options.setter
    def options(self, options: IndexOptions) -> None: ...
