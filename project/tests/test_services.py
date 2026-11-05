"""Stage 6 service checks: patient and practitioner lookup."""

import pytest

from smartcare.data_store import SmartCareDataStore
from datetime import datetime

from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def make_services() -> tuple[PatientService, PractitionerService]:
    """Create fresh services that share one new data store."""
    data_store = SmartCareDataStore()
    return PatientService(data_store), PractitionerService(data_store)


# --- FR-02: patient lookup -------------------------------------------------


def test_find_patient_returns_the_registered_object() -> None:
    """A registered ID returns the same stored patient object."""
    patients, _ = make_services()
    patient = patients.register_patient('P1', 'Alex Example')
    assert patients.find_patient('P1') is patient


def test_find_patient_unknown_id_raises_lookup_error() -> None:
    """A valid ID that nobody has raises LookupError."""
    patients, _ = make_services()
    with pytest.raises(LookupError):
        patients.find_patient('P999')


@pytest.mark.parametrize('bad_id', ['', '   ', None, 123])
def test_find_patient_blank_or_invalid_id_raises_value_error(bad_id) -> None:
    """A blank or non-text ID raises ValueError."""
    patients, _ = make_services()
    patients.register_patient('P1', 'Alex Example')
    with pytest.raises(ValueError):
        patients.find_patient(bad_id)


def test_find_patient_trims_surrounding_spaces() -> None:
    """Spaces around an ID are trimmed, so the patient is still found."""
    patients, _ = make_services()
    patient = patients.register_patient('P1', 'Alex Example')
    assert patients.find_patient('  P1  ') is patient


def test_find_patient_is_case_sensitive() -> None:
    """The wrong letter case is a different ID, so it is not found."""
    patients, _ = make_services()
    patients.register_patient('P1', 'Alex Example')
    with pytest.raises(LookupError):
        patients.find_patient('p1')


def test_find_patient_does_not_create_or_change_records() -> None:
    """A failed or successful lookup leaves the stored patients alone."""
    patients, _ = make_services()
    patient = patients.register_patient('P1', 'Alex Example')
    before = patients.data_store.list_patients()
    with pytest.raises(LookupError):
        patients.find_patient('P2')
    patients.find_patient('P1')
    assert patients.data_store.list_patients() == before == [patient]
    assert patient.patient_id == 'P1'
    assert patient.name == 'Alex Example'


# --- FR-02 supporting: practitioner lookup ---------------------------------


def test_find_practitioner_returns_the_registered_object() -> None:
    """A registered ID returns the same stored practitioner object."""
    _, practitioners = make_services()
    practitioner = practitioners.register_practitioner(
        'D1', 'Taylor Example', 'General practice',
    )
    assert practitioners.find_practitioner('D1') is practitioner


def test_find_practitioner_unknown_id_raises_lookup_error() -> None:
    """A valid ID that nobody has raises LookupError."""
    _, practitioners = make_services()
    with pytest.raises(LookupError):
        practitioners.find_practitioner('D999')


@pytest.mark.parametrize('bad_id', ['', '   ', None, 123])
def test_find_practitioner_blank_or_invalid_id_raises_value_error(
    bad_id,
) -> None:
    """A blank or non-text ID raises ValueError."""
    _, practitioners = make_services()
    practitioners.register_practitioner(
        'D1', 'Taylor Example', 'General practice',
    )
    with pytest.raises(ValueError):
        practitioners.find_practitioner(bad_id)


def test_find_practitioner_trims_surrounding_spaces() -> None:
    """Spaces around an ID are trimmed, so the practitioner is found."""
    _, practitioners = make_services()
    practitioner = practitioners.register_practitioner(
        'D1', 'Taylor Example', 'General practice',
    )
    assert practitioners.find_practitioner('  D1  ') is practitioner


def test_find_practitioner_is_case_sensitive() -> None:
    """The wrong letter case is a different ID, so it is not found."""
    _, practitioners = make_services()
    practitioners.register_practitioner(
        'D1', 'Taylor Example', 'General practice',
    )
    with pytest.raises(LookupError):
        practitioners.find_practitioner('d1')


def test_find_practitioner_does_not_create_or_change_records() -> None:
    """A failed or successful lookup leaves the stored practitioners alone."""
    _, practitioners = make_services()
    practitioner = practitioners.register_practitioner(
        'D1', 'Taylor Example', 'General practice',
    )
    before = practitioners.data_store.list_practitioners()
    with pytest.raises(LookupError):
        practitioners.find_practitioner('D2')
    practitioners.find_practitioner('D1')
    assert practitioners.data_store.list_practitioners() == before == [
        practitioner,
    ]
    assert practitioner.practitioner_id == 'D1'
    assert practitioner.name == 'Taylor Example'
    assert practitioner.specialty == 'General practice'


# --- FR-06 / FR-07: appointment cancellation -------------------------------


def make_appointment_services():
    """Create a booked appointment using one shared store."""
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)

    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner(
        'D1', 'Taylor Example', 'General practice',
    )
    appointment = appointments.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 12, 1, 10, 0),
    )
    return appointments, appointment


def test_cancel_appointment_changes_status_and_returns_same_object() -> None:
    """Cancellation returns the stored appointment with CANCELLED status."""
    appointments, appointment = make_appointment_services()

    result = appointments.cancel_appointment('A1')

    assert result is appointment
    assert appointment.status == AppointmentStatus.CANCELLED


def test_cancel_appointment_retains_history() -> None:
    """A cancelled appointment remains available in the shared store."""
    appointments, appointment = make_appointment_services()

    appointments.cancel_appointment('A1')

    assert appointments.find_appointment('A1') is appointment
    assert appointments.data_store.find_appointment('A1') is appointment
    assert appointment in appointments.data_store.list_appointments()


def test_cancel_appointment_unknown_id_raises_lookup_error() -> None:
    """An unknown appointment ID raises LookupError without changes."""
    appointments, appointment = make_appointment_services()

    with pytest.raises(LookupError):
        appointments.cancel_appointment('A999')

    assert appointment.status == AppointmentStatus.SCHEDULED
    assert appointments.data_store.list_appointments() == [appointment]


def test_cancel_appointment_repeated_attempt_raises_value_error() -> None:
    """Cancelling twice is rejected and retains the cancelled record."""
    appointments, appointment = make_appointment_services()
    appointments.cancel_appointment('A1')

    with pytest.raises(ValueError):
        appointments.cancel_appointment('A1')

    assert appointment.status == AppointmentStatus.CANCELLED
    assert appointments.find_appointment('A1') is appointment
    assert appointments.data_store.list_appointments() == [appointment]


@pytest.mark.parametrize('bad_id', ['', '   ', None, 123])
def test_cancel_appointment_invalid_id_raises_value_error(bad_id) -> None:
    """Invalid appointment IDs raise ValueError without changing records."""
    appointments, appointment = make_appointment_services()

    with pytest.raises(ValueError):
        appointments.cancel_appointment(bad_id)

    assert appointment.status == AppointmentStatus.SCHEDULED
    assert appointments.find_appointment('A1') is appointment