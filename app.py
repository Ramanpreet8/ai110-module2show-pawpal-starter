from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.markdown("Plan daily care tasks across all of your pets.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
if "schedule" not in st.session_state:
    st.session_state.schedule = None

owner: Owner = st.session_state.owner
owner.name = st.text_input("Owner name", value=owner.name)

st.subheader("Pets")
with st.form("add_pet_form", clear_on_submit=True):
    new_pet_name = st.text_input("Pet name")
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    if not new_pet_name.strip():
        st.error("Enter a name for your pet.")
    else:
        owner.add_pet(Pet(name=new_pet_name.strip(), species=new_pet_species))
        st.session_state.schedule = None
        st.success(f"Added {new_pet_name.strip()} to {owner.name}'s pets.")

if owner.pets:
    st.write(", ".join(f"{pet.name} ({pet.species})" for pet in owner.pets))
else:
    st.info("Add a pet to get started.")

st.divider()
st.subheader("Care tasks")

if not owner.pets:
    st.caption("Add a pet before creating care tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        pet_index = st.selectbox(
            "Pet",
            range(len(owner.pets)),
            format_func=lambda index: owner.pets[index].name,
        )
        task_description = st.text_input("Task description")
        scheduled_time = st.time_input("Scheduled time", value=time(8, 0))
        due_date = st.date_input("Due date", value=date.today())
        duration_minutes = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        add_task = st.form_submit_button("Add task")

    if add_task:
        if not task_description.strip():
            st.error("Enter a description for the task.")
        else:
            task = Task(
                description=task_description.strip(),
                scheduled_time=scheduled_time,
                duration_minutes=int(duration_minutes),
                frequency=frequency,
                priority=priority,
                due_date=due_date,
            )
            owner.pets[pet_index].add_task(task)
            st.session_state.schedule = None
            st.success(f"Added '{task.description}' for {owner.pets[pet_index].name}.")

all_tasks = owner.get_all_tasks()
if all_tasks:
    scheduler = Scheduler()
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        selected_pet = st.selectbox(
            "Filter by pet", ["All pets", *[pet.name for pet in owner.pets]]
        )
    with filter_col2:
        selected_status = st.selectbox(
            "Filter by status", ["All", "Pending", "Completed"]
        )
    filtered_tasks = scheduler.filter_tasks(
        owner,
        pet_name=None if selected_pet == "All pets" else selected_pet,
        is_complete={
            "All": None,
            "Pending": False,
            "Completed": True,
        }[selected_status],
    )
    st.caption(f"{len(filtered_tasks)} task(s) match these filters.")
    filtered_task_ids = {id(task) for task in filtered_tasks}
    st.dataframe(
        [
            {
                "Pet": pet.name,
                "Task": task.description,
                "Due date": task.due_date.isoformat(),
                "Time": task.scheduled_time.strftime("%H:%M"),
                "Duration (min)": task.duration_minutes,
                "Priority": task.priority,
                "Complete": task.is_complete,
            }
            for pet in owner.pets
            for task in pet.tasks
            if id(task) in filtered_task_ids
        ],
        hide_index=True,
        use_container_width=True,
    )

    pending_task_options = [
        (pet_index, task_index)
        for pet_index, pet in enumerate(owner.pets)
        for task_index, task in enumerate(pet.tasks)
        if not task.is_complete
    ]
    if pending_task_options:
        with st.form("complete_task_form"):
            selected_task = st.selectbox(
                "Mark a task complete",
                pending_task_options,
                format_func=lambda selection: (
                    f"{owner.pets[selection[0]].name}: "
                    f"{owner.pets[selection[0]].tasks[selection[1]].description}"
                ),
            )
            mark_complete = st.form_submit_button("Complete task")
        if mark_complete:
            selected_pet_obj = owner.pets[selected_task[0]]
            selected_task_obj = selected_pet_obj.tasks[selected_task[1]]
            next_task = scheduler.complete_task(
                selected_pet_obj, selected_task_obj
            )
            st.session_state.schedule = None
            if next_task is None:
                st.success(f"Completed '{selected_task_obj.description}'.")
            else:
                st.success(
                    f"Completed '{selected_task_obj.description}'. Next occurrence "
                    f"is due {next_task.due_date:%Y-%m-%d}."
                )
    else:
        st.info("All tasks are complete.")

    for warning in scheduler.detect_conflicts(owner):
        st.warning(warning)

st.divider()
st.subheader("Today's schedule")
available_minutes = st.number_input(
    "Available time today (minutes)", min_value=0, value=120, step=15
)
if st.button("Generate schedule"):
    st.session_state.schedule = Scheduler().build_schedule(
        owner, int(available_minutes)
    )

if st.session_state.schedule is not None:
    schedule = st.session_state.schedule
    if not schedule:
        st.info("No tasks fit the available time.")
    else:
        pet_by_task_id = {
            id(task): pet
            for pet in owner.pets
            for task in pet.tasks
        }
        st.dataframe(
            [
                {
                    "Time": task.scheduled_time.strftime("%H:%M"),
                    "Pet": pet_by_task_id[id(task)].name,
                    "Task": task.description,
                    "Duration (min)": task.duration_minutes,
                    "Priority": task.priority,
                }
                for task in schedule
            ],
            hide_index=True,
            use_container_width=True,
        )
