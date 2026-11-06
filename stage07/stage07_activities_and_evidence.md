# Stage 7 Testing and Verification Record

Group/tutorial: [complete]  Members/cohorts: [complete]
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| FR-01 Register patient | Register a patient with a unique ID and a valid name. |  a unique ID and a valid name.

Attempt to register another patient using an ID that is already registered. | The valid patient is stored and retrievable; duplicate registration raises ValueError and does not replace the existing patient. |
| FR-05 Prevent practitioner conflict | Book two appointments at the same date/time with different practitioners. | Attempt to book two SCHEDULED appointments for the same practitioner at exactly the same date/time. | Different practitioners can be booked simultaneously; the conflicting booking raises ValueError and leaves existing appointments unchanged. |
| FR-06 Cancel appointment | Cancel an existing SCHEDULED appointment. | Attempt to cancel an appointment that is already CANCELLED. | The first cancellation changes status to CANCELLED; repeated cancellation raises ValueError. |
| FR-07 Retain cancelled history | Cancel an appointment and retrieve it using its original ID. | Check whether cancellation incorrectly removes the appointment from the data store. | The retrieved appointment is the same object (is) and its status remains AppointmentStatus.CANCELLED. |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: [Weak/unclear]  Why: This always passes and checks no application behaviour. It cannot detect an incorrect result

`assert appointment is not None`
Judgement: [Weak/unclear]  Why: This only confirms an object exists. It does not prove the appointment has the correct ID, participants, date/time or status.

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: [Strong for stated behaviour]  Why: This directly checks that the appointment's status is CANCELLED, as required by FR-06. However, it does not prove the appointment remains stored or that invalid transitions are rejected.

`assert len(results) > 0`
Judgement: [Weak/unclear]  Why: This only proves the results collection is not empty. It does not establish that the correct appointments were returned or that filtering and ordering are correct.

`assert data_store.find_appointment('A1') is appointment`
Judgement: [Strong for stated behaviour]  Why: This checks that retrieving appointment A1 returns the exact same object, supporting FR-07's retained-history requirement. However, it does not prove that the object's status is CANCELLED; a separate status assertion is needed.

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract: 1. Blank identifiers: If a patient, practitioner or appointment ID is blank or contains only whitespace, the system should reject it with `ValueError`. This tests the domain validation rules requiring valid identifiers.

- Whitespace-only names: If a patient or practitioner name contains only spaces, the system should reject it with `ValueError`. This tests the required-name validation associated with FR-01 and FR-03.

- Same-time practitioner bookings: If two scheduled appointments are booked for the same practitioner at exactly the same date and time, the second booking should be rejected with `ValueError`. The first booking should remain unchanged. This tests FR-05.

- Cancelled appointments: After cancelling an appointment, it should remain stored and retrievable using its original ID, with status `CANCELLED`. This tests FR-07.

- Invalid status transitions: If an appointment is already cancelled, attempting to cancel it again should raise `ValueError`, leaving its status unchanged. This tests FR-06.

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 (is not None) | Only checks that an object exists, not that its data is correct. | Verify that a registered patient has the correct ID and name. |
| 2 (is not None) | Does not verify the appointment's actual properties or behaviour. | Verify that a booked appointment has the correct practitioner, patient and scheduled status. |
| 3 (assert True) | Always passes and does not test anything. | Verify that cancelling an appointment changes its status to CANCELLED. |
| 4 (SMS notification) | Invents SMS functionality that is not required. | Test that a conflicting booking for the same practitioner and time is rejected. |
| 5 (SMS notification) | Tests functionality outside the SmartCare requirements. | Verify that a cancelled appointment remains stored and retrievable. |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?

100% code coverage only means that every line of code was executed during testing. It does not mean the tests checked whether the program behaved correctly. Tests with weak assertions, such as `assert True` or `assert appointment is not None`, can pass even when the program produces incorrect results. Good verification requires meaningful assertions that check the actual requirements, including negative cases and boundary conditions.

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| FR-01 | AC-01.1 | TEST-01 | Positive | tests/test_stage07.py::test_register_valid_patient | Valid patient is registered and stored with correct ID and name. | PASS - 43 passed in 0.05s (full suite) | Student-authored |
| FR-01 | AC-01.2 | TEST-02 | Negative | Planned: tests/test_stage07.py::test_duplicate_patient_preserves_original | Duplicate patient ID raises ValueError without replacing the existing patient. | Planned - not run | Student-authored (planned) |
| FR-01 | Public validation contract: IDs must be non-blank | TEST-03 | Boundary | Planned: tests/test_stage07.py::test_blank_patient_id_rejected | Blank patient ID raises ValueError. | Planned - not run | Student-authored (planned) |
| FR-04 | AC-03.1 | TEST-04 | Positive | Planned: tests/test_stage07.py::test_valid_booking | A valid booking creates a stored SCHEDULED appointment. | Planned - not run | Student-authored (planned) |
| FR-05 | AC-04.1 | TEST-05 | Negative | Planned: tests/test_stage07.py::test_same_practitioner_time_conflict | Booking the same practitioner at the exact same time raises ValueError and preserves the original appointment. | Planned - not run | Student-authored (planned) |
| FR-05 | AC-04.2 | TEST-06 | Positive | Planned: tests/test_stage07.py::test_different_practitioners_same_time | Different practitioners can have appointments at the same time. | Planned - not run | Student-authored (planned) |
| FR-06 | AC-05.1 | TEST-07 | Positive | Planned: tests/test_stage07.py::test_cancel_scheduled_appointment | Cancelling a scheduled appointment changes its status to CANCELLED. | Planned - not run | Student-authored (planned) |
| FR-07 | AC-05.2 | TEST-08 | Positive | Planned: tests/test_stage07.py::test_cancelled_appointment_retained | A cancelled appointment remains stored and retrievable as the same object. | Planned - not run | Student-authored (planned) |
| FR-06 | AC-05.3 | TEST-09 | Negative | Planned: tests/test_stage07.py::test_repeated_cancellation_rejected | Cancelling an already cancelled appointment raises ValueError without changing its state. | Planned - not run | Student-authored (planned) |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| TEST-01 | FR-01 | AC-01.1 | Positive | test_register_valid_patient: Register a patient with a unique ID and valid name. | Patient is stored with the correct ID and name. | Checks the stored patient details rather than only checking that registration returned an object. |
| TEST-02 | FR-01 | AC-01.2 | Negative | test_duplicate_patient_preserves_original: Attempt to register another patient with an existing ID. | ValueError is raised and the original patient remains unchanged. | Checks that rejection preserves existing data, not just that an exception occurs. |
| TEST-03 | FR-01 | Public validation contract: IDs must be non-blank | Boundary | test_blank_patient_id_rejected: Attempt registration with a whitespace-only ID. | ValueError is raised and no patient is registered. | Tests the whitespace boundary and verifies that invalid input does not change stored data. |
| TEST-04 | FR-04 | AC-03.1 | Positive | test_valid_booking: Book an appointment with registered participants at an available time. | A SCHEDULED appointment is stored with the correct patient, practitioner and time. | Checks the appointment's actual details and stored status. |
| TEST-05 | FR-05 | AC-04.1 | Negative | test_same_practitioner_time_conflict: Attempt two scheduled bookings for the same practitioner at the exact same time. | ValueError is raised and the original appointment remains unchanged. | Verifies both conflict rejection and preservation of existing state. |
| TEST-06 | FR-05 | AC-04.2 | Positive | test_different_practitioners_same_time: Book different practitioners at the same time. | Both appointments are successfully stored. | Confirms that conflicts are practitioner-specific. |
| TEST-07 | FR-06 | AC-05.1 | Positive | test_cancel_scheduled_appointment: Cancel an existing scheduled appointment. | Its status changes from SCHEDULED to CANCELLED. | Checks the actual status transition. |
| TEST-08 | FR-07 | AC-05.2 | Positive | test_cancelled_appointment_retained: Retrieve an appointment after cancellation. | The same appointment object remains stored with CANCELLED status. | Verifies retained history and object identity. |
| TEST-09 | FR-06 | AC-05.3 | Negative | test_repeated_cancellation_rejected: Attempt to cancel an already cancelled appointment. | ValueError is raised and the appointment remains CANCELLED. | Verifies invalid transition rejection without state mutation. |


## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| TEST-01 | Empty data store; valid patient ID and name. | Register the patient. | Check the stored patient's ID and name match the inputs. | Proves correct patient registration, not just object creation. |
| TEST-02 | Register an existing patient. | Attempt registration with the same ID and a different name. | pytest.raises(ValueError); verify the original patient is unchanged. | Proves duplicate rejection without overwriting data. |
| TEST-03 | Empty data store; patient ID contains only spaces. | Attempt patient registration. | pytest.raises(ValueError); verify no patient was stored. | Proves invalid IDs are rejected without changing state. |
| TEST-04 | Register a patient and practitioner; choose an available datetime. | Book an appointment. | Check stored appointment ID, participants, datetime and SCHEDULED status. | Proves a valid booking creates the correct appointment. |
| TEST-05 | Register patients and one practitioner; book the first appointment. | Attempt another booking for the same practitioner and datetime. | pytest.raises(ValueError); verify the first appointment remains unchanged. | Proves conflicting bookings are rejected without modifying existing data. |
| TEST-06 | Register patients and two different practitioners. | Book both practitioners at the same datetime. | Check both appointments exist with SCHEDULED status. | Proves simultaneous bookings are allowed for different practitioners. |
| TEST-07 | Create a SCHEDULED appointment. | Cancel the appointment. | Check appointment.status == AppointmentStatus.CANCELLED. | Proves cancellation changes the appointment's status. |
| TEST-08 | Create and cancel an appointment. | Retrieve it using its original ID. | Check the retrieved object is the original appointment and its status is CANCELLED. | Proves cancellation retains the original appointment in storage. |
| TEST-09 | Create and cancel an appointment. | Attempt to cancel it again. | pytest.raises(ValueError); verify status remains CANCELLED. | Proves repeated cancellation is rejected without changing state. |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| DOM-01 | Valid patient construction and whitespace trimming | tests/test_stage07_domain.py::test_valid_patient_construction | PASS |
| DOM-02 | Blank patient ID and whitespace-only name rejected | tests/test_stage07_domain.py::test_invalid_patient_construction | PASS (2 parameterised cases) |
| DOM-03 | Practitioner construction and required-field validation | tests/test_stage07_domain.py::test_practitioner_validation | PASS |
| DOM-04 | Appointment construction and initial SCHEDULED status | tests/test_stage07_domain.py::test_appointment_initial_status | PASS |
| DOM-05 | Scheduled appointment cancellation changes status to CANCELLED | tests/test_stage07_domain.py::test_appointment_cancellation | PASS |
| DOM-06 | Repeated cancellation and COMPLETED-to-CANCELLED transition rejected | tests/test_stage07_domain.py::test_invalid_appointment_transitions | PASS |


## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| TEST-01 | Register a valid patient and verify stored details | FR-01 / AC-01.1 | tests/test_stage07.py::test_register_valid_patient | PASS |
| TEST-02 | Reject duplicate patient ID without overwriting original | FR-01 / AC-01.2 | tests/test_stage07.py::test_duplicate_patient_preserves_original | PASS |
| TEST-03 | Reject whitespace-only patient ID | FR-01 / Public validation contract | tests/test_stage07.py::test_blank_patient_id_rejected | PASS |
| TEST-04 | Book an appointment with registered participants | FR-04 / AC-03.1 | tests/test_stage07.py::test_valid_booking | PASS |
| TEST-05 | Reject same-practitioner booking conflict | FR-05 / AC-04.1 | tests/test_stage07.py::test_same_practitioner_time_conflict | PASS |
| TEST-06 | Allow different practitioners at the same time | FR-05 / AC-04.2 | tests/test_stage07.py::test_different_practitioners_same_time | PASS |
| TEST-07 | Cancel scheduled appointment and verify CANCELLED status | FR-06 / AC-05.1 | tests/test_stage07.py::test_cancel_scheduled_appointment | PASS |
| TEST-08 | Retain and retrieve cancelled appointment | FR-07 / AC-05.2 | tests/test_stage07.py::test_cancelled_appointment_retained | PASS |
| TEST-09 | Reject repeated cancellation without changing state | FR-06 / AC-05.3 | tests/test_stage07.py::test_repeated_cancellation_rejected | PASS |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| Duplicate patient registration | Existing patient ID 'P100' used again | ValueError; original patient remains unchanged | TEST-02 |
| Blank patient ID | Whitespace-only ID '   ' | ValueError; no patient is stored | TEST-03 |
| Same-practitioner booking conflict | Two appointments for practitioner D1 at the exact same datetime | ValueError; original appointment remains stored and SCHEDULED | TEST-05 |
| Repeated appointment cancellation | Attempt to cancel an already CANCELLED appointment | ValueError; appointment remains CANCELLED and retrievable | TEST-09 |
| Invalid patient construction | Whitespace-only patient ID or name | ValueError; invalid Patient object is not constructed | DOM-02 |
| Invalid practitioner construction | Whitespace-only practitioner ID or specialty | ValueError; invalid Practitioner object is not constructed | DOM-03 |
| Illegal appointment transition | Attempt to cancel an appointment with COMPLETED status | ValueError; appointment remains COMPLETED | DOM-06 |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: FR-05 — Prevent conflicting practitioner bookings.
Acceptance criterion: AC-04.1 — "Same practitioner/exact time/SCHEDULED conflicts."
Behaviour to test: Attempting to book a second SCHEDULED appointment for the same practitioner at the exact same date and time must raise ValueError without changing the existing appointment.
Human-first test idea/categories: Negative test. Register two patients and one practitioner, then book an appointment. Attempt a second booking for the same practitioner and time using a different appointment ID and patient. Assert ValueError and verify that the original appointment remains stored and SCHEDULED.
Prompt and purpose: Ask GitHub Copilot to suggest additional pytest cases and meaningful assertions for AC-04.1, then review the suggestions against the requirement. Do not automatically accept generated code.
For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: A cancelled appointment does not block the same practitioner and time slot. Cancel the original appointment, then book a new appointment for the same practitioner and exact time.
- What it claims to verify: Only SCHEDULED appointments cause booking conflicts. The original cancelled appointment remains stored, and the new appointment is stored as SCHEDULED.
- Requirement trace: FR-05 / AC-04.1, with supporting relevance to FR-07 / AC-05.2.
- Assertion quality: Strong proposed assertions because they check both appointment statuses and confirm both records remain stored.
- Human critique: This is a useful additional case. It follows the SCHEDULED-only conflict rule and does not invent new scheduling restrictions. It would need a distinct appointment ID for the replacement booking.
- Decision: Accept (test idea only; not implemented).
- Reason: The proposed test covers a meaningful boundary of the conflict rule and checks observable state.
- Final test reference if accepted/modified: Not implemented or retained as a test.
- Actual verification result: Not run. Copilot supplied a test idea, not an executed test.

- Copilot test idea/candidate: Two appointments for the same practitioner at different exact times should both be allowed.
- What it claims to verify: The booking conflict rule uses exact date/time equality rather than blocking other times for the same practitioner.
- Requirement trace: FR-05 / AC-04.1.
- Assertion quality: Strong proposed assertions because they check that both appointments are stored, remain SCHEDULED, and retain their requested date/time.
- Human critique: The suggestion correctly avoids inventing appointment durations or overlapping-time restrictions. It is relevant but less important than the cancelled-slot case because it tests ordinary non-conflicting bookings.
- Decision: Accept (test idea only; not implemented).
- Reason: It provides useful additional coverage of the exact-time conflict boundary without introducing unsupported rules.
- Final test reference if accepted/modified: Not implemented or retained as a test.
- Actual verification result: Not run. Copilot supplied a test idea, not an executed test.

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? Copilot candidate 2: allowing two appointments for the same practitioner at different exact times. The suggestion was valid, but it was weaker than the cancelled-slot test.
Why was it weak? It checks that two non-conflicting bookings succeed, but it does not directly challenge the rejection behaviour in AC-04.1. A booking implementation that incorrectly allows conflicting appointments could still pass this test. Therefore, the test alone would not adequately verify conflict prevention.
How did you strengthen it? I reviewed the proposed assertions and identified the need to pair this positive case with a negative test. My existing TEST-05 checks that booking the same practitioner at the exact same time raises ValueError and preserves the original appointment. Together, the two test ideas cover both sides of the exact-time conflict rule. I did not implement Copilot candidate 2 as an additional test.
Accepted / modified / rejected test decisions and evidence: See Section H, Copilot candidates 1 and 2. Both ideas were accepted as valid suggestions but were not implemented or executed. Candidate 2 was identified as weaker in isolation and was evaluated against the existing student-authored TEST-05. The existing full test suite passed 50 tests; this result does not include either Copilot suggestion.

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| `python -m pytest -q` | `project/` | `2d991d7f62069729a4fb2e85f4d3f6c624e2e735` (baseline HEAD; Stage 7 changes uncommitted) | 50 | 0 | None | No failures observed | Full regression suite passed in 0.06s, including 34 existing and 16 new Stage 7 test executions. |
| `python -m pytest tests/test_stage07.py tests/test_stage07_domain.py -v` | `project/` | Same baseline HEAD with uncommitted Stage 7 changes | 16 | 0 | None | No failures observed | All 9 service tests and 7 domain test executions passed in 0.08s. |

- Individual test runs and changed-order independence evidence: Earlier service-test run: 9 passed. Combined Stage 7 run: 16 passed. Changed-order independence not yet tested.

- Optional tutor-led demonstration notes: Not performed.

A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.

- Requirement → test → failure/observation → diagnosis → change → verification: FR-05 / AC-04.1 → TEST-05 → Conflicting booking correctly rejected → No defect observed → No change required → Full regression suite passed (50 tests).

## K What the Suite Still Does Not Prove

What does your test suite still not prove? Although all 50 tests pass, the suite does not prove that SmartCare is completely defect-free. The tests verify selected requirements and validation rules, but they do not cover every possible input, combination of operations, or unexpected failure. Some tests also overlap with existing tests, so the number of passing tests does not necessarily represent 50 unique behaviours.
Coverage if used: Not used. No code coverage measurement was performed.
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? Additional testing could examine invalid date/time inputs, non-string identifiers, invalid appointment participants, and more combinations of registration, booking and cancellation. These matter because invalid data or incorrect state transitions could affect appointment records.
Even 100% code coverage would not guarantee correctness. Coverage measures which code executes, not whether assertions properly verify the acceptance criteria. A test can execute a line without detecting incorrect behaviour.
Optional fixtures/parametrisation used and why, if any: Pytest parametrisation was used in test_invalid_patient_construction to check two invalid inputs: a whitespace-only patient ID and a whitespace-only patient name. This allowed the same validation behaviour to be tested against multiple cases without duplcating test code. Tests also used fresh SmartCare data stores to avoid unwanted shared state between test cases.

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| Stage 7 testing and verification | `stage07-testing` | Pending PR | Pending review | Pending feedback | 50 tests passed locally; Git review pending |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| [complete] | [complete] | [complete] |

## N Formative Questions

1. What question does verification answer?
[response]

2. What question does validation answer?
[response]

3. What is a unit test?
[response]

4. What is a pytest fixture?
[response]

5. What is parametrisation in pytest?
[response]

6. What is regression testing?
[response]

7. What does code coverage tell us, and what does it not prove?
[response]

8. What makes an assertion weak?
[response]

9. What is the appropriate role of GitHub Copilot as a test assistant?
[response]

10. What is the Stage 7 engineering rule?
[response]

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
