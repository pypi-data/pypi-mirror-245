from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Any, Callable, Generic, Literal, cast, overload

from typing_extensions import Self, TypeGuard, TypeVar, override

from kontainer.core.const import Undefined, undefined
from kontainer.core.exception import KontainerTypeError
from kontainer.core.types import Container

ValueT = TypeVar("ValueT", infer_variance=True)
OtherT = TypeVar("OtherT", infer_variance=True)
if TYPE_CHECKING:
    ElementT = TypeVar("ElementT", infer_variance=True)

__all__ = ["Maybe"]


class Maybe(Container[ValueT, None], Generic[ValueT]):
    if TYPE_CHECKING:

        @override
        def __copy__(self) -> Maybe[ValueT]: ...

        @override
        def __deepcopy__(self, memo: dict[Any, Any] | None = None) -> Maybe[ValueT]: ...

    @override
    def __init__(self, value: ValueT | Undefined | None) -> None:
        self._value = value

    @overload
    def __new__(cls, value: Undefined) -> Maybe[Any]: ...

    @overload
    def __new__(cls, value: None) -> Maybe[Any]: ...

    @overload
    def __new__(cls, value: Undefined | None) -> Maybe[Any]: ...

    @overload
    def __new__(cls, value: ValueT | Undefined) -> Maybe[ValueT]: ...

    @overload
    def __new__(cls, value: ValueT | None) -> Maybe[ValueT]: ...

    @overload
    def __new__(cls, value: ValueT | Undefined | None) -> Maybe[ValueT]: ...

    @override
    def __new__(cls, value: ValueT | Undefined | None) -> Maybe[ValueT]:
        if value is None or value is undefined:
            return Null(None)
        value = cast("ValueT", value)
        return Some(value)

    @override
    def __repr__(self) -> str:
        container_type = type(self)
        if issubclass(container_type, Some):
            name = "Some"
        elif issubclass(container_type, Null):
            name = "Null"
        else:
            name = "Maybe"  # pragma: no cover
        return f"<{name}: value={self._value!r}>"

    @override
    def __str__(self) -> str:
        return str(self._value)

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Maybe) and other._value == self._value

    @override
    def __hash__(self) -> int:
        return hash((Maybe, self._value))

    @override
    def map_value(self, func: Callable[[ValueT], OtherT]) -> Maybe[OtherT]:
        raise NotImplementedError

    @override
    def map_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], OtherT]
    ) -> Maybe[OtherT]:
        raise NotImplementedError

    @override
    def map_container(
        self, value: Maybe[ElementT], func: Callable[[ValueT, ElementT], OtherT]
    ) -> Maybe[OtherT]:
        raise NotImplementedError

    @override
    def bind_value(self, func: Callable[[ValueT], Maybe[OtherT]]) -> Maybe[OtherT]:
        raise NotImplementedError

    @override
    def bind_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], Maybe[OtherT]]
    ) -> Maybe[OtherT]:
        raise NotImplementedError

    @override
    def bind_container(
        self, value: Maybe[ElementT], func: Callable[[ValueT, ElementT], Maybe[OtherT]]
    ) -> Maybe[OtherT]:
        raise NotImplementedError

    @override
    def switch(self) -> Maybe[None]:
        raise NotImplementedError

    @override
    def default(self, value: OtherT) -> ValueT | OtherT:
        raise NotImplementedError

    @override
    def map_default(self, func: Callable[[], OtherT]) -> ValueT | OtherT:
        raise NotImplementedError

    @override
    def unwrap(self) -> ValueT:
        raise NotImplementedError

    @property
    @override
    def is_positive(self) -> bool:
        raise NotImplementedError

    @staticmethod
    def some(value: OtherT) -> Some[OtherT]:
        return Some(value)

    @staticmethod
    def null(value: Any) -> Null[Any]:  # noqa: ARG004
        return Null(None)

    @staticmethod
    def is_some(maybe: Maybe[OtherT]) -> TypeGuard[Some[OtherT]]:
        return maybe.is_positive

    @staticmethod
    def is_null(maybe: Maybe[OtherT]) -> TypeGuard[Null[OtherT]]:
        return maybe.is_negative

    @override
    def copy(self) -> Maybe[ValueT]:
        raise NotImplementedError

    @override
    def deepcopy(self) -> Maybe[ValueT]:
        raise NotImplementedError

    @override
    def ensure_positive(self) -> Some[ValueT]:
        raise NotImplementedError

    @override
    def ensure_negative(self) -> Null[ValueT]:
        raise NotImplementedError


class Some(Maybe[ValueT], Generic[ValueT]):
    if TYPE_CHECKING:

        @override
        def __copy__(self) -> Some[ValueT]: ...

        @override
        def __deepcopy__(self, memo: dict[Any, Any] | None = None) -> Some[ValueT]: ...

    _value: ValueT

    @override
    def __new__(cls, value: ValueT) -> Self:
        return super(Container, cls).__new__(cls)

    @override
    def map_value(self, func: Callable[[ValueT], OtherT]) -> Maybe[OtherT]:
        return Some(func(self._value))

    @override
    def map_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], OtherT]
    ) -> Maybe[OtherT]:
        return Some(func(self._value, value))

    @override
    def map_container(
        self, value: Maybe[ElementT], func: Callable[[ValueT, ElementT], OtherT]
    ) -> Maybe[OtherT]:
        return value.bind_value(lambda x: self.map_values(x, func))

    @override
    def bind_value(self, func: Callable[[ValueT], Maybe[OtherT]]) -> Maybe[OtherT]:
        return func(self._value)

    @override
    def bind_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], Maybe[OtherT]]
    ) -> Maybe[OtherT]:
        return func(self._value, value)

    @override
    def bind_container(
        self, value: Maybe[ElementT], func: Callable[[ValueT, ElementT], Maybe[OtherT]]
    ) -> Maybe[OtherT]:
        return value.bind_value(lambda x: self.bind_values(x, func))

    @override
    def switch(self) -> Maybe[None]:
        return Null(None)

    @override
    def default(self, value: Any) -> ValueT:
        return self._value

    @override
    def map_default(self, func: Callable[[], Any]) -> ValueT:
        return self._value

    @override
    def unwrap(self) -> ValueT:
        return self._value

    @property
    @override
    def is_positive(self) -> Literal[True]:
        return True

    @override
    def copy(self) -> Some[ValueT]:
        return self.some(self._value)

    @override
    def deepcopy(self) -> Some[ValueT]:
        new = deepcopy(self._value)
        return self.some(new)

    @override
    def ensure_positive(self) -> Some[ValueT]:
        return Some(self._value)

    @override
    def ensure_negative(self) -> Null[ValueT]:
        error_msg = f"{self!r} is not null"
        raise KontainerTypeError(error_msg)


class Null(Maybe[ValueT], Generic[ValueT]):
    if TYPE_CHECKING:

        @override
        def __copy__(self) -> Null[ValueT]: ...

        @override
        def __deepcopy__(self, memo: dict[Any, Any] | None = None) -> Null[ValueT]: ...

    @override
    def __init__(self, value: ValueT | None) -> None:
        if value is undefined:
            value = None
        super().__init__(value)

    @override
    def __new__(cls, value: ValueT) -> Null[Any]:
        return super(Container, cls).__new__(cls)

    @override
    def map_value(self, func: Callable[[ValueT], OtherT]) -> Null[OtherT]:
        return Null(None)

    @override
    def map_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], OtherT]
    ) -> Maybe[OtherT]:
        return Null(None)

    @override
    def map_container(
        self, value: Maybe[ElementT], func: Callable[[ValueT, ElementT], OtherT]
    ) -> Maybe[OtherT]:
        return Null(None)

    @override
    def bind_value(self, func: Callable[[ValueT], Maybe[OtherT]]) -> Maybe[OtherT]:
        return Null(None)

    @override
    def bind_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], Maybe[OtherT]]
    ) -> Maybe[OtherT]:
        return Null(None)

    @override
    def bind_container(
        self, value: Maybe[ElementT], func: Callable[[ValueT, ElementT], Maybe[OtherT]]
    ) -> Maybe[OtherT]:
        return Null(None)

    @override
    def switch(self) -> Maybe[None]:
        return Some(None)

    @override
    def default(self, value: OtherT) -> OtherT:
        return value

    @override
    def map_default(self, func: Callable[[], OtherT]) -> OtherT:
        return func()

    @override
    def unwrap(self) -> None:
        return None

    @property
    @override
    def is_positive(self) -> Literal[False]:
        return False

    @override
    def copy(self) -> Null[ValueT]:
        return self.null(self._value)

    @override
    def deepcopy(self) -> Null[ValueT]:
        new = deepcopy(self._value)
        return self.null(new)

    @override
    def ensure_positive(self) -> Some[ValueT]:
        error_msg = f"{self!r} is not some"
        raise KontainerTypeError(error_msg)

    @override
    def ensure_negative(self) -> Null[ValueT]:
        return Null(self._value)
