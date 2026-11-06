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
| QRY-01 | Appointment collection and practitioner ID | Pure query selects appointments for the requested practitioner | Only matching practitioner's appointments returned | `test_practitioner_isolation` |
| QRY-02 | Appointment collection and optional AppointmentStatus | Pure query applies optional status filtering | Default includes every status; explicit filters select matching status; no matches returns empty list | `test_default_includes_every_status`, `test_explicit_status_filter` |
| QRY-03 | Appointment collection | Named key sorts by date/time and appointment ID | Correct ascending order without changing source order or fields | `test_named_sort_key`, `test_source_and_objects_unchanged` |
| QRY-04 | Practitioner ID and optional status | AppointmentService validates practitioner and status, then delegates to query | Known-empty returns []; unknown ID raises LookupError; invalid ID or non-enum status raises ValueError | `tests/test_stage09_service.py` |
| FP-01 | Explicit appointment collection and filters | Pure query processes inputs without hidden state or I/O | Repeated inputs produce equivalent results without side effects | `test_repeated_calls_are_consistent`; code inspection |
| FP-02 | Empty, sorted and unsorted appointment lists | Pure query returns a new list containing existing Appointment objects | Different list identity; original objects and source unchanged | `test_empty_and_already_sorted_inputs`, `test_source_and_objects_unchanged` |
| FP-03 | Appointment objects | `appointment_sort_key` provides the reusable sorting key | Named key is tested directly and used by sorting | `test_named_sort_key`, `test_select_appointments_uses_named_sort_key` |
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
| QRY-01 / test_practitioner_isolation | `smartcare/queries.py`; `tests/test_queries.py` | D2 listing contains only A4, excluding D1 appointments | PASS — query tests passed | `project/tests/test_queries.py` |
| QRY-02 / test_default_includes_every_status | `smartcare/queries.py`; `tests/test_queries.py` | Default filter includes SCHEDULED, CANCELLED and COMPLETED | PASS | `project/tests/test_queries.py` |
| QRY-02 / test_explicit_status_filter | `smartcare/queries.py`; `tests/test_queries.py` | Each enum status returns matching appointments only | PASS — 3 parameterised cases | `project/tests/test_queries.py` |
| QRY-03 / test_source_and_objects_unchanged | `smartcare/queries.py`; `tests/test_queries.py` | Checks sorted ID order, unchanged source and fields, and original object identity | PASS | `project/tests/test_queries.py` |
| FP-01 / test_repeated_calls_are_consistent | `smartcare/queries.py`; `tests/test_queries.py` | Repeated calls produce equivalent results in distinct lists | PASS | `project/tests/test_queries.py` |
| FP-02 / test_empty_and_already_sorted_inputs | `smartcare/queries.py`; `tests/test_queries.py` | Empty and already-sorted inputs produce fresh lists containing unchanged objects | PASS | `project/tests/test_queries.py` |
| FP-03 / test_named_sort_key | `smartcare/queries.py`; `tests/test_queries.py` | Directly checks the date/time and appointment-ID sorting key | PASS | `project/tests/test_queries.py` |
| FP-03 / test_select_appointments_uses_named_sort_key | `smartcare/queries.py`; `tests/test_queries.py` | Monkeypatch verifies the query invokes the named sorting key | PASS | `project/tests/test_queries.py` |
| QRY-04 / Stage 9 service tests | `smartcare/services.py`; `tests/test_stage09_service.py` | Checks known-empty, unknown/blank practitioner, invalid status, whitespace, cancelled history and unchanged state | PASS — 7 tests | `project/tests/test_stage09_service.py` |
| Integrated workflow tests | `tests/test_workflows.py` | Checks conflicts, registered-object identity, different-practitioner booking, cancellation, filtering and freed-slot reuse | PASS — 3 tests | `project/tests/test_workflows.py` |

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: The appointment_sort_key function only reads the appointment's date/time and ID and returns a tuple.

The select_appointments function receives all required data through its parameters. It filters appointments into a new list and uses sorted() with the named appointment_sort_key function.

Neither function accesses a global data store, reads input, prints output, or changes the original collection or appointment objects. Repeated calls with unchanged inputs produce equivalent results. The returned list is new, but it contains references to the original Appointment objects.
What the tests do and do not establish: The tests verify practitioner isolation, default and explicit status filtering, date/time sorting with appointment-ID tie-breaking, repeated calls, fresh result lists and unchanged source objects.

The service tests verify known-empty results, invalid and unknown practitioner IDs, invalid status values and retained cancelled history.

The workflow tests verify booking conflicts, registered-object identity, cancellation, filtering, freed-slot rebooking and unchanged state after rejected bookings.

The full regression suite passed all 71 tests. However, passing tests cannot prove the absence of every possible defect or side effect. Code inspection is also necessary to check that the query functions contain no hidden state, input/output or mutation.

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | `python main.py --interactive`; registered P1, D1/D2; booked A1, attempted conflicting booking, booked A2, cancelled A1, retrieved and filtered appointments, then booked A3 | Registration and lookup succeed; same-practitioner conflict is rejected; different-practitioner booking succeeds; cancelled history is retained; freed slot can be reused | Manually verified: all scenarios behaved as expected, although console message wording differed from the examples. A1 remained CANCELLED and A3 booked successfully. | Manual terminal run; GitHub link to be added |
| UI-02 invalid-input recovery | `python main.py --interactive`; invalid menu choice 99, blank patient ID, unknown P999, duplicate P1, impossible date 2026-02-30, malformed date, unknown A999, invalid status banana, repeated cancellation and valid A1 retry | Invalid inputs are rejected without terminating the session or creating partial records; valid actions still succeed afterward | Manual testing completed. Terminal output confirmed errors for menu choice, blank/unknown/duplicate patient IDs and invalid dates. Remaining cases were reported completed; exact output not separately captured. | Manual terminal evidence; GitHub link pending |
| Automated service workflow | `python -m pytest tests/test_workflows.py -v`; `tests/test_workflows.py` | Verify booking, conflict rejection, different-practitioner booking, cancellation history, filtering, freed-slot reuse and unchanged state after rejected operations | PASS — 3 workflow tests passed. Full regression: 71 passed, 0 failed. Tests verified stored-object identity, cancellation history and rejected-booking state preservation. | `project/tests/test_workflows.py`; GitHub link pending |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: Commit `051b16d9d76013169e34f4874019def8dba3b257` — Stage 9 human-first design and contracts.
Actual prompt/context supplied: Act as a query and console integration reviewer for my SmartCare Stage 9 university project.

Review these files:

- `smartcare/queries.py`
- `smartcare/services.py`
- `smartcare/console.py`
- `tests/test_queries.py`
- `tests/test_stage09_service.py`
- `tests/test_workflows.py`
The current regression suite has 71 passing tests.

Check:

1. Explicit inputs, purity and source non-mutation.
2. Domain, service, data-store and console responsibilities.
3. Validation and recovery without partial state changes.
4. Correct object identity, enum filtering and ordering.
5. Retained cancellation history and integrity risks.
6. Missing query, workflow or console tests.
Do not redesign the domain or add databases, persistence or frameworks. Do not invent fields or delete cancelled appointment history.

Separate confirmed issues from optional improvements. Rank findings as Critical, Important or Optional. For each finding, identify the relevant code and test evidence.

Please review the actual files rather than assuming how they work.
Actual response: GitHub Copilot reviewed queries.py, services.py, console.py, the Stage 9 tests, domain.py and data_store.py. It ran `python -m pytest -q` and reported 71 passing tests. It found no Critical runtime defect, identified missing automated console tests as an Important coverage gap, and raised direct data-store conflict enforcement as an Optional hardening suggestion. Full response retained in the VS Code Copilot chat titled "SmartCare Stage 9 Review".

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
|| Missing automated console tests | `console.py`; Copilot identified that no automated tests directly exercised `run_menu()` or date parsing | Important | Accept — automated console tests strengthen regression coverage alongside manual UI-01 and UI-02 verification | Added `tests/test_console.py` covering invalid dates, menu recovery and cancelled history | PASS — 5 console tests passed; full regression 76 passed, 0 failed |
| Direct store writes bypass service conflict check | `services.py` checks conflicts before booking; `data_store.py` does not independently reject conflicting scheduled appointments | Optional | Reject for Stage 9 — normal booking uses the service; changing store responsibilities is unnecessary for the assessed workflow | No change | Existing service conflict test passed; 71-test regression passed |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: SmartCare separates responsibilities between its components. Domain objects enforce valid values and appointment cancellation rules. SmartCareDataStore holds registered patients, practitioners and appointments in shared in-memory collections. Services coordinate registration, lookup, booking, cancellation and validated appointment listing. The query functions filter and sort explicitly supplied appointments without mutation or input/output. The console handles menu choices, input conversion, output messages and recoverable errors while delegating business operations to services. Copilot's review found no Critical runtime defects, but identified missing automated console coverage as an Important improvement.

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? The main architectural concern was ensuring every menu operation used the same SmartCareDataStore throughout the session. If the console created a new store for each operation, registered participants and appointments would not remain available for later lookup, cancellation or listing. The console must coordinate interaction through services while the store preserves shared session state. This is an architectural concern rather than a sorting detail.
2. Which Copilot suggestion did you reject as over-engineering, and why? I rejected Copilot's optional suggestion to add scheduling conflict enforcement directly to data-store writes. The existing AppointmentService already checks practitioner conflicts before booking, and the workflow tests verify that conflicting appointments are rejected without partial insertion. Changing the store would expand the implementation beyond the required Stage 9 service workflow. The suggestion may be useful for future hardening, but it was unnecessary for this stage.
3. How did you prove cancelled appointments remain retrievable and listable in the same session? I booked appointment A1 for practitioner D1, cancelled it, and then retrieved it again using its appointment ID. The console displayed A1 with CANCELLED status. An all-status practitioner listing included A1, while a SCHEDULED-only listing excluded it. I then successfully booked A3 into the freed time slot. Automated service, workflow and console tests also verified cancelled history, filtering and retained appointment identity. The full regression suite passed 76 tests.

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity?
select_appointments is pure because it uses only its supplied inputs, returns a new filtered and sorted list, and does not modify the original appointments. Changing the source list, modifying appointment objects, printing output or accessing a global store would break purity.
2. Which explicit inputs are needed, and why avoid a global store?

The function receives a list of Appointment objects, a practitioner ID and an optional AppointmentStatus. Avoiding a global store makes its behaviour predictable, reusable and easier to test independently.

3. How can a new list reuse Appointment objects safely?
A new list can contain references to the original Appointment objects without copying them. This is safe for the query because it only reads their fields and never modifies them. The query therefore preserves the original objects and their identities.

4. Why use a named key, and what breaks equal-time ties?
appointment_sort_key provides reusable sorting logic. It returns (date_time, appointment_id), so appointments are sorted chronologically, with appointment ID breaking ties when two appointments have the same date and time.

5. How do default and explicit status filters differ?
When status=None, the query includes all appointment statuses, including SCHEDULED, CANCELLED and COMPLETED. When an explicit AppointmentStatus is supplied, only appointments with that status are returned.

6. How do empty, unknown practitioner and invalid filter cases differ?
A registered practitioner with no matching appointments receives an empty list. An unknown practitioner ID raises LookupError. A blank or invalid practitioner ID, or a status that is not an AppointmentStatus enum value, raises ValueError. The service handles these distinctions rather than the pure query.

7. Which console errors recover, and how is unchanged state checked?
The console recovers from invalid menu choices, blank or duplicate IDs, unknown records, malformed or impossible dates, invalid statuses, booking conflicts and repeated cancellation. It displays an error and returns to the menu. State preservation is checked by retrieving existing records, confirming their identity and status, and successfully reusing an appointment ID after a rejected booking.

8. What is data integrity for registered participants, conflicts and history?
Data integrity means appointments reference the actual registered Patient and Practitioner objects, duplicate appointment IDs are rejected, and a practitioner cannot have two SCHEDULED appointments at the same time. Cancellation updates the existing appointment's status without deleting its history, allowing later retrieval and listing.
9. What is Copilot's review role, and who verifies findings?
GitHub Copilot acts as a reviewer that identifies possible defects, missing tests and optional improvements. Human group members assess its suggestions against the requirements and actual code. In Stage 9, we accepted its automated console-testing recommendation and added five passing test cases, while rejecting an optional data-store hardening suggestion as unnecessary for the required workflow. Copilot's claims are not treated as proof without human verification.

10. How do pure functions and OOP responsibilities work together?
OOP components manage responsibilities such as domain validation, stored records and service coordination. Pure functions handle appointment filtering and sorting using explicit inputs without changing state. The console manages user interaction and delegates operations to services rather than implementing domain rules itself. This separation keeps the application understandable and testable.

## H. Review, completion and common handover

Issues and bounded branches: Stage 9 implementation branch `stage09-integration`. Query implementation, service listing, console integration and testing were completed in bounded commits. GitHub issue links pending.
PR/diff and another-member human reviewer: PR pending. Anish Atamkur is the designated peer reviewer; actual review feedback will be recorded after review.
Review responses and Copilot comparison: GitHub Copilot reviewed the Stage 9 code and tests in the VS Code chat "SmartCare Stage 9 Review". Its Important finding about missing automated console tests was accepted and resolved in commit `55fb153`. Its Optional data-store hardening suggestion was rejected as unnecessary for the assessed service workflow. Human peer-review evidence pending.
Integrated common Stage 9 SHA: Pending PR merge into main. Latest Stage 9 branch commit: `55fb153`.
Full regression command, working directory, actual count/result and evidence: From `project/`, ran `python -m pytest -q`. Actual result: 76 passed, 0 failed, in 0.10s. Automated query, service, workflow and console tests passed.
README run instructions and scope/limitations: Updated `project/README.md` with demo and interactive commands, menu options, test instructions, application responsibilities, session-only storage and Stage 9 limitations. GitHub link pending.
Unresolved issues and support/action:  No failing automated tests reported. README documentation, GitHub PR, peer review and integration remain outstanding.
UG common candidate / PG future branch plan: After Stage 9 is reviewed and merged, preserve the integrated common SHA. UG proceeds toward Stage 12. Any PG Stage 10/11 work must use a separate approved branch. No persistence, rescheduling or assurance extensions are included in Stage 9.

- [x] Query contracts, purity, new lists and named-key ordering verified.
- [x] Service empty/unknown/invalid cases and cancellation history verified.
- [x] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [x] Reflections and ten formative responses completed.
- [x] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
