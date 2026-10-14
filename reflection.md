# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My three core user actions were adding a pet, scheduling a task for a pet, and viewing today's schedule. I chose four classes: `Task` represents one care activity, including its description, scheduled time, duration, frequency, priority, and completion state. `Pet` stores a pet's basic information and its tasks. `Owner` stores the owner's pets and can gather their tasks with `get_all_tasks()`. `Scheduler` reads the owner's tasks and is responsible for sorting and filtering them into a daily plan based on the available time.

**b. Design changes**

The design has not changed so far. I asked AI to review the Python skeleton against the UML. The `Owner` → `Pet` → `Task` relationships are represented by the owner's pet list and each pet's task list, and the scheduler depends on the owner rather than duplicating those collections. One detail to keep in mind during implementation is that `get_all_tasks()` returns a flat list; schedule output may need to preserve which pet each task belongs to. I left the skeleton unchanged because the existing relationships are sufficient for this draft, and adding another class or duplicating the pet reference in `Task` would add complexity before it is needed.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
