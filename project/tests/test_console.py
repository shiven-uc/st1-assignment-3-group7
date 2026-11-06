"""Stage 9 interactive console tests."""

from unittest.mock import patch

import pytest

from smartcare.console import parse_date_time, run_menu


@pytest.mark.parametrize("invalid_date", [
    "tomorrow",
    "2026-02-30 09:00",
    "2026/12/01 09:00",
])
def test_invalid_date_rejected(invalid_date):
    with pytest.raises(ValueError):
        parse_date_time(invalid_date)


def test_menu_recovers_from_invalid_input(capsys):
    inputs = [
        "99",                   # Invalid menu choice
        "1", "", "Blank Name",  # Invalid patient ID
        "1", "P1", "Alex Example",
        "2", "P1",              # Successful lookup after errors
        "0",
    ]

    with patch("builtins.input", side_effect=inputs):
        run_menu()

    output = capsys.readouterr().out

    assert "Invalid menu choice" in output
    assert "Patient ID cannot be blank" in output
    assert "Patient registered: P1" in output
    assert "Patient found: P1" in output
    assert "Goodbye" in output


def test_menu_retains_cancelled_history(capsys):
    inputs = [
        "1", "P1", "Alex Example",
        "3", "D1", "Taylor Example", "General",
        "5", "A1", "P1", "D1", "2026-12-01 09:00",
        "6", "A1",
        "7", "A1",
        "8", "D1", "",           # All statuses
        "8", "D1", "scheduled",  # Excludes cancelled appointment
        "0",
    ]

    with patch("builtins.input", side_effect=inputs):
        run_menu()

    output = capsys.readouterr().out

    assert "Booked: A1" in output
    assert "Cancelled: A1" in output
    assert "Found: A1" in output
    assert "cancelled" in output
    assert "No matching appointments." in output
    assert "Goodbye" in output
