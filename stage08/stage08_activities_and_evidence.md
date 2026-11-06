# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [complete]
Members and UG/PG cohorts: [complete]
Record owner / contribution links for each member: [complete]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.

Response and reason:
- Appointment disappears after cancellation. - Symptom. This describes unexpected behaviour but does not identify its cause. FR-07 requires cancelled appointments to remain retrievable.
- The data-store removal path is probably being called. - Hypothesis. This suggests a possible explanation that needs investigation. It has not been confirmed by code inspection or test results, and the current data store has no public delete operation.
- The failing test shows store.find_appointment('A1') returns None. - Evidence. This describes an observable test result that can help confirm the symptom, assuming it was actually recorded during a test.
- The service layer is badly designed. - Opinion. This is a subjective judgement without specific evidence identifying a defect.
- Traceback points to smartcare/services.py line 42 in the example. - Evidence. A traceback identifies where an error was reported and helps guide investigation. The example line number is illustrative, not a confirmed location in our code.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason:

- Scenario: Cancelled appointment history (FR-07 / AC-05.2).

- Expected behaviour: Cancelling a SCHEDULED appointment changes its status to CANCELLED, but the appointment remains stored and retrievable using its appointment ID.

- Observed behaviour: No failure observed in the current baseline. The full regression suite passed 50 tests. The disappearance scenario is hypothetical until the Stage 8 faulty state is prepared.

- Minimal reproduction: Register a patient and practitioner, book appointment A1, cancel A1, then retrieve A1 from the data store and check its status.

- Initial hypothesis: If the appointment disappears after cancellation, the cancellation operation may be incorrectly removing or replacing the stored record rather than preserving it with CANCELLED status.

- Evidence to inspect: The failing test assertion, actual retrieved value, cancellation service and domain methods, appointment storage logic, and traceback. Compare these against FR-07 / AC-05.2.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: 

Response and reason:

Scenario 1 — Test expects cancelled appointments to be deleted:

This is a test defect, not a product defect. FR-07 requires cancelled appointments to remain stored and retrievable. The test should be corrected to expect the appointment to remain in the data store with CANCELLED status. The application should not be changed to satisfy an incorrect test.

Scenario 2 — Test expects different practitioners at the same time to conflict:

This is also a test defect because AC-04.2 explicitly allows different practitioners to have appointments at the same time. The test should be updated to expect both bookings to succeed, provided all other booking requirements are satisfied.

Conclusion: Tests must reflect the actual requirements. A failing test does not automatically mean the application code is wrong.

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason:

The hypothetical 70-line AppointmentService method contains several code smells:
- Long method: Too many responsibilities are handled in one method.
- Duplicated code: Repeated status checks and validation make maintenance harder.
- Magic strings: Using status strings instead of the existing AppointmentStatus enum increases the risk of mistakes.
- Deep nesting: Four nested conditionals make the logic difficult to understand.
- Mixed responsibilities: Validation, storage operations and printing are combined.

Small refactorings could include extracting repeated conflict-checking logic into a helper, replacing status strings with the existing enum, using clearer variable names and simplifying nested conditions. These changes should preserve the existing SmartCare behaviour and continue using the SmartCareDataStore boundary.

Classification of proposed changes:
- Rename appt to appointment - Refactoring, because it improves readability without changing behaviour.
- Extract a repeated conflict helper - Refactoring, because it removes duplication while retaining the same conflict rule.
- Add rescheduling - Feature, because it introduces new functionality not required by the current specification.
- Restore retained cancellation lookup - Repair, because it fixes behaviour that violates FR-07.
- Replace a magic status string with the existing enum - Refactoring, provided the observable behaviour remains unchanged.

Behaviour to preserve: Valid bookings must still succeed, same-practitioner/exact-time SCHEDULED conflicts must still be rejected, different practitioners may book at the same time, and cancelled appointments must remain stored and retrievable.


### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason:

Pending the controlled Stage 8 fault preparation and first failing test.

The current SmartCare baseline passed all 50 tests, so no actual failure has been observed yet.

After reproducing a fault, I will record the failing assertion or exception, expected and observed values, exact test line, application call path, and supporting requirement.

I will then rank three possible causes and identify a check for each one.

A traceback alone does not establish the root cause because it shows where a failure was detected, which may differ from where the underlying defect originated.

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: Changing code immediately after seeing a failure is risky because the problem might be caused by an incorrect test, a misunderstanding of the requirements or an unexpected interaction elsewhere in the program.

A better approach is to reproduce the failure, examine the evidence, form hypotheses and identify the root cause before making a small, justified change. This reduces the risk of introducing additional defects.


Classification responses (1–5, each with reason): See A.1. The five statements were classified as symptom, hypothesis, evidence, opinion and evidence, with explanations.
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: See A.2. The cancelled-history scenario was documented against FR-07 / AC-05.2, including expected behaviour, the passing baseline observation, reproduction steps, an initial hypothesis and planned evidence checks.
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: Pending actual Stage 8 failure. See A.5. No failure or traceback was observed in the passing 50-test baseline. Complete this field after reproducing a fault.

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline:  1c2317ab43822a2a1b4a630179ca3477b1009605. SmartCare requirements FR-01–FR-08 and their acceptance criteria remain the testing baseline.
- Baseline test command / working directory / observed result / evidence: python -m pytest -q from project/; 50 passed, 0 failed in 0.08s. No failures observed before Stage 8 fault preparation.
- Clean preparation SHA if a record-only commit followed Stage 7: d04140802ab76657208ca54169c053a0036008e7. This commit records the Stage 8 tutorial and baseline before fault preparation. The --check preflight passed at this SHA.
- Branch and preparer / how teammates obtained this branch: stage08-debugging, prepared locally by Shiven. Teammate branch access or transfer pending.
- Downloaded tool version, source SHA256 and --check outcome: Stage 8 preparation tool v1.1. Baseline source SHA256: b4a1993e878c59a9df5e9055320702b2d318c5b6055bb1693a3afc25cd8fd375. --check passed; the project remained unchanged, and both proposed fault signatures were verified in a temporary copy.
- --apply and --verify output summaries / artefact references: Stage 8 tool v1.1 successfully applied F8-01 and F8-02. The --apply command verified two expected failing fault signatures. The separate --verify command confirmed exactly two expected failures and both approved symptoms.
- Bounded diff inspected and recovery location (not committed): Inspected git --no-pager diff -- smartcare/data_store.py. The tool modified find_appointment() and has_practitioner_conflict(). Recovery information was recorded in .stage8_faults, which must not be committed.
- Prepared faulty-state commit SHA: 2592cce (prepared F8-01 and F8-02 faults, before repairs).
- Preparation or recovery issues and resolution, if any: No preparation errors occurred. The LF/CRLF messages were Git line-ending warnings, not preparation failures. Recovery was not required.
- Initial prepared full-suite command / result / key failures: python -m pytest -q from project/: 43 passed, 7 failed in 0.20s. Key failures involved same-practitioner conflicts not being rejected, different-practitioner bookings being rejected incorrectly, and cancelled appointments becoming unavailable through lookup. These failures are consistent with F8-01 and F8-02.

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: SmartCare incorrectly allows two SCHEDULED appointments for the same practitioner at the same time, while rejecting appointments for different practitioners at that time.
- Expected behaviour and requirement: FR-05 / AC-04.1 requires a conflicting SCHEDULED appointment for the same practitioner and exact time to be rejected. AC-04.2 allows different practitioners to have appointments at the same time.
- Minimal synthetic reproduction steps: Register two patients and practitioners D1 and D2. Book A1 with D1 at 9:00 AM. Attempt A2 with D1 at 9:00 AM, then separately test booking A2 with D2 at 9:00 AM using fresh store state.
- Meaningful failing test path/name and exact relevant failure: tests/test_stage07.py::test_same_practitioner_time_conflict — Failed: DID NOT RAISE ValueError at line 83. Also, tests/test_stage07.py::test_different_practitioners_same_time — unexpected ValueError: Practitioner already has a SCHEDULED appointment at this time.
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: SmartCareDataStore.has_practitioner_conflict() incorrectly used != when comparing practitioner IDs. This inverted the conflict rule, allowing same-practitioner conflicts while rejecting different practitioners. The Git diff, failing tests and code inspection confirmed the cause.
- Smallest justified fix / diff / why other behaviour is preserved: Changed the practitioner-ID comparison from != to ==. This restored the required same-practitioner conflict rule without altering the booking service, data-store interface or other scheduling requirements.
- Repair SHA / focused verification result: 9e8b98e1db57a062b75afa91cfb64ad6b79f4cdf. Focused tests: 2 passed. Full suite after F8-01 repair: 46 passed, 4 failed, with the remaining failures associated with F8-02.

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: After cancellation, an appointment becomes unavailable through service lookup. Repeated cancellation also raises LookupError instead of ValueError.
- Expected behaviour and requirement: FR-07 / AC-05.2 requires cancelled appointments to remain stored and retrievable. FR-06 / AC-05.3 requires repeated cancellation to be rejected with ValueError.
- Minimal synthetic reproduction steps: Register a patient and practitioner, book appointment A1, cancel A1, then attempt to retrieve A1. Attempt to cancel A1 again and check the exception.
- Meaningful failing test path/name and exact relevant failure: tests/test_stage07.py::test_cancelled_appointment_retained — LookupError: Appointment not found at smartcare/services.py:136. Also, tests/test_stage07.py::test_repeated_cancellation_rejected — expected ValueError but received LookupError.
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: SmartCareDataStore.find_appointment() incorrectly excluded appointments with CANCELLED status. This caused the store to return None, which led AppointmentService.find_appointment() to raise LookupError. The failing tests and inspected code supported this diagnosis.
- Smallest justified fix / diff / why other behaviour is preserved: Removed the cancelled-status exclusion and restored lookup through the appointment dictionary using validated appointment IDs. Cancelled appointments remain retrievable, while unknown IDs still return None at the store level. No additional business rules were introduced.
- Repair SHA / focused verification result: b9ee2de3d5d95c6b29e8ec2ab325c81515159337. Focused tests: 2 passed. Full regression suite after both repairs: 50 passed, 0 failed.

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: The practitioner conflict check may be comparing practitioner IDs incorrectly. The tests show that bookings for the same practitioner are incorrectly allowed, while bookings for different practitioners are rejected.
Evidence intended to inspect / competing explanation / discriminating check:  Inspect SmartCareDataStore.has_practitioner_conflict() and its practitioner ID, time and status comparisons. An alternative explanation is that AppointmentService.book_appointment() passes the wrong practitioner ID. Compare the service arguments with the stored appointment details to distinguish these possibilities.
Member and saved sequence/time or commit showing this preceded consultation: Shiven. Hypothesis recorded after the initial failing tests and before consulting GitHub Copilot. Human-first hypotheses saved in commit d53e1b6ede24a34097cc57abdeee4a6208c53319, before GitHub Copilot consultation.

### F8-02 human entry
Likely cause and why plausible: The appointment lookup method may incorrectly exclude appointments with CANCELLED status. The tests show that cancelled appointments become unavailable through lookup.
Evidence intended to inspect / competing explanation / discriminating check: Inspect SmartCareDataStore.find_appointment() and compare the result with list_appointments(). An alternative explanation is that cancellation removes the appointment from storage. Check whether the appointment is still in the stored list after cancellation.
Member and saved sequence/time or commit showing this preceded consultation: Shiven. Hypothesis recorded after the initial failing tests and before consulting GitHub Copilot. Human-first hypotheses saved in commit d53e1b6ede24a34097cc57abdeee4a6208c53319, before GitHub Copilot consultation.

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: Shiven. GitHub Copilot Chat was asked to investigate F8-01 after the human-first hypotheses were saved in commit d53e1b6. The prompt included requirements FR-05 / AC-04.1–AC-04.2, observed failures, reproduction steps, relevant code, the initial hypothesis and a request for three ranked causes. Copilot inspected the service, data store, domain and tests, then reran the two affected tests from project/. Both failed as expected. No files were edited.
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot suggested that the practitioner-ID comparison is inverted. The inspected code uses appointment.practitioner.practitioner_id != practitioner_id. This explains why the same practitioner is allowed and different practitioners are blocked. Correct — Accept. The evidence directly supports changing the comparison to equality.
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot suggested that book_appointment() might pass the wrong practitioner ID. Inspection showed that the service passes the resolved practitioner's ID to the conflict check. Wrong for the inspected code — Reject. No caller-side change is justified by the available evidence.
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot suggested that the SCHEDULED-status check might be incorrect. The domain enum defines the value as "scheduled", matching the condition currently used. Unsupported by the inspected evidence — Reject. The reported failures are better explained by the inverted practitioner comparison.
Final human conclusion and comparison with initial hypothesis: Copilot's highest-ranked diagnosis agreed with the original human-first hypothesis. The faulty practitioner-ID comparison is supported by the diff, test failures and inspected application code. The other two alternatives were not supported by the evidence. The justified repair is a minimal equality comparison change, followed by focused and full regression testing.

### F8-02 Copilot review
Actual prompt / output reference and member: Shiven. GitHub Copilot Chat was consulted after the human-first hypotheses were committed in d53e1b6. The prompt included FR-07 / AC-05.2 and FR-06 / AC-05.3, observed behaviour, reproduction steps, failing tests, the human hypothesis, relevant code and instructions not to modify files. Copilot inspected the data store and service code and ran two focused tests. Both failed with LookupError, as expected. No files were edited.
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot identified a cancelled-status filter in SmartCareDataStore.find_appointment(). The code only returns matching appointments when appointment.status.value != "cancelled". This explains why cancelled records cannot be retrieved. Comparing list_appointments() against direct lookup would distinguish filtering from actual removal. Correct — Accept. Removing the status exclusion while retaining ID validation and lookup behaviour is justified.
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot suggested that cancellation might physically remove appointments from storage. However, AppointmentService.cancel_appointment() calls appointment.cancel() without deleting the stored record. Inspecting stored appointments after cancellation would provide an additional check. Unsupported by inspected code — Reject. No change to cancellation storage behaviour is justified.
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Copilot suggested that the service might incorrectly treat cancelled appointments as missing. The service raises LookupError when the data store returns None, which is appropriate for genuinely unknown IDs. The incorrect result originates upstream in the data-store filter. Comparing direct store lookup with service lookup distinguishes this possibility. Partly correct explanation, wrong root cause - Reject as a repair. No service change is needed.
Final human conclusion and comparison with initial hypothesis: Copilot's highest-ranked diagnosis agreed with the human-first hypothesis: cancelled appointments are incorrectly excluded by SmartCareDataStore.find_appointment(). The code inspection and failing tests support this cause. The justified repair is to remove the cancelled-status exclusion while retaining required identifier validation and normal lookup behaviour.

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | F8-01 before repair | 2592cce (prepared faulty state) | python -m pytest -q from project/ |
| F8-01 after repair | F8-01 after repair | 9e8b98e | python -m pytest tests/test_stage07.py::test_same_practitioner_time_conflict tests/test_stage07.py::test_different_practitioners_same_time -q from project/ |
| F8-02 before repair | F8-02 before repair | 9e8b98e (F8-01 repaired, F8-02 still faulty) | python -m pytest -q from project/ |
| F8-02 after repair | F8-02 after repair | b9ee2de3d5d95c6b29e8ec2ab325c81515159337 | python -m pytest tests/test_stage07.py::test_cancelled_appointment_retained tests/test_stage07.py::test_repeated_cancellation_rejected -q from project/ |
| Full suite after both repairs, before refactor | Full suite after both repairs, before refactor | b9ee2de3d5d95c6b29e8ec2ab325c81515159337 | python -m pytest -q from project/ |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: F8-01 tests verify that same-practitioner/exact-time conflicts raise ValueError, while different-practitioner bookings succeed. F8-02 tests verify that cancelled appointments remain retrievable and that repeated cancellation raises ValueError. Retaining the existing tests helps detect regressions in patient registration, booking, cancellation and domain validation.
Unrelated failures investigated / resolution: During the F8-02 repair, an indentation mistake temporarily prevented pytest from collecting tests. The indentation was corrected, and the subsequent focused and full regression runs passed. No unrelated product defects remained in the final run.

## H. Refactoring decision and before/after verification

Smell and exact location: The has_practitioner_conflict() method in project/smartcare/data_store.py uses the hardcoded string "scheduled" when checking appointment status. This is a magic-string code smell because it depends on a literal value rather than the existing AppointmentStatus enum.
Small proposed structural change / why justified: Replace the comparison appointment.status.value == "scheduled" with appointment.status is AppointmentStatus.SCHEDULED. This improves readability and consistency with the domain model without changing the business rules.
External behaviour to preserve / relevant tests: Same-practitioner appointments at the exact same time must still conflict when SCHEDULED (AC-04.1). Different practitioners at the same time must still be allowed (AC-04.2). Cancelled appointments must remain retrievable (AC-05.2). Relevant tests include test_same_practitioner_time_conflict, test_different_practitioners_same_time, and the existing full regression suite.
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: Replaced appointment.status.value == "scheduled" with appointment.status is AppointmentStatus.SCHEDULED in SmartCareDataStore.has_practitioner_conflict(). This removes a magic string and uses the existing domain enum. Separate refactoring commit: 63feabb4a27620344a6dd1ea82d3f23a13c1f7ec.
Focused and full after-refactor commands / working directory / results / evidence: Ran python -m pytest tests/test_stage07.py::test_same_practitioner_time_conflict tests/test_stage07.py::test_different_practitioners_same_time -q from project/: 2 passed, 0 failed. Ran python -m pytest -q from project/: 50 passed, 0 failed.
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: Accepted. Replacing the hardcoded status string with the existing AppointmentStatus.SCHEDULED enum improved readability without changing observable behaviour. Focused conflict tests and the full regression suite passed before and after the refactor.

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: F8-01 — repair incorrect practitioner conflict detection (Shiven). F8-02 — restore cancelled appointment lookup (Shiven). Refactoring — replace the hardcoded scheduled-status string with the existing enum (Shiven). GitHub issue links pending; do not claim separate issues were created.
Branch / prepared, repair and refactor checkpoints: stage08-debugging. Prepared faulty state: 2592cce. Human-first hypotheses: d53e1b6. F8-01 repair: 9e8b98e. F8-02 repair: b9ee2de. Separate refactoring: 63feabb4a27620344a6dd1ea82d3f23a13c1f7ec. See Sections B, C, D and H.
PR link and another member's reviewer identity: Stage 8 pull request (insert actual PR link). Anish Atamkur reviewed the changes; his confirmed feedback was relayed through Shiven's GitHub account because he did not have GitHub access.
Key human feedback, difference from Copilot findings and response/outcome: Anish agreed that both repairs were consistent with the SmartCare requirements and that replacing the hardcoded status string with the enum improved readability. He suggested adding a dedicated test confirming that a cancelled appointment no longer blocks its original time slot. Unlike Copilot's diagnosis, which focused on identifying root causes, the human review also considered the adequacy of regression coverage. The suggestion has been recorded for consideration; no additional test has yet been implemented.
Actual review approval / merge evidence: No Stage 8 review approval or merge recorded yet.
Integrated code SHA and team pull/retest command / working directory / result: Pending merge into main. Current refactoring branch passed python -m pytest -q from project/ with 50 passed, 0 failed.
Evidence-only later SHA / explanation if different: Not applicable yet. Update if a documentation-only commit follows the final integrated code SHA.
Each member's substantive contribution and artefact: Shiven; inspected the actual faults, recorded human-first hypotheses, evaluated Copilot diagnoses, implemented both repairs, performed the refactoring, ran verification tests and maintained the Stage 8 evidence record. Evidence: commits d53e1b6, 9e8b98e, b9ee2de and 63feabb. Anish; human review pending; record his actual feedback and contribution once received.

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [complete]

2. Where should expected behaviour come from during debugging?

Response: [complete]

3. What is a debugging hypothesis?

Response: [complete]

4. What is a regression test and why is it retained?

Response: [complete]

5. What is meant by root cause?

Response: [complete]

6. What is refactoring?

Response: [complete]

7. What is a swallowed exception?

Response: [complete]

8. What is a code smell?

Response: [complete]

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [complete]

10. What is the Stage 8 engineering rule?

Response: [complete]

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
