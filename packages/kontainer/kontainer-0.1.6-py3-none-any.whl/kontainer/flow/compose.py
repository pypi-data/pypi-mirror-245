from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, overload

if TYPE_CHECKING:
    from typing_extensions import TypeVar

    from kontainer.container import Maybe, Result
    from kontainer.core.types import Container

    ValueT = TypeVar("ValueT", infer_variance=True)
    ValueT0 = TypeVar("ValueT0", infer_variance=True)
    ValueT1 = TypeVar("ValueT1", infer_variance=True)
    ValueT2 = TypeVar("ValueT2", infer_variance=True)
    ValueT3 = TypeVar("ValueT3", infer_variance=True)
    ValueT4 = TypeVar("ValueT4", infer_variance=True)
    ValueT5 = TypeVar("ValueT5", infer_variance=True)
    ValueT6 = TypeVar("ValueT6", infer_variance=True)
    ValueT7 = TypeVar("ValueT7", infer_variance=True)
    ValueT8 = TypeVar("ValueT8", infer_variance=True)
    ValueT9 = TypeVar("ValueT9", infer_variance=True)
    ValueT10 = TypeVar("ValueT10", infer_variance=True)

    @overload
    def compose_funcs() -> Callable[[ValueT], ValueT]: ...

    @overload
    def compose_funcs(
        func0: Callable[[ValueT], ValueT0], /
    ) -> Callable[[ValueT], ValueT0]: ...

    @overload
    def compose_funcs(
        func0: Callable[[ValueT], ValueT0], func1: Callable[[ValueT0], ValueT1], /
    ) -> Callable[[ValueT], ValueT1]: ...

    @overload
    def compose_funcs(
        func0: Callable[[ValueT], ValueT0],
        func1: Callable[[ValueT0], ValueT1],
        func2: Callable[[ValueT1], ValueT2],
        /,
    ) -> Callable[[ValueT], ValueT2]: ...

    @overload
    def compose_funcs(
        func0: Callable[[ValueT], ValueT0],
        func1: Callable[[ValueT0], ValueT1],
        func2: Callable[[ValueT1], ValueT2],
        func3: Callable[[ValueT2], ValueT3],
        /,
    ) -> Callable[[ValueT], ValueT3]: ...

    @overload
    def compose_funcs(
        func0: Callable[[ValueT], ValueT0],
        func1: Callable[[ValueT0], ValueT1],
        func2: Callable[[ValueT1], ValueT2],
        func3: Callable[[ValueT2], ValueT3],
        func4: Callable[[ValueT3], ValueT4],
        /,
    ) -> Callable[[ValueT], ValueT4]: ...

    @overload
    def compose_funcs(
        func0: Callable[[ValueT], ValueT0],
        func1: Callable[[ValueT0], ValueT1],
        func2: Callable[[ValueT1], ValueT2],
        func3: Callable[[ValueT2], ValueT3],
        func4: Callable[[ValueT3], ValueT4],
        func5: Callable[[ValueT4], ValueT5],
        /,
    ) -> Callable[[ValueT], ValueT5]: ...

    @overload
    def compose_funcs(
        func0: Callable[[ValueT], ValueT0],
        func1: Callable[[ValueT0], ValueT1],
        func2: Callable[[ValueT1], ValueT2],
        func3: Callable[[ValueT2], ValueT3],
        func4: Callable[[ValueT3], ValueT4],
        func5: Callable[[ValueT4], ValueT5],
        func6: Callable[[ValueT5], ValueT6],
        /,
    ) -> Callable[[ValueT], ValueT6]: ...

    @overload
    def compose_funcs(
        func0: Callable[[ValueT], ValueT0],
        func1: Callable[[ValueT0], ValueT1],
        func2: Callable[[ValueT1], ValueT2],
        func3: Callable[[ValueT2], ValueT3],
        func4: Callable[[ValueT3], ValueT4],
        func5: Callable[[ValueT4], ValueT5],
        func6: Callable[[ValueT5], ValueT6],
        func7: Callable[[ValueT6], ValueT7],
        /,
    ) -> Callable[[ValueT], ValueT7]: ...

    @overload
    def compose_funcs(
        func0: Callable[[ValueT], ValueT0],
        func1: Callable[[ValueT0], ValueT1],
        func2: Callable[[ValueT1], ValueT2],
        func3: Callable[[ValueT2], ValueT3],
        func4: Callable[[ValueT3], ValueT4],
        func5: Callable[[ValueT4], ValueT5],
        func6: Callable[[ValueT5], ValueT6],
        func7: Callable[[ValueT6], ValueT7],
        func8: Callable[[ValueT7], ValueT8],
        /,
    ) -> Callable[[ValueT], ValueT8]: ...

    @overload
    def compose_funcs(
        func0: Callable[[ValueT], ValueT0],
        func1: Callable[[ValueT0], ValueT1],
        func2: Callable[[ValueT1], ValueT2],
        func3: Callable[[ValueT2], ValueT3],
        func4: Callable[[ValueT3], ValueT4],
        func5: Callable[[ValueT4], ValueT5],
        func6: Callable[[ValueT5], ValueT6],
        func7: Callable[[ValueT6], ValueT7],
        func8: Callable[[ValueT7], ValueT8],
        func9: Callable[[ValueT8], ValueT9],
        /,
    ) -> Callable[[ValueT], ValueT9]: ...

    @overload
    def compose_funcs(
        func0: Callable[[ValueT], ValueT0],
        func1: Callable[[ValueT0], ValueT1],
        func2: Callable[[ValueT1], ValueT2],
        func3: Callable[[ValueT2], ValueT3],
        func4: Callable[[ValueT3], ValueT4],
        func5: Callable[[ValueT4], ValueT5],
        func6: Callable[[ValueT5], ValueT6],
        func7: Callable[[ValueT6], ValueT7],
        func8: Callable[[ValueT7], ValueT8],
        func9: Callable[[ValueT8], ValueT9],
        func10: Callable[[ValueT9], ValueT10],
        /,
    ) -> Callable[[ValueT], ValueT10]: ...

    @overload
    def compose_funcs(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]: ...

    @overload
    def compose_bind_funcs() -> Callable[[ValueT], Container[ValueT, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Maybe[ValueT0]], /
    ) -> Callable[[ValueT], Maybe[ValueT0]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Maybe[ValueT0]],
        func1: Callable[[ValueT0], Maybe[ValueT1]],
        /,
    ) -> Callable[[ValueT], Maybe[ValueT1]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Maybe[ValueT0]],
        func1: Callable[[ValueT0], Maybe[ValueT1]],
        func2: Callable[[ValueT1], Maybe[ValueT2]],
        /,
    ) -> Callable[[ValueT], Maybe[ValueT2]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Maybe[ValueT0]],
        func1: Callable[[ValueT0], Maybe[ValueT1]],
        func2: Callable[[ValueT1], Maybe[ValueT2]],
        func3: Callable[[ValueT2], Maybe[ValueT3]],
        /,
    ) -> Callable[[ValueT], Maybe[ValueT3]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Maybe[ValueT0]],
        func1: Callable[[ValueT0], Maybe[ValueT1]],
        func2: Callable[[ValueT1], Maybe[ValueT2]],
        func3: Callable[[ValueT2], Maybe[ValueT3]],
        func4: Callable[[ValueT3], Maybe[ValueT4]],
        /,
    ) -> Callable[[ValueT], Maybe[ValueT4]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Maybe[ValueT0]],
        func1: Callable[[ValueT0], Maybe[ValueT1]],
        func2: Callable[[ValueT1], Maybe[ValueT2]],
        func3: Callable[[ValueT2], Maybe[ValueT3]],
        func4: Callable[[ValueT3], Maybe[ValueT4]],
        func5: Callable[[ValueT4], Maybe[ValueT5]],
        /,
    ) -> Callable[[ValueT], Maybe[ValueT5]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Maybe[ValueT0]],
        func1: Callable[[ValueT0], Maybe[ValueT1]],
        func2: Callable[[ValueT1], Maybe[ValueT2]],
        func3: Callable[[ValueT2], Maybe[ValueT3]],
        func4: Callable[[ValueT3], Maybe[ValueT4]],
        func5: Callable[[ValueT4], Maybe[ValueT5]],
        func6: Callable[[ValueT5], Maybe[ValueT6]],
        /,
    ) -> Callable[[ValueT], Maybe[ValueT6]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Maybe[ValueT0]],
        func1: Callable[[ValueT0], Maybe[ValueT1]],
        func2: Callable[[ValueT1], Maybe[ValueT2]],
        func3: Callable[[ValueT2], Maybe[ValueT3]],
        func4: Callable[[ValueT3], Maybe[ValueT4]],
        func5: Callable[[ValueT4], Maybe[ValueT5]],
        func6: Callable[[ValueT5], Maybe[ValueT6]],
        func7: Callable[[ValueT6], Maybe[ValueT7]],
        /,
    ) -> Callable[[ValueT], Maybe[ValueT7]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Maybe[ValueT0]],
        func1: Callable[[ValueT0], Maybe[ValueT1]],
        func2: Callable[[ValueT1], Maybe[ValueT2]],
        func3: Callable[[ValueT2], Maybe[ValueT3]],
        func4: Callable[[ValueT3], Maybe[ValueT4]],
        func5: Callable[[ValueT4], Maybe[ValueT5]],
        func6: Callable[[ValueT5], Maybe[ValueT6]],
        func7: Callable[[ValueT6], Maybe[ValueT7]],
        func8: Callable[[ValueT7], Maybe[ValueT8]],
        /,
    ) -> Callable[[ValueT], Maybe[ValueT8]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Maybe[ValueT0]],
        func1: Callable[[ValueT0], Maybe[ValueT1]],
        func2: Callable[[ValueT1], Maybe[ValueT2]],
        func3: Callable[[ValueT2], Maybe[ValueT3]],
        func4: Callable[[ValueT3], Maybe[ValueT4]],
        func5: Callable[[ValueT4], Maybe[ValueT5]],
        func6: Callable[[ValueT5], Maybe[ValueT6]],
        func7: Callable[[ValueT6], Maybe[ValueT7]],
        func8: Callable[[ValueT7], Maybe[ValueT8]],
        func9: Callable[[ValueT8], Maybe[ValueT9]],
        /,
    ) -> Callable[[ValueT], Maybe[ValueT9]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Maybe[ValueT0]],
        func1: Callable[[ValueT0], Maybe[ValueT1]],
        func2: Callable[[ValueT1], Maybe[ValueT2]],
        func3: Callable[[ValueT2], Maybe[ValueT3]],
        func4: Callable[[ValueT3], Maybe[ValueT4]],
        func5: Callable[[ValueT4], Maybe[ValueT5]],
        func6: Callable[[ValueT5], Maybe[ValueT6]],
        func7: Callable[[ValueT6], Maybe[ValueT7]],
        func8: Callable[[ValueT7], Maybe[ValueT8]],
        func9: Callable[[ValueT8], Maybe[ValueT9]],
        func10: Callable[[ValueT9], Maybe[ValueT10]],
        /,
    ) -> Callable[[ValueT], Maybe[ValueT10]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Result[ValueT0, Any]], /
    ) -> Callable[[ValueT], Result[ValueT0, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Result[ValueT0, Any]],
        func1: Callable[[ValueT0], Result[ValueT1, Any]],
        /,
    ) -> Callable[[ValueT], Result[ValueT1, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Result[ValueT0, Any]],
        func1: Callable[[ValueT0], Result[ValueT1, Any]],
        func2: Callable[[ValueT1], Result[ValueT2, Any]],
        /,
    ) -> Callable[[ValueT], Result[ValueT2, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Result[ValueT0, Any]],
        func1: Callable[[ValueT0], Result[ValueT1, Any]],
        func2: Callable[[ValueT1], Result[ValueT2, Any]],
        func3: Callable[[ValueT2], Result[ValueT3, Any]],
        /,
    ) -> Callable[[ValueT], Result[ValueT3, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Result[ValueT0, Any]],
        func1: Callable[[ValueT0], Result[ValueT1, Any]],
        func2: Callable[[ValueT1], Result[ValueT2, Any]],
        func3: Callable[[ValueT2], Result[ValueT3, Any]],
        func4: Callable[[ValueT3], Result[ValueT4, Any]],
        /,
    ) -> Callable[[ValueT], Result[ValueT4, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Result[ValueT0, Any]],
        func1: Callable[[ValueT0], Result[ValueT1, Any]],
        func2: Callable[[ValueT1], Result[ValueT2, Any]],
        func3: Callable[[ValueT2], Result[ValueT3, Any]],
        func4: Callable[[ValueT3], Result[ValueT4, Any]],
        func5: Callable[[ValueT4], Result[ValueT5, Any]],
        /,
    ) -> Callable[[ValueT], Result[ValueT5, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Result[ValueT0, Any]],
        func1: Callable[[ValueT0], Result[ValueT1, Any]],
        func2: Callable[[ValueT1], Result[ValueT2, Any]],
        func3: Callable[[ValueT2], Result[ValueT3, Any]],
        func4: Callable[[ValueT3], Result[ValueT4, Any]],
        func5: Callable[[ValueT4], Result[ValueT5, Any]],
        func6: Callable[[ValueT5], Result[ValueT6, Any]],
        /,
    ) -> Callable[[ValueT], Result[ValueT6, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Result[ValueT0, Any]],
        func1: Callable[[ValueT0], Result[ValueT1, Any]],
        func2: Callable[[ValueT1], Result[ValueT2, Any]],
        func3: Callable[[ValueT2], Result[ValueT3, Any]],
        func4: Callable[[ValueT3], Result[ValueT4, Any]],
        func5: Callable[[ValueT4], Result[ValueT5, Any]],
        func6: Callable[[ValueT5], Result[ValueT6, Any]],
        func7: Callable[[ValueT6], Result[ValueT7, Any]],
        /,
    ) -> Callable[[ValueT], Result[ValueT7, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Result[ValueT0, Any]],
        func1: Callable[[ValueT0], Result[ValueT1, Any]],
        func2: Callable[[ValueT1], Result[ValueT2, Any]],
        func3: Callable[[ValueT2], Result[ValueT3, Any]],
        func4: Callable[[ValueT3], Result[ValueT4, Any]],
        func5: Callable[[ValueT4], Result[ValueT5, Any]],
        func6: Callable[[ValueT5], Result[ValueT6, Any]],
        func7: Callable[[ValueT6], Result[ValueT7, Any]],
        func8: Callable[[ValueT7], Result[ValueT8, Any]],
        /,
    ) -> Callable[[ValueT], Result[ValueT8, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Result[ValueT0, Any]],
        func1: Callable[[ValueT0], Result[ValueT1, Any]],
        func2: Callable[[ValueT1], Result[ValueT2, Any]],
        func3: Callable[[ValueT2], Result[ValueT3, Any]],
        func4: Callable[[ValueT3], Result[ValueT4, Any]],
        func5: Callable[[ValueT4], Result[ValueT5, Any]],
        func6: Callable[[ValueT5], Result[ValueT6, Any]],
        func7: Callable[[ValueT6], Result[ValueT7, Any]],
        func8: Callable[[ValueT7], Result[ValueT8, Any]],
        func9: Callable[[ValueT8], Result[ValueT9, Any]],
        /,
    ) -> Callable[[ValueT], Result[ValueT9, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Result[ValueT0, Any]],
        func1: Callable[[ValueT0], Result[ValueT1, Any]],
        func2: Callable[[ValueT1], Result[ValueT2, Any]],
        func3: Callable[[ValueT2], Result[ValueT3, Any]],
        func4: Callable[[ValueT3], Result[ValueT4, Any]],
        func5: Callable[[ValueT4], Result[ValueT5, Any]],
        func6: Callable[[ValueT5], Result[ValueT6, Any]],
        func7: Callable[[ValueT6], Result[ValueT7, Any]],
        func8: Callable[[ValueT7], Result[ValueT8, Any]],
        func9: Callable[[ValueT8], Result[ValueT9, Any]],
        func10: Callable[[ValueT9], Result[ValueT10, Any]],
        /,
    ) -> Callable[[ValueT], Result[ValueT10, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Container[ValueT0, Any]], /
    ) -> Callable[[ValueT], Container[ValueT0, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Container[ValueT0, Any]],
        func1: Callable[[ValueT0], Container[ValueT1, Any]],
        /,
    ) -> Callable[[ValueT], Container[ValueT1, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Container[ValueT0, Any]],
        func1: Callable[[ValueT0], Container[ValueT1, Any]],
        func2: Callable[[ValueT1], Container[ValueT2, Any]],
        /,
    ) -> Callable[[ValueT], Container[ValueT2, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Container[ValueT0, Any]],
        func1: Callable[[ValueT0], Container[ValueT1, Any]],
        func2: Callable[[ValueT1], Container[ValueT2, Any]],
        func3: Callable[[ValueT2], Container[ValueT3, Any]],
        /,
    ) -> Callable[[ValueT], Container[ValueT3, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Container[ValueT0, Any]],
        func1: Callable[[ValueT0], Container[ValueT1, Any]],
        func2: Callable[[ValueT1], Container[ValueT2, Any]],
        func3: Callable[[ValueT2], Container[ValueT3, Any]],
        func4: Callable[[ValueT3], Container[ValueT4, Any]],
        /,
    ) -> Callable[[ValueT], Container[ValueT4, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Container[ValueT0, Any]],
        func1: Callable[[ValueT0], Container[ValueT1, Any]],
        func2: Callable[[ValueT1], Container[ValueT2, Any]],
        func3: Callable[[ValueT2], Container[ValueT3, Any]],
        func4: Callable[[ValueT3], Container[ValueT4, Any]],
        func5: Callable[[ValueT4], Container[ValueT5, Any]],
        /,
    ) -> Callable[[ValueT], Container[ValueT5, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Container[ValueT0, Any]],
        func1: Callable[[ValueT0], Container[ValueT1, Any]],
        func2: Callable[[ValueT1], Container[ValueT2, Any]],
        func3: Callable[[ValueT2], Container[ValueT3, Any]],
        func4: Callable[[ValueT3], Container[ValueT4, Any]],
        func5: Callable[[ValueT4], Container[ValueT5, Any]],
        func6: Callable[[ValueT5], Container[ValueT6, Any]],
        /,
    ) -> Callable[[ValueT], Container[ValueT6, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Container[ValueT0, Any]],
        func1: Callable[[ValueT0], Container[ValueT1, Any]],
        func2: Callable[[ValueT1], Container[ValueT2, Any]],
        func3: Callable[[ValueT2], Container[ValueT3, Any]],
        func4: Callable[[ValueT3], Container[ValueT4, Any]],
        func5: Callable[[ValueT4], Container[ValueT5, Any]],
        func6: Callable[[ValueT5], Container[ValueT6, Any]],
        func7: Callable[[ValueT6], Container[ValueT7, Any]],
        /,
    ) -> Callable[[ValueT], Container[ValueT7, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Container[ValueT0, Any]],
        func1: Callable[[ValueT0], Container[ValueT1, Any]],
        func2: Callable[[ValueT1], Container[ValueT2, Any]],
        func3: Callable[[ValueT2], Container[ValueT3, Any]],
        func4: Callable[[ValueT3], Container[ValueT4, Any]],
        func5: Callable[[ValueT4], Container[ValueT5, Any]],
        func6: Callable[[ValueT5], Container[ValueT6, Any]],
        func7: Callable[[ValueT6], Container[ValueT7, Any]],
        func8: Callable[[ValueT7], Container[ValueT8, Any]],
        /,
    ) -> Callable[[ValueT], Container[ValueT8, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Container[ValueT0, Any]],
        func1: Callable[[ValueT0], Container[ValueT1, Any]],
        func2: Callable[[ValueT1], Container[ValueT2, Any]],
        func3: Callable[[ValueT2], Container[ValueT3, Any]],
        func4: Callable[[ValueT3], Container[ValueT4, Any]],
        func5: Callable[[ValueT4], Container[ValueT5, Any]],
        func6: Callable[[ValueT5], Container[ValueT6, Any]],
        func7: Callable[[ValueT6], Container[ValueT7, Any]],
        func8: Callable[[ValueT7], Container[ValueT8, Any]],
        func9: Callable[[ValueT8], Container[ValueT9, Any]],
        /,
    ) -> Callable[[ValueT], Container[ValueT9, Any]]: ...

    @overload
    def compose_bind_funcs(
        func0: Callable[[ValueT], Container[ValueT0, Any]],
        func1: Callable[[ValueT0], Container[ValueT1, Any]],
        func2: Callable[[ValueT1], Container[ValueT2, Any]],
        func3: Callable[[ValueT2], Container[ValueT3, Any]],
        func4: Callable[[ValueT3], Container[ValueT4, Any]],
        func5: Callable[[ValueT4], Container[ValueT5, Any]],
        func6: Callable[[ValueT5], Container[ValueT6, Any]],
        func7: Callable[[ValueT6], Container[ValueT7, Any]],
        func8: Callable[[ValueT7], Container[ValueT8, Any]],
        func9: Callable[[ValueT8], Container[ValueT9, Any]],
        func10: Callable[[ValueT9], Container[ValueT10, Any]],
        /,
    ) -> Callable[[ValueT], Container[ValueT10, Any]]: ...

    @overload
    def compose_bind_funcs(
        *funcs: Callable[[Any], Maybe[Any]]
    ) -> Callable[[Any], Maybe[Any]]: ...

    @overload
    def compose_bind_funcs(
        *funcs: Callable[[Any], Result[Any, Any]]
    ) -> Callable[[Any], Result[Any, Any]]: ...

    @overload
    def compose_bind_funcs(
        *funcs: Callable[[Any], Container[Any, Any]]
    ) -> Callable[[Any], Container[Any, Any]]: ...


__all__ = ["compose_funcs", "compose_bind_funcs"]


class _Compose:
    __slots__ = ("_funcs",)

    def __init__(self, funcs: tuple[Callable[[Any], Any], ...]) -> None:
        self._funcs = funcs

    def __call__(self, value: Any) -> Any:
        result = self._funcs[0](value)
        for func in self._funcs[1:]:
            result = func(result)
        return result


class _ComposeBinds:
    __slots__ = ("_funcs",)

    def __init__(self, funcs: tuple[Callable[[Any], Container[Any, Any]], ...]) -> None:
        self._funcs = funcs

    def __call__(self, value: Any) -> Container[Any, Any]:
        result = self._funcs[0](value)
        for func in self._funcs[1:]:
            result = result.bind_value(func)
        return result


def compose_funcs(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    if not funcs:
        from kontainer.flow.flowtools import identity

        funcs = (identity,)
    return _Compose(funcs)


def compose_bind_funcs(
    *funcs: Callable[[Any], Container[Any, Any]]
) -> Callable[[Any], Container[Any, Any]]:
    if not funcs:
        from kontainer.container.maybe import Some

        funcs = (Some,)
    return _ComposeBinds(funcs)
