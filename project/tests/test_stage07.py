import pytest
from datetime import datetime

from smartcare.domain import AppointmentStatus
from smartcare.services import AppointmentService, PractitionerService
from smartcare.data_store import SmartCareDataStore
from smartcare.services import PatientService


# TEST-01: FR-01 / AC-01.1
def test_register_valid_patient():
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)

    patient = patients.register_patient('P100', 'Alex Example')

    assert patient.patient_id == 'P100'
    assert patient.name == 'Alex Example'
    assert data_store.find_patient('P100') is patient
    assert data_store.list_patients() == [patient]


# TEST-02: FR-01 / AC-01.2
def test_duplicate_patient_preserves_original():
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)

    original = patients.register_patient('P100', 'Alex Example')

    with pytest.raises(ValueError):
        patients.register_patient('P100', 'Different Name')

    assert data_store.find_patient('P100') is original
    assert original.name == 'Alex Example'
    assert data_store.list_patients() == [original]


# TEST-03: FR-01 / Public validation contract
def test_blank_patient_id_rejected():
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)

    with pytest.raises(ValueError):
        patients.register_patient('   ', 'Alex Example')

    assert data_store.list_patients() == []


# TEST-04: FR-04 / AC-03.1
def test_valid_booking():
    store = SmartCareDataStore()
    patient = PatientService(store).register_patient('P1', 'Alex Example')
    practitioner = PractitionerService(store).register_practitioner(
        'D1', 'Taylor Example', 'General'
    )
    appointments = AppointmentService(store)
    when = datetime(2026, 12, 1, 9, 0)

    appointment = appointments.book_appointment('A1', 'P1', 'D1', when)

    assert appointment.appointment_id == 'A1'
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.date_time == when
    assert appointment.status is AppointmentStatus.SCHEDULED
    assert store.find_appointment('A1') is appointment


# TEST-05: FR-05 / AC-04.1
def test_same_practitioner_time_conflict():
    store = SmartCareDataStore()
    patients = PatientService(store)
    patients.register_patient('P1', 'Alex Example')
    patients.register_patient('P2', 'Sam Example')
    PractitionerService(store).register_practitioner(
        'D1', 'Taylor Example', 'General'
    )
    appointments = AppointmentService(store)
    when = datetime(2026, 12, 1, 9, 0)

    original = appointments.book_appointment('A1', 'P1', 'D1', when)

    with pytest.raises(ValueError):
        appointments.book_appointment('A2', 'P2', 'D1', when)

    assert store.list_appointments() == [original]
    assert store.find_appointment('A1') is original
    assert original.status is AppointmentStatus.SCHEDULED


# TEST-06: FR-05 / AC-04.2
def test_different_practitioners_same_time():
    store = SmartCareDataStore()
    PatientService(store).register_patient('P1', 'Alex Example')
    practitioners = PractitionerService(store)
    practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    practitioners.register_practitioner('D2', 'Morgan Example', 'Dental')
    appointments = AppointmentService(store)
    when = datetime(2026, 12, 1, 9, 0)

    first = appointments.book_appointment('A1', 'P1', 'D1', when)
    second = appointments.book_appointment('A2', 'P1', 'D2', when)

    assert first.status is AppointmentStatus.SCHEDULED
    assert second.status is AppointmentStatus.SCHEDULED
    assert first.practitioner.practitioner_id == 'D1'
    assert second.practitioner.practitioner_id == 'D2'
    assert store.list_appointments() == [first, second]


# TEST-07: FR-06 / AC-05.1
def test_cancel_scheduled_appointment():
    store = SmartCareDataStore()
    PatientService(store).register_patient('P1', 'Alex Example')
    PractitionerService(store).register_practitioner(
        'D1', 'Taylor Example', 'General'
    )
    appointments = AppointmentService(store)
    appointment = appointments.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 12, 1, 9, 0)
    )

    result = appointments.cancel_appointment('A1')

    assert result is appointment
    assert appointment.status is AppointmentStatus.CANCELLED


# TEST-08: FR-07 / AC-05.2
def test_cancelled_appointment_retained():
    store = SmartCareDataStore()
    PatientService(store).register_patient('P1', 'Alex Example')
    PractitionerService(store).register_practitioner(
        'D1', 'Taylor Example', 'General'
    )
    appointments = AppointmentService(store)
    original = appointments.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 12, 1, 9, 0)
    )

    appointments.cancel_appointment('A1')

    assert appointments.find_appointment('A1') is original
    assert store.find_appointment('A1') is original
    assert store.list_appointments() == [original]
    assert original.status is AppointmentStatus.CANCELLED


# TEST-09: FR-06 / AC-05.3
def test_repeated_cancellation_rejected():
    store = SmartCareDataStore()
    PatientService(store).register_patient('P1', 'Alex Example')
    PractitionerService(store).register_practitioner(
        'D1', 'Taylor Example', 'General'
    )
    appointments = AppointmentService(store)
    original = appointments.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 12, 1, 9, 0)
    )
    appointments.cancel_appointment('A1')

    with pytest.raises(ValueError):
        appointments.cancel_appointment('A1')

    assert original.status is AppointmentStatus.CANCELLED
    assert store.find_appointment('A1') is original
    assert store.list_appointments() == [original]
