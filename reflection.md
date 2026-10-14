# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My three core user actions were adding a pet, scheduling a task for a pet, and viewing today's schedule. I chose four classes: `Task` represents one care activity, including its description, scheduled time, duration, frequency, priority, and completion state. `Pet` stores a pet's basic information and its tasks. `Owner` stores the owner's pets and can gather their tasks with `get_all_tasks()`. `Scheduler` reads the owner's tasks and is responsible for sorting and filtering them into a daily plan based on the available time.

**b. Design changes**

The design grew from its initial four-class skeleton. I added `Task.due_date` so recurring tasks can be scheduled for a later day, plus methods for sorting, filtering, completing recurring tasks, and detecting conflicts. `Scheduler` still obtains all tasks through `Owner.get_all_tasks()`. I kept each pet's task list as the source of the pet-task relationship rather than adding a separate `Pet` reference to `Task`; the UI can display the associated pet by looking up which pet owns a task.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler excludes completed and future-due tasks, prioritizes high- before medium- and low-priority work, and includes tasks only while they fit the available-minute budget. It returns the selected tasks in scheduled-time order. Priority and the time budget matter most for deciding what fits; time order then makes the resulting plan easy to follow. Pet filters and exact-time conflict warnings help the owner inspect and refine the plan.

**b. Tradeoffs**

Conflict detection warns only when unfinished tasks share the same due date and exact start time; it does not detect tasks whose durations overlap. This keeps conflict checks lightweight and easy to explain, and the warning still catches the clearest scheduling collision. The tradeoff is that the owner may need to notice near-time overlaps manually.

---

## 3. AI Collaboration

**a. How you used AI**

I used the AI coding assistant to turn the class brainstorm into a Mermaid diagram and dataclass skeleton, implement the backend and Streamlit wiring, and draft and expand tests. The most helpful requests were specific and grounded in the project files, such as asking how the scheduler should retrieve all tasks through the owner, and asking for edge cases around recurrence and scheduling. Running the demo and tests let me check the proposed behavior instead of relying on code generation alone.

**b. Judgment and verification**

One design choice I kept deliberately simple was the ownership relationship: I did not add another association class or duplicate a pet reference on every task. The owner stores pets and each pet stores its tasks; when the UI needs a pet name, it looks up the task in those lists. I verified this approach by exercising multi-pet scheduling in the demo and testing task filtering, conflict detection, and recurrence.

---

## 4. Testing and Verification

**a. What you tested**

The 12 automated tests cover task completion and addition; sorting; filtering by pet and completion status; daily, weekly, and one-time recurrence behavior; exact-date-and-time conflict detection; empty owners; future-due tasks; and priority selection within a time budget. These tests check both ordinary use and edge cases that could otherwise result in completed work reappearing, future tasks appearing too early, or a schedule exceeding its time limit.

**b. Confidence**

I am reasonably confident in the tested core behavior: all 12 tests passed, and I also ran the terminal demo and checked the Streamlit pet/task forms, conflict warning, and generated schedule. The main limitation is that conflict detection only identifies identical start times, not duration overlaps. I would next test overlapping task durations, duplicate pet names in the UI filters, and more interactions through Streamlit's test harness.

---

## 5. Reflection

**a. What went well**

I am most satisfied that the same multi-pet backend powers both the terminal demo and the Streamlit UI, and that the schedule's filtering, recurrence, and conflict-warning behavior is documented and tested.

**b. What you would improve**

I would add duration-overlap detection and stronger schedule explanations so owners can see why a task was included or left out. I would also add persistent storage; the current Streamlit session state does not retain information across separate app sessions.

**c. Key takeaway**

The AI coding assistant's file-aware edits, iterative feedback, and ability to help draft tests were the most effective features. I kept work organized with separate, focused phase requests and clear file scopes; I did not actually create separate chat sessions, but keeping each phase's request distinct still helped limit context switching. I modified the suggestion to add more ownership structure: the existing nested lists were enough, so I avoided adding a new class or duplicate relationship. I learned that being the lead architect means setting boundaries, choosing which suggestions fit the design, verifying generated work with tests and runtime output, and documenting known limitations rather than treating plausible code as proof.
