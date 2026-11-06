
"""Stage 9 pure query tests."""

from datetime import datetime
import pytest

from smartcare.domain import Appointment, AppointmentStatus, Patient, Practitioner
from smartcare.queries import appointment_sort_key, select_appointments


def make_appointments():
    patient = Patient("P1", "Alex Example")
    d1 = Practitioner("D1", "Taylor Example", "General")
    d2 = Practitioner("D2", "Morgan Example", "Dental")

    a3 = Appointment("A3", patient, d1, datetime(2026, 12, 2, 10, 0))
    a2 = Appointment("A2", patient, d1, datetime(2026, 12, 1, 9, 0),
                     status=AppointmentStatus.CANCELLED)
    a1 = Appointment("A1", patient, d1, datetime(2026, 12, 1, 9, 0),
                     status=AppointmentStatus.COMPLETED)
    other = Appointment("A4", patient, d2, datetime(2026, 12, 1, 8, 0))

    return [a3, other, a2, a1]


def test_named_sort_key():
    appointment = make_appointments()[0]
    assert appointment_sort_key(appointment) == (
        datetime(2026, 12, 2, 10, 0), "A3"
    )


def test_practitioner_isolation():
    appointments = make_appointments()
    result = select_appointments(appointments, "D2")
    assert [a.appointment_id for a in result] == ["A4"]


def test_default_includes_every_status():
    result = select_appointments(make_appointments(), "D1")
    assert [a.appointment_id for a in result] == ["A1", "A2", "A3"]
    assert {a.status for a in result} == {
        AppointmentStatus.SCHEDULED,
        AppointmentStatus.CANCELLED,
        AppointmentStatus.COMPLETED,
    }


@pytest.mark.parametrize("status,expected", [
    (AppointmentStatus.SCHEDULED, ["A3"]),
    (AppointmentStatus.CANCELLED, ["A2"]),
    (AppointmentStatus.COMPLETED, ["A1"]),
])
def test_explicit_status_filter(status, expected):
    result = select_appointments(make_appointments(), "D1", status)
    assert [a.appointment_id for a in result] == expected


def test_no_matches_returns_new_empty_list():
    appointments = make_appointments()
    result = select_appointments(appointments, "D999")
    assert result == []
    assert result is not appointments


def test_source_and_objects_unchanged():
    appointments = make_appointments()
    original_order = list(appointments)
    original_fields = [
        (a.appointment_id, a.date_time, a.status, a.patient, a.practitioner)
        for a in appointments
    ]

    result = select_appointments(appointments, "D1")

    assert result is not appointments
    assert appointments == original_order
    assert [
        (a.appointment_id, a.date_time, a.status, a.patient, a.practitioner)
        for a in appointments
    ] == original_fields
    assert result[0] is original_order[3]
    assert result[1] is original_order[2]
    assert result[2] is original_order[0]


def test_repeated_calls_are_consistent():
    appointments = make_appointments()
    first = select_appointments(appointments, "D1")
    second = select_appointments(appointments, "D1")

    assert first == second
    assert first is not second
    assert all(a is b for a, b in zip(first, second))


def test_empty_and_already_sorted_inputs():
    empty = []
    empty_result = select_appointments(empty, "D1")
    assert empty_result == []
    assert empty_result is not empty

    original = select_appointments(make_appointments(), "D1")
    result = select_appointments(original, "D1")

    assert result == original
    assert result is not original
    assert all(a is b for a, b in zip(result, original))


def test_select_appointments_uses_named_sort_key(monkeypatch):
    import smartcare.queries as queries

    appointments = make_appointments()
    calls = []
    original_key = queries.appointment_sort_key

    def tracking_key(appointment):
        calls.append(appointment.appointment_id)
        return original_key(appointment)

    monkeypatch.setattr(queries, "appointment_sort_key", tracking_key)

    result = queries.select_appointments(appointments, "D1")

    assert [a.appointment_id for a in result] == ["A1", "A2", "A3"]
    assert sorted(calls) == ["A1", "A2", "A3"]
