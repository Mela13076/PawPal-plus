def pets_for_llm(pets_list):
    return [{"name": p["name"], "species": p["species"]} for p in pets_list]

def plan_for_llm(plan_tasks):
    return [
        {
            "pet_name": t.pet_name,
            "description": t.description,
            "time_hhmm": minutes_to_label(t.time),
            "duration_minutes": t.duration_minutes,
            "priority": t.priority,
            "frequency": t.frequency,
        }
        for t in plan_tasks
    ]

def time_to_minutes(t) -> int:
    return t.hour * 60 + t.minute


def minutes_to_label(minutes: int) -> str:
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"

