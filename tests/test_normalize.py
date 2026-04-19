from src.services.normalize import format_int, format_ratio, parse_float, parse_int


def test_parse_int_handles_commas():
    assert parse_int("1,234") == 1234
    assert parse_int("Gamerscore 85,420 points") == 85420


def test_parse_int_none_for_garbage():
    assert parse_int("--") is None
    assert parse_int(None) is None


def test_parse_float_two_decimals():
    assert parse_float("True Ratio 4.29") == 4.29


def test_format_int_commas():
    assert format_int(120000) == "120,000"
    assert format_int(None) == "--"


def test_format_ratio_rounds():
    assert format_ratio(4.2856) == "4.29"
    assert format_ratio("nope") == "--"
