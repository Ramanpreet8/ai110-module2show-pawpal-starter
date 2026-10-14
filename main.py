from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")

    mochi.add_task(Task("Morning walk", time(8, 0), 30, "daily", "high"))
    mochi.add_task(Task("Breakfast", time(7, 30), 10, "daily", "high"))
    luna.add_task(Task("Breakfast", time(8, 30), 10, "daily", "medium"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    schedule = Scheduler().build_schedule(owner, available_minutes=60)
    pet_by_task_id = {
        id(task): pet
        for pet in owner.pets
        for task in pet.tasks
    }

    print("Today's Schedule")
    for task in schedule:
        pet = pet_by_task_id[id(task)]
        print(
            f"{task.scheduled_time:%H:%M} - {task.description} "
            f"({pet.name}, {pet.species}; {task.duration_minutes} min, "
            f"{task.priority} priority)"
        )


if __name__ == "__main__":
    main()