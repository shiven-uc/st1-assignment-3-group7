"""Stage 9 integrated SmartCare workflow tests."""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def setup_services():
    """Create services sharing one in-memory data store."""
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    appointments = AppointmentService(store)

    patients.register_patient("P1", "Alex Example")
    practitioners.register_practitioner("D1", "Taylor Example", "General")
    practitioners.register_practitioner("D2", "Morgan Example", "Dental")

    return store, patients, practitioners, appointments


def test_full_booking_cancellation_and_rebooking_workflow():
    store, patients, practitioners, service = setup_services()
    time = datetime(2026, 12, 1, 9, 0)

    patient = patients.find_patient("P1")
    doctor1 = practitioners.find_practitioner("D1")
    doctor2 = practitioners.find_practitioner("D2")

    a1 = service.book_appointment("A1", "P1", "D1", time)

    assert a1.patient is patient
    assert a1.practitioner is doctor1
    assert a1.status is AppointmentStatus.SCHEDULED

    # Same practitioner and time must be rejected.
    with pytest.raises(ValueError):
        service.book_appointment("A-CONFLICT", "P1", "D1", time)

    assert store.find_appointment("A-CONFLICT") is None
    assert service.find_appointment("A1") is a1

    # Another practitioner at the same time is permitted.
    a2 = service.book_appointment("A2", "P1", "D2", time)
    assert a2.practitioner is doctor2

    # Cancellation retains the original appointment.
    cancelled = service.cancel_appointment("A1")
    assert cancelled is a1
    assert service.find_appointment("A1") is a1
    assert a1.status is AppointmentStatus.CANCELLED

    # All-status listing includes cancelled history.
    all_results = service.list_practitioner_appointments("D1")
    assert all_results == [a1]
    assert all_results[0] is a1

    scheduled = service.list_practitioner_appointments(
        "D1", AppointmentStatus.SCHEDULED
    )
    assert scheduled == []

    # Cancellation frees the time for a new appointment ID.
    a3 = service.book_appointment("A3", "P1", "D1", time)
    assert a3.status is AppointmentStatus.SCHEDULED

    final_results = service.list_practitioner_appointments("D1")
    assert [a.appointment_id for a in final_results] == ["A1", "A3"]
    assert final_results[0] is a1
    assert final_results[1] is a3


def test_duplicate_and_unknown_bookings_preserve_state():
    store, _, _, service = setup_services()
    time = datetime(2026, 12, 1, 9, 0)

    original = service.book_appointment("A1", "P1", "D1", time)
    before = list(store.list_appointments())

    with pytest.raises(ValueError):
        service.book_appointment("A1", "P1", "D2", time)

    with pytest.raises(LookupError):
        service.book_appointment("A2", "P999", "D1", time)

    with pytest.raises(LookupError):
        service.book_appointment("A3", "P1", "D999", time)

    after = store.list_appointments()

    assert after == before
    assert len(after) == 1
    assert after[0] is original
    assert original.status is AppointmentStatus.SCHEDULED
    assert store.find_appointment("A2") is None
    assert store.find_appointment("A3") is None


def test_repeated_cancellation_retains_history():
    _, _, _, service = setup_services()
    time = datetime(2026, 12, 1, 9, 0)

    appointment = service.book_appointment("A1", "P1", "D1", time)
    service.cancel_appointment("A1")

    with pytest.raises(ValueError):
        service.cancel_appointment("A1")

    assert service.find_appointment("A1") is appointment
    assert appointment.status is AppointmentStatus.CANCELLED

    cancelled = service.list_practitioner_appointments(
        "D1", AppointmentStatus.CANCELLED
    )
    assert cancelled == [appointment]
