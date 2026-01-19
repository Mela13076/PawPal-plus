from datetime import date, timedelta
import pytest
from pawpal_system import Owner, Pet, Task, Scheduler


def test_ordering_by_priority_then_duration():
    owner = Owner("Amelia", daily_time_available=60)
    dog = Pet("Luna", "Dog")
    cat = Pet("Milo", "Cat")

    # same priority, different durations
    dog.add_task(Task("Short meds", 5, 4, time=480, pet_name="Luna"))
    dog.add_task(Task("Long grooming", 20, 4, time=540, pet_name="Luna"))

    # higher priority should come first
    cat.add_task(Task("Walk", 15, 5, time=600, pet_name="Milo"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    plan, _ = Scheduler().generate_plan(owner)

    assert [t.description for t in plan] == ["Walk", "Short meds", "Long grooming"]


def test_respects_time_limit_and_skips_tasks_that_do_not_fit():
    owner = Owner("Amelia", daily_time_available=20)
    pet = Pet("Luna", "Dog")

    pet.add_task(Task("Walk", 25, 5, time=480, pet_name="Luna"))       # too long
    pet.add_task(Task("Feed", 5, 4, time=500, pet_name="Luna"))        # should fit
    pet.add_task(Task("Quick play", 10, 3, time=520, pet_name="Luna")) # should fit

    owner.add_pet(pet)

    plan, explanation = Scheduler().generate_plan(owner)

    assert [t.description for t in plan] == ["Feed", "Quick play"]
    assert any("not enough time" in line for line in explanation)


def test_empty_tasks_returns_empty_plan():
    owner = Owner("Amelia", daily_time_available=30)
    plan, explanation = Scheduler().generate_plan(owner)

    assert plan == []
    assert isinstance(explanation, list)


def test_empty_time_available_returns_empty_plan():
    owner = Owner("Amelia", daily_time_available=0)
    pet = Pet("Milo", "Cat")
    pet.add_task(Task("Feed", 5, 5, time=480, pet_name="Milo"))
    owner.add_pet(pet)

    plan, explanation = Scheduler().generate_plan(owner)

    assert plan == []
    assert any("not enough time" in line for line in explanation)


def test_completed_tasks_are_skipped():
    owner = Owner("Amelia", daily_time_available=30)
    pet = Pet("Luna", "Dog")

    t1 = Task("Walk", 15, 5, time=480, pet_name="Luna")
    t2 = Task("Feed", 5, 4, time=500, pet_name="Luna")
    t1.mark_complete()

    pet.add_task(t1)
    pet.add_task(t2)
    owner.add_pet(pet)

    plan, explanation = Scheduler().generate_plan(owner)

    assert [t.description for t in plan] == ["Feed"]
    assert any("already completed" in line for line in explanation)


def test_task_numbers_are_unique_across_instances():
    t1 = Task("A", 5, 1, time=480, pet_name="Luna")
    t2 = Task("B", 5, 1, time=490, pet_name="Luna")
    t3 = Task("C", 5, 1, time=500, pet_name="Luna")

    assert len({t1.number, t2.number, t3.number}) == 3
    assert t1.number < t2.number < t3.number


def test_task_mark_complete_sets_completed_true():
    task = Task("Feed pet", 5, 3, time=480, pet_name="Milo")
    assert task.completed is False

    task.mark_complete()
    assert task.completed is True


def test_adding_task_to_pet_increases_task_count():
    pet = Pet("Luna", "Dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task("Morning walk", 20, 5, time=480, pet_name="Luna"))
    pet.add_task(Task("Evening walk", 20, 2, time=1080, pet_name="Luna"))
    pet.add_task(Task("Night walk", 20, 5, time=1260, pet_name="Luna"))

    assert len(pet.tasks) == 3


def test_sort_by_time_returns_chronological_order():
    scheduler = Scheduler()
    tasks = [
        Task("Later", 10, 3, time=600, pet_name="Luna"),
        Task("Earlier", 10, 3, time=480, pet_name="Luna"),
        Task("Latest", 10, 3, time=900, pet_name="Milo"),
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)
    assert [t.time for t in sorted_tasks] == [480, 600, 900]


def test_marking_daily_task_complete_creates_next_day_task():
    owner = Owner("Amelia", daily_time_available=60)
    pet = Pet("Luna", "Dog")
    owner.add_pet(pet)

    today = date.today()
    t = Task("Walk", 20, 5, time=480, pet_name="Luna", frequency="daily", due_date=today)
    pet.add_task(t)

    scheduler = Scheduler()
    ok = scheduler.mark_task_complete(owner, t.number)

    assert ok is True
    assert t.completed is True

    # New task should be created
    assert len(pet.tasks) == 2
    new_task = pet.tasks[1]

    assert new_task.description == "Walk"
    assert new_task.completed is False
    assert new_task.due_date == today + timedelta(days=1)
    assert new_task.time == 480
    assert new_task.pet_name == "Luna"


def test_detect_conflicts_flags_same_start_time():
    scheduler = Scheduler()

    t1 = Task("Feed", 10, 4, time=500, pet_name="Luna")
    t2 = Task("Meds", 5, 5, time=500, pet_name="Milo")  # same start time => overlap

    warnings = scheduler.detect_conflicts([t1, t2])

    assert len(warnings) == 1
    assert "Time conflict" in warnings[0]
