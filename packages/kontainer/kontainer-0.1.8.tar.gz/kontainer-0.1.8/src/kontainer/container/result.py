from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Any, Callable, Generic, Literal, NoReturn, overload

from typing_extensions import Self, TypeGuard, TypeVar, override

from kontainer.core.const import Undefined, undefined
from kontainer.core.exception import KontainerTypeError
from kontainer.core.types import Container

ValueT = TypeVar("ValueT", infer_variance=True)
OtherT = TypeVar("OtherT", infer_variance=True)
if TYPE_CHECKING:
    ErrorT = TypeVar("ErrorT", infer_variance=True, bound=Exception)
    AnotherT = TypeVar("AnotherT", infer_variance=True)
    ElementT = TypeVar("ElementT", infer_variance=True)

__all__ = ["Result"]


class Result(Container[ValueT, OtherT], Generic[ValueT, OtherT]):
    if TYPE_CHECKING:

        @override
        def __copy__(self) -> Result[ValueT, OtherT]: ...

        @override
        def __deepcopy__(
            self, memo: dict[Any, Any] | None = None
        ) -> Result[ValueT, OtherT]: ...

    @property
    def _value_or_other(self) -> ValueT | OtherT:
        raise NotImplementedError

    @override
    def __init__(self, value: ValueT) -> None:
        self._value = value

    @overload
    def __new__(cls, value: ErrorT) -> Result[Any, ErrorT]: ...

    @overload
    def __new__(cls, value: type[ErrorT]) -> Result[Any, type[ErrorT]]: ...

    @overload
    def __new__(cls, value: ValueT) -> Result[ValueT, Any]: ...

    @overload
    def __new__(
        cls, value: ValueT | ErrorT | type[ErrorT]
    ) -> Result[ValueT, Any] | Result[Any, ErrorT] | Result[Any, type[ErrorT]]: ...

    @override
    def __new__(
        cls, value: ValueT | ErrorT | type[ErrorT]
    ) -> Result[ValueT, Any] | Result[Any, ErrorT] | Result[Any, type[ErrorT]]:
        if isinstance(value, Exception) or (
            isinstance(value, type) and issubclass(value, Exception)
        ):
            return Error(value)
        return Done(value)

    @override
    def __repr__(self) -> str:
        container_type = type(self)
        if issubclass(container_type, Done):
            name = "Done"
        elif issubclass(container_type, Error):
            name = "Error"
        else:
            name = "Result"  # pragma: no cover
        return f"<{name}: value={self._value!r}>"

    @override
    def __str__(self) -> str:
        return str(self._value)

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Result) and other._value == self._value

    @override
    def __hash__(self) -> int:
        return hash((Result, self._value))

    @override
    def map_value(self, func: Callable[[ValueT], AnotherT]) -> Result[AnotherT, OtherT]:
        raise NotImplementedError

    @override
    def map_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Result[AnotherT, OtherT]:
        raise NotImplementedError

    @override
    def map_container(
        self, value: Result[ElementT, Any], func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Result[AnotherT, OtherT]:
        raise NotImplementedError

    @override
    def bind_value(
        self, func: Callable[[ValueT], Result[AnotherT, OtherT]]
    ) -> Result[AnotherT, OtherT]:
        raise NotImplementedError

    @override
    def bind_values(
        self,
        value: ElementT,
        func: Callable[[ValueT, ElementT], Result[AnotherT, OtherT]],
    ) -> Result[AnotherT, OtherT]:
        raise NotImplementedError

    @override
    def bind_container(
        self,
        value: Result[ElementT, Any],
        func: Callable[[ValueT, ElementT], Result[AnotherT, OtherT]],
    ) -> Result[AnotherT, OtherT]:
        raise NotImplementedError

    @override
    def switch(self) -> Result[OtherT, ValueT]:
        raise NotImplementedError

    @override
    def default(self, value: AnotherT) -> ValueT | AnotherT:
        raise NotImplementedError

    @override
    def map_default(self, func: Callable[[], AnotherT]) -> ValueT | AnotherT:
        raise NotImplementedError

    @override
    def unwrap(self) -> ValueT:
        raise NotImplementedError

    def unwrap_error(self) -> NoReturn:
        raise NotImplementedError

    def unwrap_error_or(self, value: AnotherT) -> AnotherT | NoReturn:
        raise NotImplementedError

    def unwrap_error_or_else(self, func: Callable[[], AnotherT]) -> AnotherT | NoReturn:
        raise NotImplementedError

    def unwrap_error_or_with(
        self, func: Callable[[OtherT], AnotherT]
    ) -> AnotherT | NoReturn:
        raise NotImplementedError

    @property
    @override
    def is_positive(self) -> bool:
        raise NotImplementedError

    @staticmethod
    def done(value: AnotherT) -> Done[AnotherT, Any]:
        return Done(value)

    @staticmethod
    def error(value: AnotherT) -> Error[Any, AnotherT]:
        return Error(value)

    @staticmethod
    def is_done(
        result: Result[AnotherT, ElementT]
    ) -> TypeGuard[Done[AnotherT, ElementT]]:
        return result.is_positive

    @staticmethod
    def is_error(
        result: Result[ElementT, AnotherT]
    ) -> TypeGuard[Error[ElementT, AnotherT]]:
        return result.is_negative

    @override
    def copy(self) -> Result[ValueT, OtherT]:
        raise NotImplementedError

    @override
    def deepcopy(self) -> Result[ValueT, OtherT]:
        raise NotImplementedError

    @override
    def ensure_positive(self) -> Done[ValueT, OtherT]:
        raise NotImplementedError

    @override
    def ensure_negative(self) -> Error[ValueT, OtherT]:
        raise NotImplementedError


class Done(Result[ValueT, OtherT], Generic[ValueT, OtherT]):
    if TYPE_CHECKING:

        @override
        def __copy__(self) -> Done[ValueT, OtherT]: ...

        @override
        def __deepcopy__(
            self, memo: dict[Any, Any] | None = None
        ) -> Done[ValueT, OtherT]: ...

    @property
    @override
    def _value_or_other(self) -> ValueT:
        return self._value

    @override
    def __new__(cls, value: ValueT) -> Self:
        return super(Container, cls).__new__(cls)

    @override
    def map_value(self, func: Callable[[ValueT], AnotherT]) -> Result[AnotherT, OtherT]:
        return Done(func(self._value))

    @override
    def map_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Result[AnotherT, OtherT]:
        return Done(func(self._value, value))

    @override
    def map_container(
        self, value: Result[ElementT, Any], func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Result[AnotherT, OtherT]:
        return value.bind_value(lambda x: self.map_values(x, func))

    @override
    def bind_value(
        self, func: Callable[[ValueT], Result[AnotherT, OtherT]]
    ) -> Result[AnotherT, OtherT]:
        return func(self._value)

    @override
    def bind_values(
        self,
        value: ElementT,
        func: Callable[[ValueT, ElementT], Result[AnotherT, OtherT]],
    ) -> Result[AnotherT, OtherT]:
        return func(self._value, value)

    @override
    def bind_container(
        self,
        value: Result[ElementT, Any],
        func: Callable[[ValueT, ElementT], Result[AnotherT, OtherT]],
    ) -> Result[AnotherT, OtherT]:
        return value.bind_value(lambda x: self.bind_values(x, func))

    @override
    def switch(self) -> Result[OtherT, ValueT]:
        return Error(self._value)

    @override
    def default(self, value: Any) -> ValueT:
        return self._value

    @override
    def map_default(self, func: Callable[[], Any]) -> ValueT:
        return self._value

    @override
    def unwrap(self) -> ValueT:
        return self._value

    @override
    def unwrap_error(self) -> NoReturn:
        raise KontainerTypeError("Not an error container")

    @override
    def unwrap_error_or(self, value: AnotherT) -> AnotherT:
        return value

    @override
    def unwrap_error_or_else(self, func: Callable[[], AnotherT]) -> AnotherT:
        return func()

    def unwrap_error_or_with(
        self,
        func: Callable[[OtherT], Any],  # noqa: ARG002
    ) -> NoReturn:
        raise KontainerTypeError("Not an error container")

    @property
    @override
    def is_positive(self) -> Literal[True]:
        return True

    @override
    def copy(self) -> Done[ValueT, OtherT]:
        return self.done(self._value)

    @override
    def deepcopy(self) -> Done[ValueT, OtherT]:
        new = deepcopy(self._value)
        return self.done(new)

    @override
    def ensure_positive(self) -> Done[ValueT, OtherT]:
        return Done(self._value)

    @override
    def ensure_negative(self) -> Error[ValueT, OtherT]:
        error_msg = f"{self!r} is not error"
        raise KontainerTypeError(error_msg)


class Error(Result[ValueT, OtherT], Generic[ValueT, OtherT]):
    if TYPE_CHECKING:

        @override
        def __copy__(self) -> Error[ValueT, OtherT]: ...

        @override
        def __deepcopy__(
            self, memo: dict[Any, Any] | None = None
        ) -> Error[ValueT, OtherT]: ...

    __slots__ = ("_value", "_other")

    @property
    @override
    def _value_or_other(self) -> OtherT:
        return self._other

    @override
    def __init__(self, value: OtherT) -> None:
        self._value = value if value is undefined else undefined
        self._other = value

    @overload
    def __new__(cls, value: Undefined) -> Error[Any, Any]: ...

    @overload
    def __new__(cls, value: OtherT) -> Error[ValueT, OtherT]: ...

    @overload
    def __new__(
        cls, value: OtherT | Undefined
    ) -> Error[ValueT, OtherT] | Error[Any, Any]: ...

    @override
    def __new__(
        cls, value: OtherT | Undefined
    ) -> Error[ValueT, OtherT] | Error[Any, Any]:
        return super(Container, cls).__new__(cls)

    @override
    def map_value(self, func: Callable[[ValueT], AnotherT]) -> Result[AnotherT, OtherT]:
        return Error(self._other)

    @override
    def map_values(
        self, value: ElementT, func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Result[AnotherT, OtherT]:
        return Error(self._other)

    @override
    def map_container(
        self, value: Result[ElementT, Any], func: Callable[[ValueT, ElementT], AnotherT]
    ) -> Result[AnotherT, OtherT]:
        return Error(self._other)

    @override
    def bind_value(
        self, func: Callable[[ValueT], Result[AnotherT, OtherT]]
    ) -> Result[AnotherT, OtherT]:
        return Error(self._other)

    @override
    def bind_values(
        self,
        value: ElementT,
        func: Callable[[ValueT, ElementT], Result[AnotherT, OtherT]],
    ) -> Result[AnotherT, OtherT]:
        return Error(self._other)

    @override
    def bind_container(
        self,
        value: Result[ElementT, Any],
        func: Callable[[ValueT, ElementT], Result[AnotherT, OtherT]],
    ) -> Result[AnotherT, OtherT]:
        return Error(self._other)

    @override
    def switch(self) -> Result[OtherT, ValueT]:
        return Done(self._other)

    @override
    def default(self, value: AnotherT) -> AnotherT:
        return value

    @override
    def map_default(self, func: Callable[[], AnotherT]) -> AnotherT:
        return func()

    @override
    def unwrap(self) -> NoReturn:
        self.unwrap_error()

    @override
    def unwrap_error(self) -> NoReturn:
        if not isinstance(self._other, Exception):
            raise KontainerTypeError("error container does not hold an error")

        raise self._other

    @override
    def unwrap_error_or(self, value: AnotherT) -> AnotherT | NoReturn:
        if isinstance(self._other, Exception):
            raise self._other
        return value

    @override
    def unwrap_error_or_else(self, func: Callable[[], AnotherT]) -> AnotherT | NoReturn:
        if isinstance(self._other, Exception):
            raise self._other
        return func()

    def unwrap_error_or_with(self, func: Callable[[OtherT], AnotherT]) -> AnotherT:
        return func(self._other)

    @property
    @override
    def is_positive(self) -> Literal[False]:
        return False

    @override
    def copy(self) -> Error[ValueT, OtherT]:
        return self.error(self._other)

    @override
    def deepcopy(self) -> Error[ValueT, OtherT]:
        new = deepcopy(self._other)
        return self.error(new)

    @override
    def ensure_positive(self) -> Done[ValueT, OtherT]:
        error_msg = f"{self!r} is not done"
        raise KontainerTypeError(error_msg)

    @override
    def ensure_negative(self) -> Error[ValueT, OtherT]:
        return Error(self._other)
