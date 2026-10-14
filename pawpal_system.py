from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time, timedelta


@dataclass
class Task:
    description: str
    scheduled_time: time
    duration_minutes: int
    frequency: str
    priority: str
    is_complete: bool = False
    due_date: date = field(default_factory=date.today)

    def __post_init__(self) -> None:
        if type(self.duration_minutes) is not int or self.duration_minutes <= 0:
            raise ValueError("duration_minutes must be a positive integer")
        if self.priority not in {"low", "medium", "high"}:
            raise ValueError("priority must be 'low', 'medium', or 'high'")

    def mark_complete(self) -> None:
        self.is_complete = True

    def next_occurrence(self, completed_on: date) -> Task | None:
        """Return the next daily or weekly instance after completion."""
        interval = {"daily": 1, "weekly": 7}.get(self.frequency)
        if interval is None:
            return None

        return Task(
            description=self.description,
            scheduled_time=self.scheduled_time,
            duration_minutes=self.duration_minutes,
            frequency=self.frequency,
            priority=self.priority,
            due_date=completed_on + timedelta(days=interval),
        )


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by their scheduled time without changing the input."""
        return sorted(tasks, key=lambda task: task.scheduled_time)

    def filter_tasks(
        self,
        owner: Owner,
        pet_name: str | None = None,
        is_complete: bool | None = None,
    ) -> list[Task]:
        """Filter all owner tasks by pet name and/or completion status."""
        tasks = owner.get_all_tasks()
        if pet_name is not None:
            matching_tasks = {
                id(task)
                for pet in owner.pets
                if pet.name.casefold() == pet_name.casefold()
                for task in pet.tasks
            }
            tasks = [task for task in tasks if id(task) in matching_tasks]
        if is_complete is not None:
            tasks = [task for task in tasks if task.is_complete is is_complete]
        return tasks

    def complete_task(
        self, pet: Pet, task: Task, completed_on: date | None = None
    ) -> Task | None:
        """Complete a pet's task and add its next recurring occurrence, if any."""
        if not any(pet_task is task for pet_task in pet.tasks):
            raise ValueError("task does not belong to the given pet")
        if task.is_complete:
            raise ValueError("task is already complete")

        task.mark_complete()
        next_task = task.next_occurrence(completed_on or date.today())
        if next_task is not None:
            pet.add_task(next_task)
        return next_task

    def detect_conflicts(self, owner: Owner) -> list[str]:
        """Warn when unfinished tasks share an exact due date and start time."""
        tasks_by_slot: dict[tuple[date, time], list[tuple[str, Task]]] = {}
        for pet in owner.pets:
            for task in pet.tasks:
                if task.is_complete:
                    continue
                slot = (task.due_date, task.scheduled_time)
                tasks_by_slot.setdefault(slot, []).append((pet.name, task))

        warnings = []
        for (due_date, scheduled_time), tasks in sorted(tasks_by_slot.items()):
            if len(tasks) < 2:
                continue
            descriptions = ", ".join(
                f"{pet_name}: {task.description}" for pet_name, task in tasks
            )
            warnings.append(
                f"Conflict on {due_date:%Y-%m-%d} at "
                f"{scheduled_time:%H:%M}: {descriptions}"
            )
        return warnings

    def build_schedule(
        self,
        owner: Owner,
        available_minutes: int,
        schedule_date: date | None = None,
    ) -> list[Task]:
        """Prioritize due tasks within the time budget and return them by time."""
        if type(available_minutes) is not int or available_minutes < 0:
            raise ValueError("available_minutes must be a non-negative integer")

        target_date = schedule_date or date.today()
        priority_rank = {"high": 0, "medium": 1, "low": 2}
        tasks = [
            task
            for task in owner.get_all_tasks()
            if task.due_date <= target_date and not task.is_complete
        ]
        if any(task.priority not in priority_rank for task in tasks):
            raise ValueError("task priority must be 'low', 'medium', or 'high'")

        candidates = sorted(
            enumerate(tasks),
            key=lambda item: (
                priority_rank[item[1].priority],
                item[1].scheduled_time,
                item[0],
            ),
        )

        selected: list[Task] = []
        remaining_minutes = available_minutes
        for _, task in candidates:
            if task.duration_minutes > remaining_minutes:
                continue
            selected.append(task)
            remaining_minutes -= task.duration_minutes

        return self.sort_by_time(selected)
