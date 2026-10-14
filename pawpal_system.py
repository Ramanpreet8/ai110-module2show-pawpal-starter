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

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> list[Task]:
        pass


class Scheduler:
    def build_schedule(
        self, owner: Owner, available_minutes: int
    ) -> list[Task]:
        pass