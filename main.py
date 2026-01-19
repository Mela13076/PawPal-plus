from pawpal_system import *

from rag import load_knowledge_chunks, retrieve_context
from llm_client import test_gemini_connection

#testing the connection to Gemini LLM
print(test_gemini_connection())

#testing RAG
'''chunks = load_knowledge_chunks("knowledge")
results = retrieve_context("dog medication schedule feeding", chunks, k=3)

for source, text, score in results:
    print(source, score)
    print(text[:200], "...\n")
'''


#testing the pawpal system
'''owner = Owner("Amelia", daily_time_available=55)

pet1 = Pet("Ani", "Dog")
pet2 = Pet("Haze", "Cat")

# Add at least 3 tasks with different durations
task1 = Task("Morning walk", duration_minutes=20, priority=5, time=480, pet_name=pet1.name)
task2 = Task("Feed Haze", duration_minutes=5, priority=4, time=540, pet_name=pet1.name)
task3 = Task("Clean litter box", duration_minutes=10, priority=5, time=600, pet_name=pet2.name)
task4 = Task("Playtime with Ani", duration_minutes=15, priority=3, time=450, pet_name=pet2.name)

pet1.add_task(task1)
pet1.add_task(task2)
pet2.add_task(task3)
pet2.add_task(task4)

# Mark one task complete for filtering demo
task2.mark_complete()

owner.add_pet(pet1)
owner.add_pet(pet2)

# Generate and print today's schedule
scheduler = Scheduler()
plan, explanation = scheduler.generate_plan(owner)

print("=== PawPal+ Today's Schedule ===")
total = 0
for task in plan:
    print(f"[#{task.number}] {task.description} - {task.duration_minutes} min (priority {task.priority})")
    total += task.duration_minutes

print(f"\nTotal scheduled time: {total} min (out of {owner.daily_time_available} min)\n")

print("=== Reasoning ===")
for line in explanation:
    print("-", line)

print("\n=== Tasks by Pet ===")
tasks_by_pet = owner.get_all_task_by_pet()
for pet_name, tasks in tasks_by_pet.items():
    print(f"{pet_name}:")
    for task in tasks:
        print(f"  [#{task.number}] {task.description} at {task.time} min")

print("\n=== Tasks Sorted by Time ===")
sorted_by_time = scheduler.sort_by_time(owner.get_all_tasks())
for task in sorted_by_time:
    print(f"[#{task.number}] {task.description} at {task.time} min")

print("\n=== Incomplete Tasks ===")
incomplete_tasks = scheduler.filter_by_completed(owner.get_all_tasks(), completed=False)
for task in incomplete_tasks:
    print(f"[#{task.number}] {task.description} (incomplete)")

print("\n=== Completed Tasks ===")
completed_tasks = scheduler.filter_by_completed(owner.get_all_tasks(), completed=True)
for task in completed_tasks:
    print(f"[#{task.number}] {task.description} (completed)")

print("\n=== Mark Task Complete (Recurring) ===")
daily_task = Task("Give vitamins", duration_minutes=2, priority=2, time=615, pet_name=pet1.name)
weekly_task = Task("Brush coat", duration_minutes=8, priority=3, time=630, pet_name=pet1.name, frequency="weekly")
monthly_task = Task("Weigh-in", duration_minutes=5, priority=2, time=645, pet_name=pet1.name, frequency="monthly")

pet1.add_task(daily_task)
pet1.add_task(weekly_task)
pet1.add_task(monthly_task)

print("Before:", [(t.description, t.due_date, t.completed) for t in pet1.get_tasks() if t.description in {"Give vitamins", "Brush coat", "Weigh-in"}])

result_daily = scheduler.mark_task_complete(owner, daily_task.number)
result_weekly = scheduler.mark_task_complete(owner, weekly_task.number)
result_monthly = scheduler.mark_task_complete(owner, monthly_task.number)

print("Mark daily:", result_daily)
print("Mark weekly:", result_weekly)
print("Mark monthly:", result_monthly)
print("After:", [(t.description, t.due_date, t.completed) for t in pet1.get_tasks() if t.description in {"Give vitamins", "Brush coat", "Weigh-in"}])

print("\n=== Detect Conflicts ===")
conflict_task1 = Task("Short walk", duration_minutes=20, priority=3, time=560, pet_name=pet1.name)
conflict_task2 = Task("Nail trim", duration_minutes=15, priority=3, time=570, pet_name=pet2.name)
non_conflict_task = Task("Treats", duration_minutes=10, priority=1, time=590, pet_name=pet2.name)

pet1.add_task(conflict_task1)
pet2.add_task(conflict_task2)
pet2.add_task(non_conflict_task)

warnings = scheduler.detect_conflicts(owner.get_all_tasks())
for warning in warnings:
    print("-", warning)'''
