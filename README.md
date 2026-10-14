# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

```
Tasks sorted by time:
07:30 - Breakfast
07:30 - Medication
16:00 - Playtime
18:00 - Evening walk

Pending tasks for Mochi:
18:00 - Evening walk
07:30 - Breakfast

Conflict warnings:
Warning: Conflict on 2026-10-13 at 07:30: Mochi: Breakfast, Luna: Medication

Completed 'Breakfast'; next occurrence: 2026-10-14 at 07:30.

Today's Schedule
07:30 - Medication (Luna, cat; 5 min, high priority)
16:00 - Playtime (Luna, cat; 20 min, low priority)
18:00 - Evening walk (Mochi, dog; 30 min, medium priority)
```

## 🧪 Testing PawPal+

```bash
python -m pytest
```

The tests cover task completion and addition, chronological sorting, filtering by
pet and completion status, daily and weekly recurrence, one-time tasks, exact-time
conflict detection, empty owners, future-due tasks, and schedule time-budget and
priority behavior.

```
============================= test session starts ==============================
platform darwin -- Python 3.14.5, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/ramanpreetsingh/ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 12 items

tests/test_pawpal.py ............                                        [100%]

============================== 12 passed in 0.03s ==============================
```

**Confidence level:** 4/5 stars. All 12 automated tests pass across the core
logic and listed edge cases. Conflict detection intentionally checks exact
matching start times rather than overlapping task durations, and the Streamlit
interface is not covered by this pytest suite.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting | `Scheduler.sort_by_time` | Returns a new task list ordered by scheduled time. `build_schedule` prioritizes high, then medium, then low priority within the time budget, and presents selected tasks by time. |
| Filtering | `Scheduler.filter_tasks` | Filters all of an owner's tasks by pet name, completion status, or both. `build_schedule` also omits completed tasks and future-due tasks and skips tasks that do not fit the remaining minute budget. |
| Conflict detection | `Scheduler.detect_conflicts` | Returns warning messages for unfinished tasks with the same due date and exact start time, including tasks belonging to different pets. Duration overlaps without identical start times are not detected. |
| Recurring tasks | `Task.next_occurrence`, `Scheduler.complete_task` | Completing a daily or weekly task adds a fresh instance due one or seven days after completion. One-time tasks do not recur. |
| Multi-pet tasks | `Owner.get_all_tasks`, `Scheduler.build_schedule` | Scheduling reads tasks through the owner's all-pets method. |

Tasks have a due date (defaulting to today) as well as a time of day. Future-due tasks are left out of the current schedule until their due date.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
