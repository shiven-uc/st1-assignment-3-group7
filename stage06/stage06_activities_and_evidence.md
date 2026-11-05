# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Group 7, Wednesday 2:30-4:30
- Members, GitHub usernames and cohorts: Shiven Mitra (shiven-uc), UG, Anish Atamkur (anish32132), UG
- Repository URL: https://github.com/shiven-uc/st1-assignment-3-group7
- Starting SHA: a597bfc9854f4d75f8adb97c713d3785c550fd18

## A Requirement to issue activities

### FR-02 Patient Search

- Title: Add patient and practitioner lookup by ID (FR-02)
- Context: The `find_patient` and `find_practitioner` functions in `services.py` currently raise `NotImplementedError`, as deliberately specified in the starter code. This prevents the services from searching for and returning registered patient and practitioner records.
- Requirement: FR-02 Patient Search
- Acceptance criteria: See issue #1. A registered ID returns the same stored object; a valid ID nobody has raises `LookupError`; a blank or invalid ID raises `ValueError`; IDs are trimmed and case-sensitive; the same cases apply to `find_practitioner`; lookup never creates a replacement or modifies records.
- Scope: Included: looking up registered patients and practitioners by ID, returning the stored objects, and handling missing, blank or invalid IDs. Not included: displaying details, cancellation, the interactive menu, or registering, editing or deleting records.
- Definition of Done: All relevant tests written and passing, reviewed by a different group member through a pull request, and merged into `main`.
- Owner: shiven-uc
- Actual issue link: https://github.com/shiven-uc/st1-assignment-3-group7/issues/1

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: Add appointment cancellation with retained history (FR-06/FR-07)
- Context: The `cancel_appointment` function in `services.py` currently raises `NotImplementedError`, preventing appointments from being cancelled through the service layer.
- Requirement: FR-06 Appointment Cancellation with FR-07 Retained History
- Acceptance criteria: See issue #2. Cancelling a scheduled appointment returns the cancelled object; an unknown ID raises `LookupError`; cancelling an already-cancelled or completed appointment raises `ValueError` and leaves status and details unchanged; after cancelling, `find_appointment` still returns the same object with its original details; a blank or invalid ID raises `ValueError`.
- Scope: Included: cancelling scheduled appointments, handling unknown IDs, preventing illegal cancellations, and retaining cancelled records. Not included: patient and practitioner lookup (issue #1), listing appointments (Stage 9), creating or rescheduling appointments, permanently deleting records, or the interactive menu.
- Definition of Done: All relevant tests written and passing, reviewed by a different group member through a pull request, and merged into `main`.
- Owner: shiven-uc
- Actual issue link: https://github.com/shiven-uc/st1-assignment-3-group7/issues/2

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | Weak | It doesn't say what was changed or why, so anyone reading the history later can't tell what the commit did without opening the code. |
| final version | Weak | It is too vague and doesn't explain what was finalised or which feature was changed. |
| Add patient search by ID | Strong | Clearly identifies the feature that was added and what it does. Someone reading the commit history can understand the change without opening the code. |
| fix stuff | Weak | It doesn't identify the problem that was fixed or explain what was modified. |
| Prevent cancellation of completed appointments | Strong | Clearly describes the specific behaviour being enforced. It is descriptive and easy to understand. |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: The PR includes changes that are unrelated to appointment cancellation. This makes the pull request larger than necessary and harder to understand and review. The unrelated changes also don't trace back to any issue or acceptance criteria, so a reviewer has nothing to check them against.
- Responsibility and architecture concerns: Renaming patient fields changes the public interface of the Patient domain object, which other code and the supplied tests rely on, and restructuring unrelated code could affect other parts of the system. Changes should remain focused on the cancellation service and the domain's existing cancel transition. A new dependency also needs a justification, because SmartCare's runtime uses only the standard library.
- Testing and review concerns: Unrelated changes increase the risk of introducing bugs into existing functionality. Additional tests would be needed to ensure patient-related features and other existing functionality still work correctly. A green test run doesn't settle this, because passing tests only prove what they check, and reviewing the PR also becomes more difficult because the reviewer can't tell whether the unrelated changes are safe.
- Changes to remove or separate, with reasons: Changes to remove or separate, with reasons: Remove the unrelated patient field renaming, code restructuring and new dependency from the cancellation PR. If these changes are necessary, create separate issues and pull requests for them so each change can be reviewed and tested independently. Keep the original PR focused only on appointment cancellation and retained history.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: The review does not provide evidence of which tests were run, what functionality was tested, whether edge cases were covered, or whether the code meets the acceptance criteria.
- Follow-up review question 1: Have all acceptance criteria been tested, including successful searches and invalid inputs?
- Follow-up review question 2: Which test command was run, from which directory, and what was the exact result?
- Follow-up review question 3: Have blank or invalid IDs been tested to ensure the correct errors are raised?
- Follow-up review question 4: Does the function return the original stored object rather than creating a copy or replacement?
- Follow-up review question 5: Have you tested that cancelling an appointment retains its history and does not delete the original record?
- Additional questions if useful: Are there any untested edge cases, unintended side effects, or changes outside the intended scope? Would these tests actually fail if the behaviour were wrong, or could an incorrect result still pass?

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | Use descriptive branch names that include the feature or issue number, e.g. `feature/issue-1-patient-lookup`. |
| Commit message convention | Use short, descriptive messages explaining what changed, starting with an action verb, e.g. `Add patient search by ID`. |
| PR size | Keep pull requests small and focused on one issue or feature at a time to make reviewing easier. |
| Another-member review requirement | Every pull request must be reviewed and approved by at least one different group member before merging. |
| Merge rule | Only merge into `main` after the required review is completed, all feedback is resolved, there are no unrelated changes, and all relevant tests pass. |
| Significant Copilot disclosure rule | Team members must disclose significant use of GitHub Copilot in the PR description and in section H of the Stage 6 record, and must review and understand any generated content before committing it. |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| https://github.com/shiven-uc/st1-assignment-3-group7/issues/1 | FR-02 Patient Search | shiven-uc | See issue #1: patient and practitioner lookup. Supporting criterion for `find_practitioner` to be confirmed with tutor. | Open |
| https://github.com/shiven-uc/st1-assignment-3-group7/issues/2 | FR-06 Cancellation with FR-07 retained history | shiven-uc | See issue #2: cancel_appointment | Open |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: https://github.com/shiven-uc/st1-assignment-3-group7/pull/3, "Add patient and practitioner lookup by ID (FR-02)"
- Linked issue and requirement: Issue #1, Add patient and practitioner lookup by ID (FR-02)
- Feature branch: feature/issue-1-patient-lookup
- Changed behaviour: find_patient and find_practitioner now return the stored object for a registered ID, raise LookupError for a valid ID nobody has, and raise ValueError for a blank or invalid ID. IDs are trimmed and case-sensitive. Lookup does not create or modify records.
- Meaningful commits: https://github.com/shiven-uc/st1-assignment-3-group7/commit/7ccfdfe (Add patient and practitioner lookup by ID)
- Test command, directory and observed result: python -m pytest, run from project/, 26 passed (8 starter tests plus 18 new), code SHA 7ccfdfe
- Another-member reviewer: anish32132 (Anish Atamkur)
- Human observations recorded before Copilot: Reviewed 5 November 2026, approximately 7:05 pm AEDT, before any Copilot use. Anish checked the acceptance criteria for both lookups: the original stored object is returned, an unknown valid ID raises LookupError, blank or invalid IDs raise ValueError, and lookup creates or modifies no records. He also checked the additional tests for trimming surrounding spaces and case-sensitive IDs, and found the implementation consistent with the criteria. His observations were supplied to me and entered by me on his behalf, as unit staff confirmed was acceptable.
- Requirement, responsibilities, test assertions and unrelated-scope checks: Anish checked the implementation against the issue's acceptance criteria and reviewed the additional tests for trimming and case sensitivity.
- Key feedback: The PR description did not include the test command, the test results or any significant AI assistance, so Anish could not verify that the tests had passed. He recommended adding that evidence.
- Author response/change and verification: Following the review, the author addressed Copilot's two optional findings in commit 558b9d5. The preservation tests gained direct assertions for stored record fields, and incidental final-newline changes were corrected. The test suite was rerun from project/, with 26 tests passing. The PR description's test evidence and AI disclosure should also be updated as recommended.
- Reviewer recheck and approval: Anish's confirmed recheck and approval https://github.com/shiven-uc/st1-assignment-3-group7/pull/3#issuecomment-6660698047
- Merge outcome and SHA: PR #3 successfully merged into main. Merge commit SHA: 2eb256b3e7d22967dee6fced3b3214c103c1a54b.
- Significant Copilot assistance: Copilot reviewed the PR diff, identified weaknesses in preservation-test assertions and flagged unrelated newline changes. The suggestions were checked and acted upon by the author.
- Linked issue closure:  Issue #1 was linked to PR #3. Its closure status must be confirmed on GitHub. https://github.com/shiven-uc/st1-assignment-3-group7/issues/1.
- Integrated verification after merge: Shiven updated local main using git pull --ff-only, then ran python -m pytest from project/. All 26 tests passed in 0.14 seconds.

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: Shiven Mitra, Copilot review of PR #3 for Issue #1 (FR-02 lookup).
- Prompt/purpose and relevant issue/diff: Used the Stage 6 Copilot review instructions to examine the acceptance criteria and the difference between main and feature/issue-1-patient-lookup, initially at commit 7ccfdfe.
- Summary of output: Copilot considered the lookup implementation consistent with the requirements but raised two optional findings. First, the preservation tests compared lists containing the same object references, meaning changes to object fields might not be detected. Second, the diff contained unrelated final-newline changes. Copilot also stated that it had not executed the tests.
- Human check against actual code, requirements and tests: The author inspected the preservation-test assertions and the diff. Both findings were considered valid. Direct assertions on record fields were added, and the incidental newline changes were corrected.
- Decision — Accept / Modify / Reject: Modify the first suggestion and Accept the second.
- Reason: The first suggestion was implemented using straightforward assertions on stored patient and practitioner fields rather than relying only on object-reference comparisons. The second was accepted because removing unrelated changes kept the PR focused.
- Verification/evidence: Commit 558b9d5. Running python -m pytest from project/ produced 26 passing tests. The corrected diff was checked for the incidental newline changes.

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: Anish checked the lookup acceptance criteria, including stored-object identity, error handling, ID trimming and case sensitivity. He identified missing test results and AI disclosure in the PR description.
- Copilot noticed: Copilot identified a weakness in the preservation tests because comparing collections of the same object references could miss changes to individual fields. It also identified incidental final-newline changes.
- Overlap: Both reviews considered the lookup implementation consistent with the main FR-02 requirements. Both supported retaining the existing objects and validating lookup behaviour.
- What did the human reviewer notice that Copilot did not: Anish noticed that the PR description lacked sufficient testing evidence and AI disclosure for a reviewer to verify the work.
- What did Copilot identify that the human reviewer initially missed: Copilot identified the limitations of the preservation assertions and unrelated newline changes in the diff.
- Unsupported or incorrect Copilot suggestion: None identified in the recorded findings. Copilot's suggestions were treated as recommendations requiring human verification, not automatically accepted changes.
- Human judgement accepted, modified or rejected, and why: The author modified the first suggestion by adding explicit field assertions and accepted the second by correcting incidental formatting changes. Both decisions improved the reviewability and verification of the implementation without changing the required lookup behaviour.
- Which evidence justified merge approval: Anish reviewed the implementation against the FR-02 acceptance criteria and confirmed his approval after the feedback was addressed. The final changes included stronger preservation tests and removal of unrelated newline changes. The full test suite passed with 26 tests. Anish's approval was documented in a GitHub comment posted by Shiven on Anish's behalf.

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: Shiven Mitra (shiven-uc), UG
- Implementation: Implemented the FR-02 patient and practitioner lookup functionality in Issue #1, including valid ID lookup, error handling, whitespace trimming and case-sensitive matching. Evidence: PR #3, commit 7ccfdfe.
- Testing: Developed and ran tests for valid, missing and invalid IDs, object identity and preservation of stored records. Strengthened preservation assertions following Copilot feedback. The test suite returned 26 passing tests.
- Review: Responded to human reviewer feedback and evaluated Copilot's review suggestions, applying appropriate improvements in commit 558b9d5.
- Issue refinement: Contributed to defining and implementing the FR-02 lookup requirements in Issue #1.
- Design and responsibility discussion: Worked on service-layer lookup behaviour, including returning existing stored objects and raising the appropriate exceptions.
- Debugging or integration: Corrected preservation-test weaknesses and removed unrelated formatting changes. Integration into main will be recorded after merging.
- Documentation or team support: Prepared the PR description, recorded review evidence, documented human and Copilot feedback, and maintained the Stage 6 activity and evidence record.

- Member: Anish Atamkur (anish32132), UG
- Implementation: Not applicable so far.
- Testing: Helped develop test scenarios for valid, missing and blank IDs (see the acceptance criteria in issue #1).
- Review: Reviewed the issue #1 lookup , checked each acceptance criterion and the extra trimming and case-sensitivity tests, and gave feedback on missing test evidence.
- Issue refinement: Helped refine the FR-02 patient and practitioner lookup issue.
- Design and responsibility discussion: Helped clarify the service-layer requirements and the expected error handling.
- Debugging or integration: Not applicable so far.
- Documentation or team support: Helped draft the team workflow agreement and commit message conventions, and gave feedback on the PR description.


## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

A high commit count does not necessarily mean someone made a strong contribution because commits can vary significantly in size, complexity and importance. Someone might make many small changes, while another person makes fewer commits that involve substantial implementation, testing or problem solving. Strong contributions should be judged by the quality and impact of the work, including code, testing, reviews, documentation and teamwork, rather than just the number of commits.

## L Stage 6 formative questions

1. What is version control?

Version control is a system that tracks changes made to files over time. It allows developers to see previous versions, restore changes when needed and collaborate on the same project without losing work.

2. Why is a feature branch useful?

A feature branch allows developers to work on a specific feature or issue without directly changing the main branch. This keeps the main version stable while changes are developed, tested and reviewed.

3. What makes a commit a good engineering commit?

A good engineering commit contains a focused, meaningful change with a clear commit message explaining what was done. It should avoid unrelated changes and ideally leave the code working and tested.

4. What is a pull request?

A pull request is a request to merge changes from one branch into another, usually into main. It allows team members to inspect the code, discuss changes, review tests and provide feedback before merging.

5. What is the purpose of code review?

Code review helps identify bugs, check that requirements are met, improve code quality and ensure changes are understandable and maintainable. It also allows team members to share knowledge and provide feedback.

6. What does a Git diff show?

A Git diff shows the differences between versions of files or branches. It highlights lines that have been added, removed or modified, allowing developers and reviewers to see exactly what changed.

7. What is a Definition of Done?

A Definition of Done is a set of agreed conditions that must be satisfied before work is considered complete. These can include meeting acceptance criteria, passing tests, completing code review and updating documentation.

8. What is the appropriate role of GitHub Copilot in pull-request review?

GitHub Copilot should be used as a supporting review tool to identify possible bugs, missing tests or improvements. Its suggestions must be checked against the actual code and requirements by a human. Copilot should not replace human review or make the final approval decision.

9. Why should individual contribution not be judged only by commit count?

Commit count does not measure the quality, difficulty or importance of someone's work. A person may make fewer commits but contribute significant implementation, testing or reviews. Contributions should be assessed using actual evidence of work and its impact.

10. What is the Stage 6 engineering rule?

Changes should be developed on a feature branch, supported by appropriate tests and evidence, reviewed by another team member and checked before merging into main. Copilot can assist with review, but human judgement and verification are still required.

## M Completion and handover

- Starting SHA: a597bfc (original SmartCare starter commit).
- Final Stage 6 code SHA: 2eb256b3e7d22967dee6fced3b3214c103c1a54b
- Test command: `python -m pytest`
- Working directory: `project/`
- Observed result: 26 tests passed in 0.14 seconds on updated main.
- PR and another-member reviewer: PR #3 — reviewed by Anish Atamkur (anish32132) https://github.com/shiven-uc/st1-assignment-3-group7/pull/3#issuecomment-6660698047
- Unresolved issue or none: PR #3 has been merged and integrated verification passed (26 tests). Confirmation of Issue #1 closure, Anish's separate integrated verification, and integration of the Stage 6 documentation PR #4 remain outstanding.
- Stage 7 handover status: Stage 6 code has been merged and verified. Stage 7 handover is pending final integration of the Stage 6 evidence document and confirmation of the remaining checklist items.
- Final submitted SHA if later than tested SHA: The tested code SHA is 2eb256b3e7d22967dee6fced3b3214c103c1a54b. Documentation commit 459e242 records later evidence changes on branch docs/stage06-record. The final integrated submission SHA will be recorded after PR #4 is merged. These documentation changes do not modify the tested application code.

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
