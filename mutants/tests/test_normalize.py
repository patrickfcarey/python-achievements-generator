from src.services.normalize import (
    clamp,
    format_int,
    format_ratio,
    parse_float,
    parse_int,
)


def test_parse_int_handles_commas():
    assert parse_int("1,234") == 1234
    assert parse_int("Gamerscore 85,420 points") == 85420


def test_parse_int_none_for_garbage():
    assert parse_int("--") is None
    assert parse_int(None) is None


def test_parse_int_truncates_decimals():
    assert parse_int("4.99") == 4


def test_parse_int_accepts_non_string_inputs():
    assert parse_int(42) == 42


def test_parse_int_negative():
    assert parse_int("-7 kills") == -7


def test_parse_float_two_decimals():
    assert parse_float("True Ratio 4.29") == 4.29


def test_parse_float_none_input():
    assert parse_float(None) is None


def test_parse_float_no_match():
    assert parse_float("nothing numeric") is None


def test_parse_float_handles_commas():
    assert parse_float("1,234.5") == 1234.5


def test_format_int_commas():
    assert format_int(120000) == "120,000"
    assert format_int(None) == "--"


def test_format_int_handles_float_value():
    assert format_int(3.7) == "3"


def test_format_int_bad_string():
    assert format_int("abc") == "--"


def test_format_ratio_rounds():
    assert format_ratio(4.2856) == "4.29"
    assert format_ratio("nope") == "--"


def test_format_ratio_custom_decimals():
    assert format_ratio(4.2856, decimals=3) == "4.286"


def test_format_ratio_none_value():
    assert format_ratio(None) == "--"


def test_clamp_within_range():
    assert clamp(5, 0, 10) == 5


def test_clamp_below_low():
    assert clamp(-3, 0, 10) == 0


def test_clamp_above_high():
    assert clamp(42, 0, 10) == 10
