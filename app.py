from datetime import time

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
            )
            owner.pets[pet_index].add_task(task)
            st.session_state.schedule = None
            st.success(f"Added '{task.description}' for {owner.pets[pet_index].name}.")

all_tasks = owner.get_all_tasks()
if all_tasks:
    task_rows = [
        {
            "Pet": pet.name,
            "Task": task.description,
            "Time": task.scheduled_time.strftime("%H:%M"),
            "Duration (min)": task.duration_minutes,
            "Priority": task.priority,
            "Complete": task.is_complete,
        }
        for pet in owner.pets
        for task in pet.tasks
    ]
    st.dataframe(task_rows, hide_index=True, use_container_width=True)

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
