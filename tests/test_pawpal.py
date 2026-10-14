from datetime import time

from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status() -> None:
    task = Task(
        description="Morning walk",
        scheduled_time=time(8, 0),
        duration_minutes=30,
        frequency="daily",
        priority="high",
    )

    task.mark_complete()

    assert task.is_complete is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="dog")
    task = Task(
        description="Breakfast",
        scheduled_time=time(7, 30),
        duration_minutes=10,
        frequency="daily",
        priority="medium",
    )

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task