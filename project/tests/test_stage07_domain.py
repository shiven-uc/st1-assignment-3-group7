
"""Stage 7 domain validation and state-transition tests."""

from datetime import datetime

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)


# DOM-01: Valid patient construction
def test_valid_patient_construction():
    patient = Patient(' P1 ', ' Alex Example ')

    assert patient.patient_id == 'P1'
    assert patient.name == 'Alex Example'


# DOM-02: Invalid patient construction
@pytest.mark.parametrize(
    'patient_id,name',
    [
        ('   ', 'Alex Example'),
        ('P1', '   '),
    ],
)
def test_invalid_patient_construction(patient_id, name):
    with pytest.raises(ValueError):
        Patient(patient_id, name)


# DOM-03: Practitioner construction and validation
def test_practitioner_validation():
    practitioner = Practitioner(' D1 ', ' Taylor Example ', ' General ')

    assert practitioner.practitioner_id == 'D1'
    assert practitioner.name == 'Taylor Example'
    assert practitioner.specialty == 'General'

    with pytest.raises(ValueError):
        Practitioner('D2', 'Taylor Example', '   ')

    with pytest.raises(ValueError):
        Practitioner('   ', 'Taylor Example', 'General')


# DOM-04: Appointment construction and initial status
def test_appointment_initial_status():
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    when = datetime(2026, 12, 1, 9, 0)

    appointment = Appointment('A1', patient, practitioner, when)

    assert appointment.appointment_id == 'A1'
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.date_time == when
    assert appointment.status is AppointmentStatus.SCHEDULED


# DOM-05: Valid cancellation
def test_appointment_cancellation():
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    appointment = Appointment(
        'A1', patient, practitioner, datetime(2026, 12, 1, 9, 0)
    )

    appointment.cancel()

    assert appointment.status is AppointmentStatus.CANCELLED


# DOM-06: Invalid status transitions
def test_invalid_appointment_transitions():
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    when = datetime(2026, 12, 1, 9, 0)

    cancelled = Appointment('A1', patient, practitioner, when)
    cancelled.cancel()

    with pytest.raises(ValueError):
        cancelled.cancel()

    assert cancelled.status is AppointmentStatus.CANCELLED

    completed = Appointment(
        'A2', patient, practitioner, when,
        status=AppointmentStatus.COMPLETED
    )

    with pytest.raises(ValueError):
        completed.cancel()

    assert completed.status is AppointmentStatus.COMPLETED

