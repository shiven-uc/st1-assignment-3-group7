# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: Group 7 Wednesday 2:30-4:30
Members and responsibilities: Shiven - Stage 9 design, implementation, testing, documentation and Git integration. Anish Atamkur - peer review and feedback, with specific contributions to be recorded as completed.
Stage 8 integrated SHA, command, working directory and actual result: 2688f7792b9235d756ae2b9f559003cf7671fc3a. Ran python -m pytest -q from project/: 50 passed, 0 failed in 0.13s. The working tree was clean.

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity | Required session/domain state | Patient IDs and names must remain available for registration, lookup and appointments. |
| Appointment history | Required session/domain state | FR-07 requires cancelled appointment history to remain retrievable during the session. |
| Temporary menu choice | Transient state | Used only to select the current console operation. |
| Practitioner specialty | Required session/domain state | Specialty is part of the registered practitioner's information. |
| Debug print output | Transient state | Diagnostic output is not part of the SmartCare domain or stored records. |
| Appointment status | Required session/domain state | SCHEDULED, CANCELLED and COMPLETED statuses are needed for appointment lookup and filtering. |

What is intentionally lost on exit? SmartCare uses an in-memory data store, so patient, practitioner and appointment records are not persisted after the application exits. Temporary menu selections, user input and debug output are also discarded. No database or file persistence is required in Stage 9

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key | appointment: Appointment | Tuple of date_time and appointment_id | Produces a sorting key without modifying the appointment | Appointment.date_time and Appointment.appointment_id |
| select_appointments | Appointment collection, optional practitioner ID and optional status | New list[Appointment] | Filters and sorts appointments without changing the original collection | QRY-01–04; all statuses included by default |
| Service listing | Practitioner ID and optional status | list[Appointment] or error | Validates inputs, distinguishes unknown practitioners from empty results, and calls the query function | FP-01–03; SmartCareDataStore |
| Console | Menu choice and user-entered values | Displayed results or error messages | Handles input/output, converts dates and statuses, calls services and handles invalid input | UI-01–02; existing SmartCare services |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: Patients and practitioners have unique, nonblank IDs and required names. Practitioners also have a required specialty. Appointments have unique IDs and reference actual registered Patient and Practitioner objects. Dates use local minute-precision datetime values, and statuses use the existing AppointmentStatus enum. Queries must preserve these values, object identities and appointment history.

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input | Domain object handling console input | Appointment.cancel should only change and validate appointment status. The console handles user input. |
| Service prints/reads the menu | Service layer performing user interface operations | Services should coordinate business operations and return results or errors. The console handles menus and printing. |
| Query sorts its source in place | Pure query mutating the original collection | Queries should return a new sorted list without changing the original collection or appointments. |
| Store prints Appointment saved | Data store performing presentation logic | SmartCareDataStore should manage stored records. The console should display confirmation messages. |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: appointments.sort(key=appointment_sort_key) modifies the original list in place and returns None. Any variable referencing that list sees the changed order.

result = sorted(appointments, key=appointment_sort_key) creates a new sorted list while leaving the original list unchanged. The result contains references to the same Appointment objects.

A meaningful mutation check is to save the original appointment ID order, call sorted(), and assert that the source order is unchanged, the returned list is a different object, and its elements are the same stored Appointment objects.

Score-example prediction and explanation of passing the named key: For appointments with the same date/time, appointment_sort_key uses the appointment ID to break the tie. For example, appointments A2 and A1 at 9:00 AM should be ordered A1, then A2. An earlier appointment should appear before both.

Passing the named appointment_sort_key function to sorted() provides consistent date/time ordering and an appointment-ID tie-break without duplicating sorting logic or modifying the original collection.

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: Cancellation changes an appointment's status from SCHEDULED to CANCELLED, while deletion removes the appointment entirely.

SmartCare requires cancelled appointments to remain stored and retrievable during the same session (FR-07 / AC-05.2).

To verify this, I would book an appointment, cancel it, and check that:
- Looking up its ID returns the original appointment with CANCELLED status.
- Listing appointments without a status filter includes the cancelled appointment.
- Listing only SCHEDULED appointments excludes the cancelled appointment.
- The original appointment remains in the data store, with its ID and participant references unchanged.

This verifies that cancellation preserves appointment history rather than deleting records.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: The Stage 9 design will preserve the existing SmartCare domain model and shared in-memory data store.

Pure query functions will receive appointment collections and filters explicitly, return new sorted lists, and never modify stored records.

The service layer will validate practitioner IDs, distinguish unknown practitioners from known practitioners with no appointments, and coordinate query operations.

The console will handle menus, input conversion, output and recoverable errors without putting presentation logic into domain objects or the data store.

These decisions preserve registered participant identities, appointment history, and the existing booking and cancellation requirements.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| QRY-01 | Collection of Appointment objects | appointment_sort_key generates a sorting key | Appointments ordered by date/time, then appointment ID | Planned: test appointment sorting |
| QRY-02 | Appointment collection and optional practitioner ID | select_appointments filters by practitioner | Only matching practitioner's appointments returned | Planned: test practitioner filtering |
| QRY-03 | Appointment collection and optional status | select_appointments filters by AppointmentStatus | Matching status returned; no filter includes all statuses | Planned: test status filtering |
| QRY-04 | Appointment collection and filter values | Pure query returns a new sorted list | Original list, appointment fields and object identities unchanged | Planned: test query purity |
| FP-01 | Known practitioner ID | Service retrieves appointments through the query function | Sorted appointment list, including an empty list when appropriate | Planned: test service listing |
| FP-02 | Unknown or invalid practitioner ID | Service validates and checks the practitioner | Appropriate error; existing records unchanged | Planned: test invalid practitioner lookup |
| FP-03 | Optional status filter | Service validates status and delegates filtering | Correct filtered results or validation error | Planned: test service status filtering |
| UI-01 | Valid menu choices and user inputs | Console calls existing SmartCare services | Registration, lookup, booking, cancellation and listing work in one session | Planned: console workflow test |
| UI-02 | Invalid menu choices and inputs | Console catches expected errors and allows retry | Clear error message; program continues without corrupting state | Planned: console recovery test |
| FR-01–FR-08 | Existing registered records and appointment operations | Existing domain, store and service methods | Existing requirements remain satisfied | Existing regression suite: 50 passed before Stage 9 |
| FR-09 | Registered practitioner and appointment records | Service provides appointment listing | Appointment listings satisfy the Stage 9 contract | Planned: listing integration test |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: An empty result for a registered practitioner means no appointments match the filters and should return an empty list. An unknown practitioner ID must be distinguished from this case, while blank or invalid identifiers must be rejected according to the service validation contract.

The console should convert valid status input into the existing AppointmentStatus enum and valid date/time input into a local minute-precision datetime. Invalid values should produce clear errors without modifying stored records.

Appointments must reference the actual registered Patient and Practitioner objects, preserving object identity. Query results should contain those same Appointment objects in a new list, without copying or changing their fields.

Errors must be handled at the correct layer. Domain objects enforce invariants, services validate and coordinate operations, queries perform side-effect-free selection and sorting, and the console displays results and handles user input. Rejected operations must leave the existing SmartCare state unchanged.

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| | | | | |

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: <!-- response -->
What the tests do and do not establish: <!-- response -->

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | `python main.py --interactive`; registered P1, D1/D2; booked A1, attempted conflicting booking, booked A2, cancelled A1, retrieved and filtered appointments, then booked A3 | Registration and lookup succeed; same-practitioner conflict is rejected; different-practitioner booking succeeds; cancelled history is retained; freed slot can be reused | Manually verified: all scenarios behaved as expected, although console message wording differed from the examples. A1 remained CANCELLED and A3 booked successfully. | Manual terminal run; GitHub link to be added |
| UI-02 invalid-input recovery | `python main.py --interactive`; invalid menu choice 99, blank patient ID, unknown P999, duplicate P1, impossible date 2026-02-30, malformed date, unknown A999, invalid status banana, repeated cancellation and valid A1 retry | Invalid inputs are rejected without terminating the session or creating partial records; valid actions still succeed afterward | Manual testing completed. Terminal output confirmed errors for menu choice, blank/unknown/duplicate patient IDs and invalid dates. Remaining cases were reported completed; exact output not separately captured. | Manual terminal evidence; GitHub link pending |
| Automated service workflow | `python -m pytest tests/test_workflows.py -v`; `tests/test_workflows.py` | Verify booking, conflict rejection, different-practitioner booking, cancellation history, filtering, freed-slot reuse and unchanged state after rejected operations | PASS — 3 workflow tests passed. Full regression: 71 passed, 0 failed. Tests verified stored-object identity, cancellation history and rejected-booking state preservation. | `project/tests/test_workflows.py`; GitHub link pending |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: <!-- reference -->
Actual prompt/context supplied: <!-- paste or accessible reference -->
Actual response: <!-- accessible reference -->

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| | | | | | |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: <!-- response -->

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? <!-- response -->
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->
3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- response -->

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? <!-- response -->
2. Which explicit inputs are needed, and why avoid a global store? <!-- response -->
3. How can a new list reuse Appointment objects safely? <!-- response -->
4. Why use a named key, and what breaks equal-time ties? <!-- response -->
5. How do default and explicit status filters differ? <!-- response -->
6. How do empty, unknown practitioner and invalid filter cases differ? <!-- response -->
7. Which console errors recover, and how is unchanged state checked? <!-- response -->
8. What is data integrity for registered participants, conflicts and history? <!-- response -->
9. What is Copilot's review role, and who verifies findings? <!-- response -->
10. How do pure functions and OOP responsibilities work together? <!-- response -->

## H. Review, completion and common handover

Issues and bounded branches: <!-- links -->
PR/diff and another-member human reviewer: <!-- actual links/name -->
Review responses and Copilot comparison: <!-- links -->
Integrated common Stage 9 SHA: <!-- complete -->
Full regression command, working directory, actual count/result and evidence: <!-- complete -->
README run instructions and scope/limitations: <!-- link -->
Unresolved issues and support/action: <!-- complete -->
UG common candidate / PG future branch plan: <!-- complete -->

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
