import pytest

from app.core import Err, Ok


class TestResultState:
    def test_ok_and_err_state_and_unwrap(self) -> None:
        # GIVEN
        ok_result = Ok(10)
        err_result = Err("boom")

        # WHEN / THEN
        assert ok_result.is_ok is True
        assert ok_result.is_err is False
        assert ok_result.unwrap() == 10
        assert ok_result.value == 10

        assert err_result.is_err is True
        assert err_result.is_ok is False
        assert err_result.unwrap_err() == "boom"
        assert err_result.error == "boom"

        # THEN
        with pytest.raises(ValueError, match="unwrap an Err"):
            err_result.unwrap()

        with pytest.raises(ValueError, match="unwrap_err an Ok"):
            ok_result.unwrap_err()
