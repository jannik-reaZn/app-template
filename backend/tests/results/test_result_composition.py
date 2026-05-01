from app.core import Err, Ok, Result, safe


class TestResultComposition:
    def test_flatten_and_combine(self) -> None:
        # GIVEN
        nested = Ok(Ok("ready"))

        # WHEN
        flattened = nested.flatten()
        combined = Result.combine([Ok(1), Ok(2), Ok(3)])
        failed = Result.combine([Ok(1), Err("stop"), Ok(3)])

        # THEN
        assert flattened == Ok("ready")
        assert combined == Ok([1, 2, 3])
        assert failed == Err("stop")

    def test_from_callable_and_safe_capture_exceptions(self) -> None:
        # GIVEN
        def divide(dividend: int, divisor: int) -> float:
            return dividend / divisor

        safe_divide = safe(divide)

        # WHEN
        success = Result.from_callable(divide, 10, 2)
        failure = safe_divide(10, 0)

        # THEN
        assert success == Ok(5.0)
        assert failure.is_err is True
        assert isinstance(failure.unwrap_err(), ZeroDivisionError)
        assert failure.unwrap_or(99) == 99
        assert failure.unwrap_or_else(lambda exc: len(str(exc))) == 16
