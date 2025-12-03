from src.common.utils import camel_to_snake, snake_to_camel


def test_camel_to_snake():
    """Test camel_to_snake function."""
    assert camel_to_snake("camelCaseTest") == "camel_case_test"

    assert camel_to_snake("word") == "word"
    assert camel_to_snake("") == ""
    assert camel_to_snake("A") == "a"


def test_snake_to_camel():
    """Test snake_to_camel function."""
    assert snake_to_camel("snake_case_test") == "snakeCaseTest"

    assert snake_to_camel("word") == "word"
    assert snake_to_camel("") == ""
    assert snake_to_camel("_test") == "Test"


def test_round_trip_conversion():
    """Test that conversions are reversible for common cases."""

    camel_case = "camelCaseTest"
    assert snake_to_camel(camel_to_snake(camel_case)) == camel_case

    snake_case = "snake_case_test"
    assert camel_to_snake(snake_to_camel(snake_case)) == snake_case
