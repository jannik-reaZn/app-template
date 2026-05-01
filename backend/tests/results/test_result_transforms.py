from app.core import Err, Ok, Result


class TestResultTransforms:
    def test_map_and_bind_short_circuit_errors(self) -> None:
        # GIVEN
        calls: list[int] = []

        def track(value: int) -> int:
            calls.append(value)
            return value * 2

        def half_if_even(value: int) -> Result[int, str]:
            if value % 2 == 0:
                return Ok(value // 2)
            return Err("not even")

        # WHEN
        success = Ok(4).map(track).and_then(half_if_even)
        failed = Err("bad input").map(track).and_then(half_if_even)

        # THEN
        assert success == Ok(4)
        assert calls == [4]
        assert failed == Err("bad input")
        assert calls == [4]

    def test_map_error_or_else_and_recover(self) -> None:
        # GIVEN
        error_result = Err("boom")
        ok_result = Ok(7)

        # WHEN
        mapped_error = error_result.map_error(str.upper)
        mapped_ok = ok_result.map_error(str.upper)
        recovered = Err("missing").or_else(lambda error: Ok(len(error)))
        recovered_length = Err("missing").recover(len)
        preserved_ok = Ok(3).recover(lambda _: 99)

        # THEN
        assert mapped_error == Err("BOOM")
        assert mapped_ok == Ok(7)
        assert recovered == Ok(7)
        assert recovered_length == Ok(7)
        assert preserved_ok == Ok(3)

    def test_tap_variants_and_match(self) -> None:
        # GIVEN
        seen_values: list[int] = []
        seen_errors: list[str] = []

        # WHEN
        ok_result = Ok(5).tap(seen_values.append).tap_error(seen_errors.append)
        err_result = Err("bad").tap(seen_values.append).tap_error(seen_errors.append)

        # THEN
        assert seen_values == [5]
        assert seen_errors == ["bad"]
        assert ok_result.match(lambda value: value * 2, str) == 10
        assert err_result.match(lambda value: str(value), str.upper) == "BAD"
