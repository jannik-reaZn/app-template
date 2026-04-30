import unittest

from app.core import Err, Ok, Result, safe


class ResultTests(unittest.TestCase):
    def test_ok_and_err_state_and_unwrap(self) -> None:
        ok_result = Ok(10)
        err_result = Err("boom")

        self.assertTrue(ok_result.is_ok)
        self.assertFalse(ok_result.is_err)
        self.assertEqual(ok_result.unwrap(), 10)
        self.assertEqual(ok_result.value, 10)

        self.assertTrue(err_result.is_err)
        self.assertFalse(err_result.is_ok)
        self.assertEqual(err_result.unwrap_err(), "boom")
        self.assertEqual(err_result.error, "boom")

        with self.assertRaisesRegex(ValueError, "unwrap an Err"):
            err_result.unwrap()

        with self.assertRaisesRegex(ValueError, "unwrap_err an Ok"):
            ok_result.unwrap_err()

    def test_map_and_bind_short_circuit_errors(self) -> None:
        calls: list[int] = []

        def track(value: int) -> int:
            calls.append(value)
            return value * 2

        def half_if_even(value: int) -> Result[int, str]:
            if value % 2 == 0:
                return Ok(value // 2)
            return Err("not even")

        self.assertEqual(Ok(4).map(track).and_then(half_if_even), Ok(4))
        self.assertEqual(calls, [4])

        failed = Err("bad input").map(track).and_then(half_if_even)
        self.assertEqual(failed, Err("bad input"))
        self.assertEqual(calls, [4])

    def test_map_error_or_else_and_recover(self) -> None:
        self.assertEqual(Err("boom").map_error(str.upper), Err("BOOM"))
        self.assertEqual(Ok(7).map_error(str.upper), Ok(7))

        recovered = Err("missing").or_else(lambda error: Ok(len(error)))
        self.assertEqual(recovered, Ok(7))

        self.assertEqual(Err("missing").recover(len), Ok(7))
        self.assertEqual(Ok(3).recover(lambda _: 99), Ok(3))

    def test_tap_variants_and_match(self) -> None:
        seen_values: list[int] = []
        seen_errors: list[str] = []

        ok_result = Ok(5).tap(seen_values.append).tap_error(seen_errors.append)
        err_result = Err("bad").tap(seen_values.append).tap_error(seen_errors.append)

        self.assertEqual(seen_values, [5])
        self.assertEqual(seen_errors, ["bad"])
        self.assertEqual(ok_result.match(lambda value: value * 2, str), 10)
        self.assertEqual(err_result.match(lambda value: str(value), str.upper), "BAD")

    def test_flatten_and_combine(self) -> None:
        nested = Ok(Ok("ready"))
        self.assertEqual(nested.flatten(), Ok("ready"))

        combined = Result.combine([Ok(1), Ok(2), Ok(3)])
        self.assertEqual(combined, Ok([1, 2, 3]))

        failed = Result.combine([Ok(1), Err("stop"), Ok(3)])
        self.assertEqual(failed, Err("stop"))

    def test_from_callable_and_safe_capture_exceptions(self) -> None:
        def divide(dividend: int, divisor: int) -> float:
            return dividend / divisor

        safe_divide = safe(divide)

        self.assertEqual(Result.from_callable(divide, 10, 2), Ok(5.0))

        failure = safe_divide(10, 0)
        self.assertTrue(failure.is_err)
        self.assertIsInstance(failure.unwrap_err(), ZeroDivisionError)
        self.assertEqual(failure.unwrap_or(99), 99)
        self.assertEqual(failure.unwrap_or_else(lambda exc: len(str(exc))), 16)


if __name__ == "__main__":
    unittest.main()
