"""Unit tests for library_eligibility.can_borrow.

Requirements under test (see library_loans-specification.pdf):
  GR-2/GR-3  Wrong data type (incl. bool)        -> TypeError
  GR-4       Correct type, outside range (< 0)   -> ValueError
  FR2.1      Allowed only when active_loans < 5 AND overdue_books == 0
  FR2.2      Not allowed when active_loans >= 5 OR overdue_books > 0
  FR2-OUT    Return value is a Python bool

Test IDs (TC-E-xx) match the Test Case Specification document.
"""
import pytest

from library_eligibility import can_borrow


# ---------- Allowed to borrow ----------
@pytest.mark.parametrize(
    "active_loans, overdue_books",
    [
        pytest.param(0, 0, id="TC-E-01_no_loans_no_overdue"),
        pytest.param(3, 0, id="TC-E-02_typical_allowed"),
        pytest.param(4, 0, id="TC-E-03_four_loans_upper_boundary_allowed"),
    ],
)
def test_can_borrow_under_limit_and_no_overdue_returns_true(active_loans, overdue_books):
    assert can_borrow(active_loans, overdue_books) is True


# ---------- Not allowed to borrow ----------
@pytest.mark.parametrize(
    "active_loans, overdue_books",
    [
        pytest.param(5, 0, id="TC-E-04_five_loans_limit_reached"),
        pytest.param(6, 0, id="TC-E-05_above_limit"),
        pytest.param(0, 1, id="TC-E-06_one_overdue_book"),
        pytest.param(4, 1, id="TC-E-07_under_limit_but_overdue"),
        pytest.param(5, 2, id="TC-E-08_both_conditions_fail"),
    ],
)
def test_can_borrow_limit_reached_or_overdue_returns_false(active_loans, overdue_books):
    assert can_borrow(active_loans, overdue_books) is False


def test_can_borrow_returns_bool():
    """TC-E-09: Output must be a Python bool."""
    assert type(can_borrow(1, 0)) is bool


# ---------- Invalid range: correct type but negative -> ValueError ----------
@pytest.mark.parametrize(
    "active_loans, overdue_books",
    [
        pytest.param(-1, 0, id="TC-E-10_negative_active_loans"),
        pytest.param(0, -1, id="TC-E-11_negative_overdue_books"),
    ],
)
def test_can_borrow_negative_values_raise_value_error(active_loans, overdue_books):
    with pytest.raises(ValueError):
        can_borrow(active_loans, overdue_books)


# ---------- Invalid type -> TypeError ----------
@pytest.mark.parametrize(
    "active_loans, overdue_books",
    [
        pytest.param(2.0, 0, id="TC-E-12_float_active_loans"),
        pytest.param(0, "1", id="TC-E-13_string_overdue_books"),
        pytest.param(None, 0, id="TC-E-14_none_active_loans"),
        pytest.param(True, 0, id="TC-E-15_bool_active_loans"),
        pytest.param(0, False, id="TC-E-16_bool_overdue_books"),
    ],
)
def test_can_borrow_invalid_type_raises_type_error(active_loans, overdue_books):
    with pytest.raises(TypeError):
        can_borrow(active_loans, overdue_books)
