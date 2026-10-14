from datetime import date, time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")

    mochi.add_task(Task("Evening walk", time(18, 0), 30, "daily", "medium"))
    mochi.add_task(Task("Breakfast", time(7, 30), 10, "daily", "high"))
    luna.add_task(Task("Medication", time(7, 30), 5, "weekly", "high"))
    luna.add_task(Task("Playtime", time(16, 0), 20, "once", "low"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler()
    print("Tasks sorted by time:")
    for task in scheduler.sort_by_time(owner.get_all_tasks()):
        print(f"{task.scheduled_time:%H:%M} - {task.description}")

    print("\nPending tasks for Mochi:")
    for task in scheduler.filter_tasks(
        owner, pet_name="Mochi", is_complete=False
    ):
        print(f"{task.scheduled_time:%H:%M} - {task.description}")

    print("\nConflict warnings:")
    conflicts = scheduler.detect_conflicts(owner)
    if conflicts:
        for warning in conflicts:
            print(f"Warning: {warning}")
    else:
        print("No conflicts found.")

    today = date.today()
    completed_task = mochi.tasks[1]
    next_task = scheduler.complete_task(
        mochi, completed_task, completed_on=today
    )
    if next_task is not None:
        print(
            f"\nCompleted '{completed_task.description}'; next occurrence: "
            f"{next_task.due_date:%Y-%m-%d} at {next_task.scheduled_time:%H:%M}."
        )

    schedule = scheduler.build_schedule(owner, available_minutes=60)
    pet_by_task_id = {
        id(task): pet
        for pet in owner.pets
        for task in pet.tasks
    }

    print("\nToday's Schedule")
    for task in schedule:
        pet = pet_by_task_id[id(task)]
        print(
            f"{task.scheduled_time:%H:%M} - {task.description} "
            f"({pet.name}, {pet.species}; {task.duration_minutes} min, "
            f"{task.priority} priority)"
        )


if __name__ == "__main__":
    main()