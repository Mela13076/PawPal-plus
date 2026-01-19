import streamlit as st
from datetime import time as dt_time
from pawpal_system import Owner, Pet, Scheduler, Task
from rag import load_knowledge_chunks, retrieve_context
from llm_client import GeminiClient  
from helper_function import pets_for_llm, plan_for_llm, time_to_minutes, minutes_to_label


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("Plan pet care tasks for the day and generate a schedule.")

#prevents re-reading files on every rerun
@st.cache_data
def get_knowledge_chunks():
    return load_knowledge_chunks("knowledge")


if "pets" not in st.session_state:
    st.session_state.pets = []
if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
daily_time_available = st.number_input(
    "Daily time available (minutes)", min_value=15, max_value=600, value=120, step=15
)

st.divider()

st.subheader("Pets")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    if not pet_name.strip():
        st.error("Pet name is required.")
    else:
        st.session_state.pets.append({"name": pet_name.strip(), "species": species})

if st.session_state.pets:
    st.write("Current pets:")
    st.table(st.session_state.pets)
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Tasks")
st.caption("Add tasks for specific pets, then generate a schedule.")

if st.session_state.pets:
    pet_options = [p["name"] for p in st.session_state.pets]
    with st.form("add_task_form", clear_on_submit=True):
        task_description = st.text_input("Task description", value="Morning walk")
        task_pet = st.selectbox("Pet", pet_options)
        cols = st.columns(3)
        with cols[0]:
            duration_minutes = st.number_input(
                "Duration (minutes)", min_value=5, max_value=240, value=20, step=5
            )
        with cols[1]:
            priority = st.slider("Priority (1-5)", min_value=1, max_value=5, value=4)
        with cols[2]:
            task_time = st.time_input("Start time", value=dt_time(8, 0))
        cols_2 = st.columns(2)
        with cols_2[0]:
            frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"], index=0)
        with cols_2[1]:
            due_date = st.date_input("Due date")
        add_task = st.form_submit_button("Add task")

    if add_task:
        if not task_description.strip():
            st.error("Task description is required.")
        else:
            st.session_state.tasks.append(
                {
                    "description": task_description.strip(),
                    "duration_minutes": int(duration_minutes),
                    "priority": int(priority),
                    "time": time_to_minutes(task_time),
                    "pet_name": task_pet,
                    "frequency": frequency,
                    "completed": False,
                    "due_date": due_date,
                }
            )
else:
    st.info("Add a pet before creating tasks.")

if st.session_state.tasks:
    display_rows = []
    for idx, t in enumerate(st.session_state.tasks, start=1):
        display_rows.append(
            {
                "#": idx,
                "Task": t["description"],
                "Pet": t["pet_name"],
                "Start": minutes_to_label(t["time"]),
                "Duration": t["duration_minutes"],
                "Priority": t["priority"],
                "Frequency": t["frequency"],
                "Due": t["due_date"],
            }
        )
    st.write("Current tasks:")
    st.table(display_rows)

    remove_options = [f"{row['#']}: {row['Task']} ({row['Pet']})" for row in display_rows]
    remove_choice = st.selectbox("Remove task", options=["None"] + remove_options)
    if st.button("Remove selected task"):
        if remove_choice != "None":
            remove_index = int(remove_choice.split(":", 1)[0]) - 1
            st.session_state.tasks.pop(remove_index)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate the plan using your scheduling logic.")

if st.button("Generate schedule"):
    owner = Owner(name=owner_name.strip() or "Owner", daily_time_available=int(daily_time_available))
    pets_by_name = {}
    for pet_data in st.session_state.pets:
        pet = Pet(name=pet_data["name"], species=pet_data["species"])
        owner.add_pet(pet)
        pets_by_name[pet.name] = pet

    for task_data in st.session_state.tasks:
        pet = pets_by_name.get(task_data["pet_name"])
        if not pet:
            continue
        task = Task(
            description=task_data["description"],
            duration_minutes=task_data["duration_minutes"],
            priority=task_data["priority"],
            time=task_data["time"],
            pet_name=task_data["pet_name"],
            frequency=task_data["frequency"],
            completed=task_data["completed"],
            due_date=task_data["due_date"],
        )
        pet.add_task(task)

    scheduler = Scheduler()
    plan, explanation = scheduler.generate_plan(owner)
    plan_sorted = scheduler.sort_by_time(plan)
    warnings = scheduler.detect_conflicts(plan_sorted)

    # -------------------------
    # PetBot (RAG + Gemini)
    # -------------------------
    try:
        chunks = get_knowledge_chunks()

        # Build a simple query using pets + task keywords
        task_words = " ".join([t["description"] for t in st.session_state.tasks])
        species_words = " ".join([p["species"] for p in st.session_state.pets])
        query = f"{species_words} {task_words} scheduling feeding meds grooming enrichment routine conflicts"

        retrieved = retrieve_context(query, chunks, k=3)
        snippets_for_llm = [(src, txt) for (src, txt, _score) in retrieved]

        client = GeminiClient()

        petbot_text = client.answer_from_snippets(
            owner_name=owner.name,
            daily_time_available=owner.daily_time_available,
            pets=pets_for_llm(st.session_state.pets),
            plan=plan_for_llm(plan_sorted),
            conflicts=warnings,
            snippets=snippets_for_llm,
        )

        st.subheader("PetBot explanation")
        st.write(petbot_text)

        # Optional: show sources
        with st.expander("Sources used"):
            for src, _txt, score in retrieved:
                st.write(f"{src} (score={score})")

    except Exception as e:
        st.error("PetBot is unavailable. See error details below.")
        st.exception(e)


    if not plan_sorted:
        st.warning("No tasks scheduled for today. Try increasing time available or priorities.")
    else:
        plan_rows = []
        for task in plan_sorted:
            plan_rows.append(
                {
                    "Task": task.description,
                    "Pet": task.pet_name,
                    "Start": minutes_to_label(task.time),
                    "Duration": task.duration_minutes,
                    "Priority": task.priority,
                }
            )
        st.success("Today's schedule")
        st.table(plan_rows)

    if warnings:
        st.warning("Conflicts detected")
        for warning in warnings:
            st.write(warning)

    if explanation:
        st.subheader("Schedule reasoning")
        for line in explanation:
            st.write(line)
