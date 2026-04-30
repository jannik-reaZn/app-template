from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any, Generic, ParamSpec, TypeVar, cast

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")
F = TypeVar("F")
P = ParamSpec("P")


@dataclass(frozen=True, slots=True)
class Result(Generic[T, E]):
    _is_ok: bool
    _value: T | None = None
    _error: E | None = None

    @classmethod
    def ok(cls, value: T) -> Result[T, E]:
        return cls(_is_ok=True, _value=value)

    @classmethod
    def err(cls, error: E) -> Result[T, E]:
        return cls(_is_ok=False, _error=error)

    @property
    def is_ok(self) -> bool:
        return self._is_ok

    @property
    def is_err(self) -> bool:
        return not self._is_ok

    @property
    def value(self) -> T:
        return self.unwrap()

    @property
    def error(self) -> E:
        return self.unwrap_err()

    def unwrap(self) -> T:
        if self.is_err:
            raise ValueError(f"Tried to unwrap an Err result: {self._error!r}")
        return cast(T, self._value)

    def unwrap_err(self) -> E:
        if self.is_ok:
            raise ValueError(f"Tried to unwrap_err an Ok result: {self._value!r}")
        return cast(E, self._error)

    def unwrap_or(self, default: U) -> T | U:
        if self.is_ok:
            return cast(T, self._value)
        return default

    def unwrap_or_else(self, fn: Callable[[E], U]) -> T | U:
        if self.is_ok:
            return cast(T, self._value)
        return fn(cast(E, self._error))

    def map(self, fn: Callable[[T], U]) -> Result[U, E]:
        if self.is_err:
            return Result.err(cast(E, self._error))
        return Result.ok(fn(cast(T, self._value)))

    def map_error(self, fn: Callable[[E], F]) -> Result[T, F]:
        if self.is_ok:
            return Result.ok(cast(T, self._value))
        return Result.err(fn(cast(E, self._error)))

    def and_then(self, fn: Callable[[T], Result[U, E]]) -> Result[U, E]:
        if self.is_err:
            return Result.err(cast(E, self._error))
        return fn(cast(T, self._value))

    def bind(self, fn: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return self.and_then(fn)

    def or_else(self, fn: Callable[[E], Result[T, F]]) -> Result[T, F]:
        if self.is_ok:
            return Result.ok(cast(T, self._value))
        return fn(cast(E, self._error))

    def recover(self, fn: Callable[[E], T]) -> Result[T, E]:
        if self.is_ok:
            return Result.ok(cast(T, self._value))
        return Result.ok(fn(cast(E, self._error)))

    def tap(self, fn: Callable[[T], Any]) -> Result[T, E]:
        if self.is_ok:
            fn(cast(T, self._value))
        return self

    def tap_error(self, fn: Callable[[E], Any]) -> Result[T, E]:
        if self.is_err:
            fn(cast(E, self._error))
        return self

    def inspect(self, fn: Callable[[T], Any]) -> Result[T, E]:
        return self.tap(fn)

    def inspect_error(self, fn: Callable[[E], Any]) -> Result[T, E]:
        return self.tap_error(fn)

    def match(self, ok_fn: Callable[[T], U], err_fn: Callable[[E], U]) -> U:
        if self.is_ok:
            return ok_fn(cast(T, self._value))
        return err_fn(cast(E, self._error))

    def to_tuple(self) -> tuple[T | None, E | None]:
        return (self._value, self._error)

    def flatten(self: Result[Result[U, E], E]) -> Result[U, E]:
        if self.is_err:
            return Result.err(cast(E, self._error))
        return cast(Result[U, E], self._value)

    @classmethod
    def from_callable(
        cls,
        fn: Callable[P, T],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Result[T, Exception]:
        try:
            return Result(_is_ok=True, _value=fn(*args, **kwargs))
        except Exception as exc:  # noqa: BLE001
            return Result(_is_ok=False, _error=exc)

    @classmethod
    def combine(cls, results: Iterable[Result[T, E]]) -> Result[list[T], E]:
        values: list[T] = []
        for result in results:
            if result.is_err:
                return Result.err(result.unwrap_err())
            values.append(result.unwrap())
        return Result.ok(values)


def Ok(value: T) -> Result[T, Any]:
    return Result.ok(value)


def Err(error: E) -> Result[Any, E]:
    return Result.err(error)


def safe(fn: Callable[P, T]) -> Callable[P, Result[T, Exception]]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, Exception]:
        return Result.from_callable(fn, *args, **kwargs)

    return wrapper


__all__ = ["Err", "Ok", "Result", "safe"]
