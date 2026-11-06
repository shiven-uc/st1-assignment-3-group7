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
- Clean preparation SHA if a record-only commit followed Stage 7: 3367c7e43a7db8e84cfa4b805d69f4c45297ab7a. This was the current HEAD when the passing baseline was checked. The Stage 8 document had uncommitted changes; unrelated desktop.ini was untracked.
- Branch and preparer / how teammates obtained this branch: [complete]
- Downloaded tool version, source SHA256 and --check outcome: [complete]
- --apply and --verify output summaries / artefact references: [complete]
- Bounded diff inspected and recovery location (not committed): [complete]
- Prepared faulty-state commit SHA: [complete]
- Preparation or recovery issues and resolution, if any: [complete]
- Initial prepared full-suite command / result / key failures: [complete]

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: [complete]
- Expected behaviour and requirement: [complete]
- Minimal synthetic reproduction steps: [complete]
- Meaningful failing test path/name and exact relevant failure: [complete]
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: [complete]
- Expected behaviour and requirement: [complete]
- Minimal synthetic reproduction steps: [complete]
- Meaningful failing test path/name and exact relevant failure: [complete]
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: [complete]
Evidence intended to inspect / competing explanation / discriminating check: [complete]
Member and saved sequence/time or commit showing this preceded consultation: [complete]

### F8-02 human entry
Likely cause and why plausible: [complete]
Evidence intended to inspect / competing explanation / discriminating check: [complete]
Member and saved sequence/time or commit showing this preceded consultation: [complete]

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

### F8-02 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-02 before repair | [complete] | [complete] | [complete] |
| F8-02 after repair | [complete] | [complete] | [complete] |
| Full suite after both repairs, before refactor | [complete] | [complete] | [complete] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [complete]
Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

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
