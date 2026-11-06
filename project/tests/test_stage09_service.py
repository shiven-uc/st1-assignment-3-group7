
"""Stage 9 appointment service listing tests."""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus, Patient, Practitioner
from smartcare.services import AppointmentService


def setup_service():
    store = SmartCareDataStore()
    store.add_patient(Patient("P1", "Alex Example"))
    store.add_practitioner(
        Practitioner("D1", "Taylor Example", "General")
    )
    store.add_practitioner(
        Practitioner("D2", "Morgan Example", "Dental")
    )
    return AppointmentService(store)


def test_known_practitioner_without_appointments():
    service = setup_service()

    result = service.list_practitioner_appointments("D1")

    assert result == []
    assert result is not service.data_store.list_appointments()


def test_unknown_practitioner():
    service = setup_service()

    with pytest.raises(LookupError):
        service.list_practitioner_appointments("D999")


def test_blank_practitioner_id():
    service = setup_service()

    with pytest.raises(ValueError):
        service.list_practitioner_appointments("   ")


def test_invalid_status():
    service = setup_service()

    with pytest.raises(ValueError):
        service.list_practitioner_appointments("D1", "scheduled")


def test_listing_uses_registered_practitioner_id():
    service = setup_service()

    appointment = service.book_appointment(
        "A1", "P1", "D1", datetime(2026, 12, 1, 9, 0)
    )

    result = service.list_practitioner_appointments(" D1 ")

    assert len(result) == 1
    assert result[0] is appointment


def test_cancelled_history_remains_listable():
    service = setup_service()

    appointment = service.book_appointment(
        "A1", "P1", "D1", datetime(2026, 12, 1, 9, 0)
    )

    cancelled = service.cancel_appointment("A1")

    all_results = service.list_practitioner_appointments("D1")
    scheduled_results = service.list_practitioner_appointments(
        "D1", AppointmentStatus.SCHEDULED
    )
    cancelled_results = service.list_practitioner_appointments(
        "D1", AppointmentStatus.CANCELLED
    )

    assert cancelled is appointment
    assert service.find_appointment("A1") is appointment
    assert appointment.status is AppointmentStatus.CANCELLED
    assert all_results == [appointment]
    assert scheduled_results == []
    assert cancelled_results == [appointment]


def test_failed_listing_preserves_existing_appointments():
    service = setup_service()

    appointment = service.book_appointment(
        "A1", "P1", "D1", datetime(2026, 12, 1, 9, 0)
    )

    with pytest.raises(LookupError):
        service.list_practitioner_appointments("D999")

    with pytest.raises(ValueError):
        service.list_practitioner_appointments("D1", "invalid")

    assert service.find_appointment("A1") is appointment
    assert appointment.status is AppointmentStatus.SCHEDULED
