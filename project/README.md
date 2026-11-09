# SmartCare — Stage 12 Undergraduate Release Candidate

Software Technology 1, Assignment 3 — 2026 revision 2.

SmartCare is a Python application for registering patients and practitioners, booking and cancelling appointments, retrieving appointment history, and listing a practitioner's appointments.

The application uses the Python standard library at runtime. Development tests use pytest.

## Requirements and Setup

The course's documented baseline is Python 3.13 with pytest 8.3.5. The team's latest local verification used Python 3.14.3 and pytest 8.3.5.

From the repository root, open a terminal and run:

```powershell
cd project
python -m pip install -r requirements-dev.txt
```

No additional third-party runtime dependencies are required.

## Running SmartCare

Open a terminal in the `project/` directory.

Run the supplied demonstration:

```powershell
python main.py
```

Run the interactive menu:

```powershell
python main.py --interactive
```

The interactive menu supports:

| Choice | Operation |
|---|---|
| 1 | Register patient |
| 2 | Find patient |
| 3 | Register practitioner |
| 4 | Find practitioner |
| 5 | Book appointment |
| 6 | Cancel appointment |
| 7 | Find appointment |
| 8 | List practitioner appointments |
| 0 | Exit |

Date/time input must use `YYYY-MM-DD HH:MM`, for example `2026-12-01 09:00`.

When listing appointments, leave the status blank to include all appointments, or enter `scheduled`, `cancelled` or `completed`.

## Running Tests

From `project/`:

```powershell
python -m pytest -q
```

Latest local Stage 12 verification: **76 passed, 0 failed**, in 0.13 seconds.

The test suite includes cumulative regression tests covering registration, lookup, booking, conflicts, cancellation, retained history, listing, sorting, filtering and console recovery.

## Application Responsibilities

- `domain.py` — Patient, Practitioner and Appointment objects, validation and guarded cancellation.
- `data_store.py` — Shared in-memory patient, practitioner and appointment collections, lookup and storage.
- `services.py` — Registration, lookup, booking, cancellation and validated practitioner appointment listing.
- `queries.py` — Pure appointment filtering and sorting using explicit inputs and a named sorting key.
- `console.py` — Date/time parsing, appointment formatting, demonstration and interactive menu.
- `main.py` — Selects the demonstration or interactive menu.

The services share one `SmartCareDataStore` for each interactive session.

## Rules and Behaviour

- IDs are trimmed, non-blank and case-sensitive.
- Appointments reference the actual registered Patient and Practitioner objects.
- Duplicate IDs and invalid values are rejected.
- A practitioner cannot have two SCHEDULED appointments at the same date/time.
- Different practitioners can have appointments at the same time, including for the same patient.
- Cancellation changes an existing appointment's status to CANCELLED without deleting its history.
- Cancelling an appointment frees the practitioner's time slot for another appointment.
- Practitioner listing returns a new list sorted by date/time and then appointment ID.
- Listing without a status filter includes SCHEDULED, CANCELLED and COMPLETED appointments.
- Recoverable input errors display messages and return to the menu.

## Scope and Limitations

SmartCare uses **session-only in-memory storage**. All registered records and appointments are lost when the application exits. Restart persistence (FR-10) is retired and is not required.

There is no database, file-based persistence, rescheduling or PG-only extension in this undergraduate release candidate.

Booking uses local minute-precision date/time values. No age, appointment-duration, patient-conflict or past-date restriction is imposed by the supplied requirements.

The application has no authentication, clinical integration, notifications, billing, production monitoring or concurrency guarantees. It is intended only as a teaching demonstration, not for production healthcare use.

The application uses synthetic teaching data only. Do not enter real patient information.

## Responsible AI and Release Evidence

GitHub Copilot was used to review the Stage 9 implementation. Its recommendation to add automated console tests was accepted and verified. An optional data-store hardening recommendation was not implemented because it was outside the assessed service workflow.

AI suggestions were evaluated by human reviewers and checked against requirements and tests.

Release scope, regression evidence, known limitations, human review and final release decisions are documented in `../stage12/stage12_activities_and_evidence.md`.