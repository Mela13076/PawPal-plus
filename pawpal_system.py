from dataclasses import dataclass, field
from typing import List, Tuple, ClassVar, Optional
from datetime import date, timedelta

@dataclass
class Task:
    description: str
    duration_minutes: int
    priority:  int # scale of 1-5 (5 highest)
    time: int #minutes since midnight
    pet_name: str
    frequency: str = "daily" #daily, weekly, monthly
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    number: int = field(init=False)
    _counter: ClassVar[int] = 0 # class variable for unique numbering


    def __post_init__(self) -> None:
        #assign_number function called after init to assign unique number
        Task._counter += 1
        self.number = self._counter
        

    def mark_complete(self) -> None:
        self.completed = True

    def mark_incomplete(self) -> None:
        self.completed = False


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    '''def remove_task(self, task_description: str) -> None:
        for task in self.tasks:
            if task.description == task_description:
                self.tasks.remove(task)'''
    
    def remove_task(self, task_number: int) -> None:
        for task in self.tasks:
            if task.number == task_number:
                self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        return self.tasks #list(self.tasks)


@dataclass
class Owner:
    name: str
    daily_time_available: int  # minutes
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks
    
    def get_all_task_by_pet(self):
        tasks_by_pet = {}
        for pet in self.pets:
            tasks_by_pet[pet.name] = pet.get_tasks()
        return tasks_by_pet
# -------------------------
# Scheduling Logic
# -------------------------

class Scheduler:
    def generate_plan(self, owner: Owner) -> Tuple[List[Task], List[str]]:
        """
        Returns:
        - plan: tasks selected for today
        - explanation: reasons why tasks were selected or skipped
        """
        available_minutes = owner.daily_time_available
        explanation: List[str] = []
        selected: List[Task] = []

        tasks = owner.get_all_tasks()
        #sort by priority (high to low), then by duration (short to long)
        tasks.sort(key=lambda t: (-t.priority, t.duration_minutes))

        for task in tasks:
            
            if task.completed:
                explanation.append(
                    f"Skipped '{task.description}' (already completed)."
                )
                continue
            if task.duration_minutes > available_minutes:
                explanation.append(
                    f"Skipped '{task.description}' (not enough time)."
                )
                continue
            selected.append(task)
            available_minutes -= task.duration_minutes
            explanation.append(
                f"Scheduled '{task.description}' (priority {task.priority})."
            )

        return selected, explanation
    
    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: t.time)
    
    def filter_by_completed(self, tasks: List[Task], completed: bool) -> List[Task]:
        return [t for t in tasks if t.completed == completed]
    
    def mark_task_complete(self, owner: Owner, task_number: int) -> bool:
        """
        Marks a task complete by task_number.
        If task is daily/weekly, creates the next occurrence and adds it to the same pet.
        Returns True if the task was found and marked complete; otherwise False.
        """
        for pet in owner.pets:
            for task in pet.tasks:
                if task.number == task_number:
                    task.mark_complete()

                    # Create next occurrence for recurring tasks
                    if task.frequency in ("daily", "weekly"):
                        days = 1 if task.frequency == "daily" else 7
                        next_due = task.due_date + timedelta(days=days)

                        new_task = Task(
                            description=task.description,
                            duration_minutes=task.duration_minutes,
                            priority=task.priority,
                            time=task.time,
                            pet_name=task.pet_name,
                            frequency=task.frequency,
                            completed=False,
                            due_date=next_due,
                        )
                        pet.add_task(new_task)

                    return True
        return False
    
    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """
        Lightweight conflict detection:
        - Returns warning messages for overlapping tasks.
        - Does NOT raise errors or stop the program.
        """
        warnings: List[str] = []

        # Sort by start time so we only compare neighbors
        tasks_sorted = sorted(tasks, key=lambda t: t.time)

        for i in range(len(tasks_sorted) - 1):
            current = tasks_sorted[i]
            nxt = tasks_sorted[i + 1]

            current_end = current.time + current.duration_minutes
            next_start = nxt.time

            # Overlap check
            if next_start < current_end:
                warnings.append(
                    f"Time conflict: '{current.description}' ({current.pet_name}) "
                    f"overlaps with '{nxt.description}' ({nxt.pet_name})."
                )

        return warnings
