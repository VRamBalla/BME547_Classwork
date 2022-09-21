import pytest


@pytest.mark.parametrize("input_one, expected", [
    (85, "Normal"),
    (45, "Borderline Low"),
    (25, "Low")])
def test_check_HDL(input_one, expected):
    from blood_calculator import check_HDL
    answer = check_HDL(input_one)
    assert answer == expected
