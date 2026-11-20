"""Unit tests for library_fine.calculate_fine.

Requirements under test (see library_loans-specification.pdf):
  GR-2/GR-3  Wrong data type (incl. bool)       -> TypeError
  GR-4       Correct type, outside range (< 0)  -> ValueError
  FR1.1      Fine = 50 cents x days overdue
  FR1.2      0 days -> 0 fine; NO maximum fine
  FR1-OUT    Return value is an int (cents)

Test IDs (TC-F-xx) match the Test Case Specification document.
"""
import pytest

from library_fine import calculate_fine


# ---------- Valid inputs: equivalence partitions + boundary values ----------
@pytest.mark.parametrize(
    "days_overdue, expected_fine",
    [
        pytest.param(0, 0, id="TC-F-01_zero_days_lower_boundary"),
        pytest.param(1, 50, id="TC-F-02_one_day_just_above_boundary"),
        pytest.param(5, 250, id="TC-F-03_typical_value"),
        pytest.param(10, 500, id="TC-F-04_ten_days"),
        pytest.param(11, 550, id="TC-F-05_eleven_days_no_cap"),
        pytest.param(100, 5000, id="TC-F-06_large_value_no_maximum"),
    ],
)
def test_calculate_fine_valid_days_returns_50_cents_per_day(days_overdue, expected_fine):
    # Act
    result = calculate_fine(days_overdue)
    # Assert
    assert result == expected_fine


def test_calculate_fine_returns_int():
    """TC-F-07: Output must be an integer number of cents."""
    result = calculate_fine(3)
    assert type(result) is int


# ---------- Invalid range: correct type but negative -> ValueError ----------
@pytest.mark.parametrize(
    "days_overdue",
    [
        pytest.param(-1, id="TC-F-08_minus_one_just_below_boundary"),
        pytest.param(-100, id="TC-F-09_large_negative"),
    ],
)
def test_calculate_fine_negative_days_raises_value_error(days_overdue):
    with pytest.raises(ValueError):
        calculate_fine(days_overdue)


# ---------- Invalid type -> TypeError ----------
@pytest.mark.parametrize(
    "days_overdue",
    [
        pytest.param(1.5, id="TC-F-10_float"),
        pytest.param("3", id="TC-F-11_string"),
        pytest.param(None, id="TC-F-12_none"),
        pytest.param(True, id="TC-F-13_bool_true"),
        pytest.param(False, id="TC-F-14_bool_false"),
    ],
)
def test_calculate_fine_invalid_type_raises_type_error(days_overdue):
    with pytest.raises(TypeError):
        calculate_fine(days_overdue)
