from datetime import date, time

from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_scheduler_sorts_tasks_by_time() -> None:
    later = Task("Walk", time(9, 0), 20, "once", "medium")
    earlier = Task("Breakfast", time(7, 0), 10, "once", "high")

    assert Scheduler().sort_by_time([later, earlier]) == [earlier, later]


def test_filter_tasks_by_pet_and_completion_status() -> None:
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    pending = Task("Walk", time(8, 0), 20, "once", "medium")
    completed = Task("Breakfast", time(7, 0), 10, "once", "high")
    completed.mark_complete()
    other_pet_task = Task("Medication", time(9, 0), 5, "once", "high")
    mochi.tasks.extend([pending, completed])
    luna.add_task(other_pet_task)
    owner.pets.extend([mochi, luna])

    tasks = Scheduler().filter_tasks(owner, pet_name="mochi", is_complete=False)

    assert tasks == [pending]


def test_daily_completion_creates_next_occurrence() -> None:
    pet = Pet("Mochi", "dog")
    task = Task(
        "Breakfast", time(7, 0), 10, "daily", "high",
        due_date=date(2026, 10, 13),
    )
    pet.add_task(task)

    next_task = Scheduler().complete_task(
        pet, task, completed_on=date(2026, 10, 13)
    )

    assert task.is_complete is True
    assert next_task is not None
    assert next_task.due_date == date(2026, 10, 14)
    assert next_task.is_complete is False
    assert next_task in pet.tasks


def test_weekly_completion_creates_next_occurrence() -> None:
    pet = Pet("Luna", "cat")
    task = Task("Medication", time(9, 0), 5, "weekly", "high")
    pet.add_task(task)

    next_task = Scheduler().complete_task(
        pet, task, completed_on=date(2026, 10, 13)
    )

    assert next_task is not None
    assert next_task.due_date == date(2026, 10, 20)


def test_conflict_detection_warns_for_same_due_date_and_time() -> None:
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    due_date = date(2026, 10, 13)
    mochi.add_task(
        Task("Walk", time(8, 0), 30, "once", "high", due_date=due_date)
    )
    luna.add_task(
        Task("Medication", time(8, 0), 5, "once", "high", due_date=due_date)
    )
    owner.pets.extend([mochi, luna])

    warnings = Scheduler().detect_conflicts(owner)

    assert len(warnings) == 1
    assert "Mochi: Walk" in warnings[0]
    assert "Luna: Medication" in warnings[0]


def test_schedule_excludes_tasks_not_yet_due() -> None:
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    pet.add_task(
        Task(
            "Future walk",
            time(8, 0),
            20,
            "once",
            "high",
            due_date=date(2026, 10, 14),
        )
    )
    owner.add_pet(pet)

    schedule = Scheduler().build_schedule(
        owner, available_minutes=60, schedule_date=date(2026, 10, 13)
    )

    assert schedule == []
