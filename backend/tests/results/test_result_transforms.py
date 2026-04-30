from app.core import Err, Ok, Result


class TestResultTransforms:
    def test_map_and_bind_short_circuit_errors(self) -> None:
        calls: list[int] = []

        def track(value: int) -> int:
            calls.append(value)
            return value * 2

        def half_if_even(value: int) -> Result[int, str]:
            if value % 2 == 0:
                return Ok(value // 2)
            return Err("not even")

        assert Ok(4).map(track).and_then(half_if_even) == Ok(4)
        assert calls == [4]

        failed = Err("bad input").map(track).and_then(half_if_even)
        assert failed == Err("bad input")
        assert calls == [4]

    def test_map_error_or_else_and_recover(self) -> None:
        assert Err("boom").map_error(str.upper) == Err("BOOM")
        assert Ok(7).map_error(str.upper) == Ok(7)

        recovered = Err("missing").or_else(lambda error: Ok(len(error)))
        assert recovered == Ok(7)

        assert Err("missing").recover(len) == Ok(7)
        assert Ok(3).recover(lambda _: 99) == Ok(3)

    def test_tap_variants_and_match(self) -> None:
        seen_values: list[int] = []
        seen_errors: list[str] = []

        ok_result = Ok(5).tap(seen_values.append).tap_error(seen_errors.append)
        err_result = Err("bad").tap(seen_values.append).tap_error(seen_errors.append)

        assert seen_values == [5]
        assert seen_errors == ["bad"]
        assert ok_result.match(lambda value: value * 2, str) == 10
        assert err_result.match(lambda value: str(value), str.upper) == "BAD"
