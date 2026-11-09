# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Group 7. Wednesday 2:30-4:30
Members and UG/PG applicability: Shiven and Anish Atamkur. Common undergraduate release pathway (Stages 6, 7, 8, 9 and 12). Stages 10 and 11 are not applicable to us.


## A Release scope and starting SHA

Release label/version and requirements baseline: SmartCare Assignment 3 - Stage 12 common undergraduate release candidate, based on the 2026 revision 2 requirements.
Common starting SHA / branch / applicable members: `6b6595180d82dfc6f9e67daf6b20931163df544c`, branch `main`; common Stage 9 checkpoint for UG members.
PG starting SHA / branch / applicable members or not applicable: not applicable
Working-state review and approved integration: Stage 9 implementation and final evidence were merged into main. The integrated project passed 76 automated tests in 0.16 seconds from `project/`, with a clean working tree. Final Stage 12 release verification remains pending.
Protected common candidate and PG differences: The verified Stage 9 common candidate is preserved at SHA `6b6595180d82dfc6f9e67daf6b20931163df544c`. No PG rescheduling or assurance extensions are included.
Feature freeze / owner / verifier: Common Stage 9 features are complete. Shiven will coordinate Stage 12 verification and release documentation. Anish Atamkur is the designated independent human verifier; his Stage 12 verification is pending.


## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: Decision: Do not release yet.
Passing automated tests is important, but it does not automatically mean the application is ready for release. An incomplete README makes the application difficult to reproduce, an unreviewed dependency introduces uncertainty, and an undocumented limitation could mislead users. Before releasing, the team should complete and verify the README instructions, review the dependency, document the known limitation, and repeat the relevant verification checks. Release can be reconsidered once these gaps are resolved.

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | Cancelled appointments remain retrievable and appear in all-status listings; verified by workflow and console tests | `project/tests/test_workflows.py`, `project/tests/test_console.py`; SHA `6b65951` | Shiven; Anish Stage 12 verification pending | Yes, automated evidence; final review pending | Confirm during final release demonstration |
| Architecture responsibilities are appropriate | Domain validates objects, store maintains session records, services coordinate operations, pure queries filter/sort, console handles interaction | `project/smartcare/`; Stage 9 Sections C and E | Shiven; Anish verification pending | Provisionally yes | Final code-quality review |
| Rescheduling is safe — PG only | N/A | N/A | N/A | N/A | N/A |
| AI use is responsible — common recheck / PG assurance | Copilot review recorded; missing console tests were added and verified; optional store change rejected | Stage 9 Section E; PR #10 | Shiven; Anish verification pending | Partially | Complete final Stage 12 AI/dependency check |
| System is maintainable | Separate domain, store, service, query and console modules; tests and README supplied | `project/README.md`, `project/smartcare/` | Shiven; Anish verification pending | Provisionally yes | Complete final maintainability review |
| FR-01–03 register/find and validation |  Registration, lookup, invalid and duplicate ID tests passed | `project/tests/test_services.py`; Stage 9 console evidence | Shiven; Anish verification pending | Yes, existing tests | Final regression |
| FR-04–05 booking/conflict rules | Same-practitioner conflict rejected; another practitioner allowed at the same time | `project/tests/test_workflows.py`; Stage 9 Section D | Shiven; Anish verification pending | Yes, existing tests | Final regression |
| FR-06–08 cancellation/history/find | Cancellation preserves original appointment identity and history; repeated cancellation rejected | `project/tests/test_workflows.py`; Stage 9 Section D | Shiven; Anish verification pending | Yes, existing tests | Final regression |
| FR-09 and QRY/FP listing/filter/order/purity | Practitioner isolation, enum filtering, fresh lists, ordering, unchanged source and named key tested | `project/tests/test_queries.py`, `project/tests/test_stage09_service.py` | Shiven; Anish verification pending | Yes, existing tests | Final regression |
| UI full console sequence and error recovery | Manual UI-01/UI-02 workflows and five automated console test executions | `project/tests/test_console.py`; Stage 9 Section D | Shiven; Anish verification pending | Yes, prior evidence | Repeat final release demonstration |
| Session-only scope / FR-10 retired | README documents in-memory storage and loss of data on exit | `project/README.md`; Stage 9 Section H | Shiven; Anish verification pending | Yes, documented scope | Confirm in final release notes |
| PG RES and assurance integration | N/A | N/A | N/A | N/A | N/A |


## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | Python 3.14.3; pytest 8.3.5 | `project/`; `python -m pytest -q` | `6b6595180d82dfc6f9e67daf6b20931163df544c` | PASS — 76 passed in 0.10s | Local terminal output; GitHub evidence link pending |
| Complete PG if applicable | Not applicable — UG-only group | Not applicable | Not applicable | Not applicable | No PG tests required |
| Affected focused checks after correction | No Stage 12 code corrections made yet | Not applicable | Not applicable | Not applicable | Run focused checks if corrections are needed |
| Full integrated recheck | Python 3.14.3; pytest 8.3.5 | `project/`; `python -m pytest -q` | `6b6595180d82dfc6f9e67daf6b20931163df544c` | PASS — 76 passed in 0.10s | Local terminal output; final release-candidate recheck pending |
Prior assertions preserved / reviewed test diff: All 76 accumulated tests from the previous stages were retained and passed without failures. No Stage 12 application code changes have been made at this checkpoint. Final release diff review remains pending.
Remaining failure / limitation: No automated test failures were observed. The application remains limited to synthetic, session-only in-memory data, with no restart persistence, rescheduling or production healthcare features. Final README reproducibility, release review and packaging checks remain pending.


## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders | SmartCare manages synthetic patients, practitioners and appointment records | Explain the problem and relevant users | Supports registration, booking and appointment history for patients and practitioners | `project/README.md` |
| Register and find Patient and two Practitioners | P1, D1 and D2 | FR-01–03: registration and lookup | PASS — P1, D1 and D2 registered and retrieved during Stage 9 manual testing | Stage 9 Section D |
| Valid booking | A1, P1, D1, 2026-12-01 09:00 | FR-04: valid booking | PASS — A1 booked as SCHEDULED | Stage 9 Section D |
| Same practitioner exact-time conflict rejected | A-CONFLICT, P1, D1, 2026-12-01 09:00 | FR-05: conflicting booking rejected | PASS — conflict error displayed | Stage 9 Section D |
| Different practitioner same time allowed | A2, P1, D2, 2026-12-01 09:00 | FR-05: different practitioner permitted | PASS — A2 booked successfully | Stage 9 Section D |
| Cancel SCHEDULED and retain/find CANCELLED object | Cancel A1, then find A1 | FR-06–08: cancellation retains history | PASS — A1 remained retrievable with CANCELLED status | Stage 9 Section D; `tests/test_workflows.py` |
| Invalid/repeated cancellation rejected | Cancel unknown A999; cancel A1 twice | FR-06–08: reject invalid cancellation | Previously tested during Stage 9 UI-02; automated repeated-cancellation test passed | `tests/test_workflows.py` |
| Default all-status listing | List D1 with blank status | QRY-02: default includes all statuses | PASS - cancelled A1 remained visible | Stage 9 Section D |
| Explicit filtering / empty vs unknown / deterministic order | Filter D1 by SCHEDULED; check unknown practitioner and ID tie-break | QRY-01–04, FP-03 | PASS in Stage 9 query and service tests; scheduled-only listing excluded cancelled A1 | `tests/test_queries.py`; `tests/test_stage09_service.py` |
| Invalid date/status/menu/lookup recovery and continued operation | Invalid date, status banana, menu 99, unknown IDs | UI-02: recover without partial state changes | Stage 9 manual and automated tests demonstrated error recovery | Stage 9 Section D; `tests/test_console.py` |
| Session-only limitation and normal exit | Exit using 0 | FR-10 retired; session data discarded | PASS - console exited normally and displayed session-data warning | Stage 9 Section D |
| One meaningful requirement-linked pytest test explained | `test_full_booking_cancellation_and_rebooking_workflow` | FR-04–08: booking, conflict, cancellation and history | PASS - verifies same-object identity, conflict rejection, retained history and freed-slot rebooking | `tests/test_workflows.py` |
| Architecture and one actual AI decision / known limitation | Shared store, services, pure queries and console; Copilot review | Separation of responsibilities and responsible AI | Accepted missing console-test finding and added five passing tests; session-only data remains a limitation | Stage 9 Section E; `tests/test_console.py` |
| PG reschedule identity/participants/time and no-op | N/A | N/A | N/A | N/A |
| PG conflict/invalid status/failure non-mutation | N/A | N/A | N/A | N/A |
| PG old slot / current lookup/list ordering / assurance risks | N/A| N/A | N/A | N/A |
Stable demo owner / fresh process / command: Shiven will demonstrate SmartCare using `python main.py --interactive` from the `project/` directory in a fresh Python process. The Stage 9 demonstration was completed successfully; final Stage 12 demonstration remains to be confirmed.
PG demonstrations through service/tests or not applicable: Not applicable - both group members are undergraduate students.


## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | `project/smartcare/domain.py`, `services.py`, `queries.py`, `console.py` | Domain, service, store and query responsibilities were separated during Stage 9 | No change required based on previous review; final Stage 12 inspection pending |
| PascalCase and snake_case naming | `project/smartcare/` | Classes use PascalCase and functions/methods use snake_case in reviewed Stage 9 code | Final naming review pending |
| Useful type hints and meaningful docstrings | `project/smartcare/queries.py`, `services.py` | Query and service interfaces contain type hints and descriptive docstrings | Final review pending |
| Four-space indentation and imports/layout | `project/smartcare/` | No formatting issues identified during previous testing | Final inspection pending |
| Focused methods / duplication / dead or commented code | `project/smartcare/` | Existing functions separate booking, lookup, cancellation and listing | Inspect for unnecessary duplication and dead code before release |
| Globals / leakage / unnecessary inheritance or frameworks | `project/smartcare/queries.py`, `console.py` | Queries use explicit inputs; console creates one session store | Final inspection for hidden state pending |
| No SQLite/persistence/repository ABCs/speculative features | `project/smartcare/`; `project/README.md` | No persistence or PG-only extensions included in Stage 9 implementation | No change required under UG requirements |
| Synthetic data / secrets / dependencies / provenance | `project/README.md`, `requirements-dev.txt` | Synthetic teaching data used; standard library runtime and pytest development dependency documented | Final dependency and secret inspection pending |
| Significant common Copilot contributions and human verification | Stage 9 Section E; PR #10; `tests/test_console.py` | Copilot identified missing automated console coverage; five tests were added and passed | Accepted finding verified; 76-test regression passed |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | N/A | N/A | N/A |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| Missing automated console coverage | UI-01/UI-02; `project/smartcare/console.py` | Added `tests/test_console.py` and ran the full regression suite | Accept — relevant missing test coverage | Five console tests passed; full suite 76 passed |
| Direct data-store writes bypass conflict checking | `project/smartcare/data_store.py`, `services.py` | Reviewed service booking and conflict tests | Reject — optional hardening beyond the required Stage 9 workflow | No code change; existing conflict tests passed |
Access route or approved equivalent / limitations: GitHub Copilot was used through VS Code to review the Stage 9 code and tests. Its suggestions were evaluated by humans rather than accepted automatically.
Available AI evidence and missing evidence honestly disclosed: Stage 9 Section E records the actual Copilot review, human decisions and verification results. PR #10 records Anish's feedback, relayed by Shiven. A separate final AI-use disclosure and Stage 12 release verification are still pending.


## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | `project/README.md` | Shiven; Anish verification pending | SmartCare purpose and UG common features documented; PG-only features excluded |
| Out-of-scope capabilities and known limitations | `project/README.md` | Shiven; Anish verification pending | Session-only storage, no persistence or rescheduling documented |
| Confirmed teaching Python version and dependency installation | `project/README.md`; `project/requirements-dev.txt` | Shiven | Local Python 3.14.3 and pytest 8.3.5 verified; README setup instructions present; fresh environment check pending |
| Working directory / demo / interactive / test commands | `project/README.md` | Shiven | Commands documented: `python main.py`, `python main.py --interactive`, `python -m pytest -q`; existing tests passed |
| Repository structure and architecture responsibilities | Root `README.md`; `project/README.md` | Shiven | Domain, data store, services, queries, console and main entry point documented |
| Responsible AI summary / synthetic-data rule | Stage 9 Section E; `project/README.md` | Shiven | Copilot review documented; synthetic-data-only rule stated; final AI disclosure pending |
| Release label/version and SHA links | Stage 12 Section A; `project/README.md` | Shiven | Stage 12 release label recorded in evidence; final release SHA and README links pending |
Root README index and project/README verified: Both README files were reviewed for the existing project structure, stage links, run instructions and session-only limitations. Final independent verification remains pending.
Fresh clone or extracted ZIP / candidate identity: Not yet performed. A fresh extraction of the final release ZIP will be checked against the submitted Git commit.
Verifier and clean environment / actual version:  Shiven verified Python 3.14.3, pytest 8.3.5 and 76 passing tests. Anish Atamkur independently reported that SmartCare works. His exact environment, test commands and output have not been supplied.8.3.5. Independent verification by Anish and fresh-environment reproduction remain pending.
Setup/run/test commands and observed results: From `project/`, `python -m pytest -q` returned 76 passed in 0.10s at SHA `6b6595180d82dfc6f9e67daf6b20931163df544c`. Demo and interactive commands were previously exercised during Stage 9; final fresh-environment checks remain pending.
Missing local file or setup gap / remedy and recheck: No missing local files have been reported. Final release packaging and independent setup checks are still pending; any issues found will be documented, corrected and retested.


## G Known limitations debt and release notes

Delivered features: Patient and practitioner registration and lookup; appointment booking, conflict rejection, cancellation and retained history; practitioner appointment listing with status filtering and deterministic sorting; interactive console with invalid-input recovery.
Important fixes: Stage 8 practitioner conflict detection and cancelled appointment retrieval were repaired. Stage 9 added automated console tests following Copilot feedback. The full regression suite passed 76 tests.
Architecture/quality improvements: SmartCare separates domain rules, shared in-memory storage, service coordination, pure queries and console interaction. Typed interfaces, reusable sorting, regression tests and README documentation support maintainability.
Known limitations: Data is lost when the program exits. The application has no restart persistence, rescheduling, authentication, notifications, billing or production healthcare integration. Dates use local minute precision without a timezone policy.
AI-assisted development note: GitHub Copilot reviewed the Stage 9 implementation. Its suggestion to add automated console coverage was accepted and tested. Optional data-store hardening was not implemented because it was outside the assessed Stage 9 service workflow. Human verification remains responsible for accepting AI recommendations.

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| Session-only storage | Records disappear when the program exits | Accepted scope limitation | Add persistence only if future requirements call for it | Yes — FR-10 retired |
| No authentication or access controls | Not suitable for real healthcare users or patient records | High for production use | Implement authentication, authorisation and privacy safeguards in a future production system | Yes — course demonstration uses synthetic data |
| No timezone or concurrency policy | Real-world scheduling across regions or simultaneous users is unsupported | Future production concern | Define timezone handling and concurrent booking rules before deployment | Yes — outside course release scope |
| Limited production usability and monitoring | Text-only console without operational monitoring or accessibility assessment | Future improvement | Evaluate accessibility, usability, logging and monitoring for production use | Yes — not required for this teaching application |

Session-only synthetic data and minute-precision local time: SmartCare uses synthetic data stored in memory for one running session. Date/time values use YYYY-MM-DD HH:MM and have minute precision. Records are intentionally lost on exit.
Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: These capabilities are not implemented and are outside the required undergraduate release scope. SmartCare is not intended for clinical or production use.
Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: The application has not been assessed for concurrent users, production scale, timezone handling, monitoring or accessibility. These would need separate requirements and verification before real deployment.
Difference between accepted scope limit and unresolved required behaviour: An accepted scope limitation is functionality deliberately excluded by the requirements, such as persistence or rescheduling. An unresolved required behaviour is a feature that should work under the requirements but has not been implemented or verified. No failing required behaviour was identified in the latest 76-test regression, although final release checks are still in progress.
PG assurance residual risks / owner / status or not applicable: Not applicable — UG-only group. Stage 10 and 11 PG assurance work is not required.


## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| Common Stage 12 regression | `python -m pytest -q` from `project/` at SHA `6b6595180d82dfc6f9e67daf6b20931163df544c`; 76 passed | No failing tests observed | Shiven — continue release verification | No code correction required | Full regression: 76 passed in 0.10s | Automated tests do not establish complete release readiness |
| Independent verification | Anish reported that SmartCare works; exact test output and environment not supplied | Evidence gap; not a confirmed application defect | Shiven and Anish — record reproducible verification details if available | No code change | Shiven's 76-test regression passed; Anish's detailed results pending | Independent setup reproducibility not fully evidenced |

Justified no-change conclusion if no defect found: No new application defect was identified in the latest Stage 12 regression. All 76 tests passed, and previous Stage 9 manual demonstrations covered the main workflows and invalid-input recovery. Therefore, no corrective code change is currently justified. Remaining release activities concern verification evidence, documentation, packaging and final approval rather than an identified runtime failure.
Release blockers still open / status: Final release verification remains in progress. Outstanding activities include completing the final repository and dependency checks, confirming README reproducibility, recording the release review and decision, verifying the source ZIP, and confirming submission arrangements. No failing automated tests are currently known. The release is not yet approved for submission.


## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA: Stage 9 implementation PR: https://github.com/shiven-uc/st1-assignment-3-group7/pull/10. Stage 9 code and evidence were integrated into main. Verified starting SHA: `6b6595180d82dfc6f9e67daf6b20931163df544c`. Stage 12 release PR pending.
Independent reviewer / feedback / response: Anish Atamkur reviewed the Stage 9 work and confirmed agreement with the feedback relayed in PR #10. For Stage 12, Anish reported that SmartCare works. His exact independent commands and test output were not supplied. No additional defects were reported.
Integration commit / full recheck: Stage 9 common integration SHA `6b6595180d82dfc6f9e67daf6b20931163df544c`. From `project/`, `python -m pytest -q` returned 76 passed in 0.10s during Stage 12 verification. Final Stage 12 integration remains pending.
Tracked and untracked file inspection / cleanliness: Before Stage 12 changes, the Stage 9 main branch had a clean working tree. Stage 12 work is being completed on `stage12-release`, with `stage12/stage12_activities_and_evidence.md` modified. Final tracked/untracked inspection remains pending.
Secrets/staff material/caches/tool-metadata exclusion check: Final repository and release ZIP inspection pending. The submission must exclude credentials, real patient information, staff solutions, caches, virtual environments, Stage 8 preparation utilities and recovery metadata.
Candidate recovery plan / known-good SHA: The verified common baseline is `6b6595180d82dfc6f9e67daf6b20931163df544c`. If a Stage 12 change causes a regression, compare it against this checkpoint, correct the bounded change and rerun the full regression suite. Preserve the known-good commit.
Named substantive contributions: Shiven coordinated the Stage 9 implementation, testing, documentation, Git integration and Stage 12 release preparation. Anish Atamkur provided confirmed Stage 9 peer-review feedback and reported that SmartCare works during Stage 12 verification. Further contributions will be recorded when completed.


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: NOT YET READY - final release checks and submission packaging remain outstanding.
Approver / date / rationale and evidence: Shiven is coordinating release preparation. Anish Atamkur reported that SmartCare works. Final group release approval is pending. The latest verified regression returned 76 passed in 0.10s.
What risks remain / conditions / owners: Shiven must complete the final README, dependency, repository and ZIP checks and confirm submission requirements. Independent reproduction evidence from Anish remains limited to his reported feedback.
Can the team explain the system: The team has documented SmartCare's domain objects, shared store, services, pure queries and console responsibilities. Individual understanding will be demonstrated during the course viva.
Can a change be recovered: Yes. Git preserves the verified common checkpoint `6b6595180d82dfc6f9e67daf6b20931163df544c`. Changes can be compared against this commit, corrected and retested.
Common decision / PG decision where different: Common UG release decision is NOT YET READY pending final checks. PG decision is not applicable because both group members are undergraduate students.


## K Final tested release SHA

Exact common tested SHA: `6b6595180d82dfc6f9e67daf6b20931163df544c` — verified from `project/` with `python -m pytest -q`: 76 passed in 0.10s.
Exact PG tested SHA or not applicable: Not applicable — UG-only group.
Final submitted SHA / repository URL: Final Stage 12 submission SHA pending. Repository: https://github.com/shiven-uc/st1-assignment-3-group7
Evidence-only later commit and difference explanation: Stage 12 documentation is being completed after the verified Stage 9 checkpoint. Any later evidence-only commit will be recorded separately from the tested application code.
Executable changes after testing and re-verification: No Stage 12 executable code changes reported so far. Final regression will be repeated against the completed release candidate.
Source ZIP name / SHA correspondence / extracted comparison: Pending — the final source ZIP has not yet been created or checked against the submitted SHA.


## L Submission package verification

- [ ] Feature freeze and scoped requirements traced.
- [ ] Applicable full regressions, integrated demo and invalid paths verified.
- [ ] Architecture/code quality and final AI/dependency checks complete.
- [ ] Root README and project/README reproduced by another verifier.
- [ ] Release notes, technical debt and limitations visible.
- [ ] Independent human review, integration and release decision recorded.
- [ ] Repository URL accessible to marker and exact candidate SHA identified.
- [ ] One source ZIP from submitted commit with root README.md and .gitignore.
- [x] project/ source and all accumulated applicable tests included.
- [x] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [ ] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [ ] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [ ] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: [response]
Deadline/timezone: [response]
Repository access arrangement: [response]
Mixed-candidate upload arrangement: [response]
Oral/video recording/accessibility arrangements: [response]
Remaining administration or release dependency: [response]


## M Formative questions

1. What is a release candidate? [response]

2. What is feature freeze and why is it used? [response]

3. What is regression testing in a release context? [response]

4. What is a known limitation? [response]

5. What is technical debt? [response]

6. What are release notes? [response]

7. What is software maintenance? [response]

8. What is the purpose of the individual demonstration/viva? [response]

9. What should the final responsible-AI check establish before release? [response]

10. What is the main course conclusion about AI and the role of the software engineer? [response]


## N Reflection viva and handover

Strongest evidence SmartCare is ready: All 76 automated tests passed, covering registration, lookup, booking, conflicts, cancellation, queries, service listing and console recovery. The Stage 9 integrated demonstration also behaved as expected.
Weakest area: The application has only been tested as a small, single-session teaching system. It lacks production features such as persistence, authentication and concurrency handling. Independent reproduction evidence is also limited.
How AI use changed from Stage 1 to Stage 12: AI became a more structured review and development aid. Instead of simply accepting suggestions, I used requirements, tests and human judgement to evaluate AI output and reject unnecessary changes.
Start doing — engineering and AI use: Define tests and acceptance criteria earlier, document decisions consistently and check AI suggestions against actual code and requirements.
Stop doing — engineering and AI use: Avoid accepting AI-generated suggestions without verification or adding unnecessary features outside the assessed scope.
Continue doing — engineering and AI use: Continue using Git branches, pull requests, focused tests, full regression tests, peer feedback and responsible AI review.
What worked / caused rework / future delivery improvement: Separating responsibilities and using automated tests helped identify defects and protect existing behaviour. Additional console tests were needed after Copilot identified a coverage gap. Future work would benefit from planning these tests earlier.
One paragraph — If AI can write code why do we still need software engineers: AI can generate code and suggest improvements, but it cannot really take responsibility for understanding stakeholder needs, interpreting requirements, making architectural trade-offs and verifying that software behaves correctly. Software engineers must assess risks, review code, test assumptions and ensure the final product is appropriate for its intended use. SmartCare demonstrated this because AI suggestions still required human decisions and verification before being accepted.

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | SmartCare manages patient, practitioner and appointment information. Stakeholders include patients, practitioners and staff coordinating bookings. Evidence: `project/README.md`. |
| Two requirements and acceptance criteria | FR-05 rejects same-practitioner scheduling conflicts. FR-07 retains cancelled appointments. Evidence: `tests/test_workflows.py`. |
| Domain model and architecture | Patient and Practitioner represent registered participants. Appointment stores their references, date/time and status. Services coordinate operations using one shared store. Evidence: `project/smartcare/`. |
| Design trade-off | Session-only in-memory storage is simple and suitable for the teaching scope, but records disappear on exit. Evidence: `project/README.md`. |
| Meaningful test and its limits / 100 percent coverage | `test_full_booking_cancellation_and_rebooking_workflow` verifies conflicts, cancellation history, identity and rebooking. Passing tests do not prove every possible defect is absent. Evidence: `tests/test_workflows.py`. |
| Diagnosed defect and verification | Stage 8 corrected practitioner conflict comparison and retained cancelled appointment lookup. Regression testing confirmed the fixes. Evidence: Stage 8 record and tests. |
| Shared store and session-state/query responsibilities | One SmartCareDataStore preserves records throughout a session. Queries receive explicit inputs and return new sorted lists without mutation. |
| What would break if session-state lookup/query responsibilities changed? | Creating a new store for each menu action would lose registered records between actions. Mutating query inputs could change stored appointment ordering or state unexpectedly. |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | Appointment.cancel guards its status transition. AppointmentService coordinates booking against registered participants and scheduling conflicts. |
| FR-07 retained history test | Cancel A1, retrieve the same stored object, confirm CANCELLED status and verify all-status listing includes it. Evidence: `tests/test_workflows.py`. |
| Actual AI change rejected/modified or honestly accepted with verification | Accepted Copilot's missing console-test finding and added five passing tests. Rejected optional data-store conflict hardening for the Stage 9 scope. Evidence: Stage 9 Section E. |
| Unresolved limitation / future production work | No persistent storage, authentication, timezone policy, concurrency protection or clinical integration. These are excluded from the course release. |
| Personal implementation contribution | Shiven implemented and integrated SmartCare's query, listing and console functionality and contributed to earlier service repairs. |
| Personal test/review/design/integration contribution | Shiven completed human-first design, implemented tests, evaluated Copilot feedback, documented results and coordinated GitHub integration. Anish provided peer-review feedback. |
| PG agentic change and rescheduling verification | Not applicable |
| PG responsible-AI risk/remediation or supported no finding | Not applicable |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: Not undertaken. No optional code changes were made because the verified release candidate is under feature freeze.
Separate reflection / peer / common team viva evidence links and routing: Stage 12 group reflection is recorded in this document. Individual confidential peer-assessment forms and the common team viva must be submitted through their separately confirmed assessment routes; submission evidence pending.
No further coding stage. Later corrections use the published assessment process.
