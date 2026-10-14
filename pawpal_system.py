from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time


@dataclass
class Task:
    description: str
    scheduled_time: time
    duration_minutes: int
    frequency: str
    priority: str
    is_complete: bool = False

    def __post_init__(self) -> None:
        if type(self.duration_minutes) is not int or self.duration_minutes <= 0:
            raise ValueError("duration_minutes must be a positive integer")
        if self.priority not in {"low", "medium", "high"}:
            raise ValueError("priority must be 'low', 'medium', or 'high'")

    def mark_complete(self) -> None:
        self.is_complete = True


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
    def build_schedule(
        self, owner: Owner, available_minutes: int
    ) -> list[Task]:
        if type(available_minutes) is not int or available_minutes < 0:
            raise ValueError("available_minutes must be a non-negative integer")

        priority_rank = {"high": 0, "medium": 1, "low": 2}
        tasks = owner.get_all_tasks()
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
            if task.is_complete or task.duration_minutes > remaining_minutes:
                continue
            selected.append(task)
            remaining_minutes -= task.duration_minutes

        return sorted(selected, key=lambda task: task.scheduled_time)