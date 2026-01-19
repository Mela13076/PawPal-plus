# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Three core actions user should be able to perform: 
    1. Add and manage pet tasks
    2. View daily care schedule
    3. Update pet information
    4. add a pet

- Briefly describe your initial UML design:
    -The inital UML deisgn classes for Owner, Pet, Scheduler, and task. IT will focus on separating data, task managemetn, and scheduling. 
- What classes did you include, and what responsibilities did you assign to each?
    - Owner: includes the pet's owner information like name and availability. 
    - Pet: includes pet information like name, type, breed, and any special care instructions.
    - Task: Each task will have the name, duration, priority, and category. 
    - Scheduler: This will handle generating the daily care plan. It will concider task priority, time constriants, and create a final schedule. 
    - Task Manager: This will handle adding, remvoing, and updating tasks. 

**b. Design changes**

- Did your design change during implementation? If yes, describe at least one change and why you made it.
    - Yes, I decided not to create task manager and instead have the task as a list associated with the pet. 


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    -The scheduler considers available daily time, task priority, task duration, completion status, and scheduled time.
- How did you decide which constraints mattered most
    - Priority and time availability mattered most because the goal is to complete the most important tasks without exceeding the owner’s available time.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    - The conflict detection only checks adjacent tasks after sorting by time instead of checking every possible pair.
- Why is that tradeoff reasonable for this scenario?
    -It keeps the algorithm efficient and readable while still catching realistic scheduling conflicts.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    - I used AI to brainstorm class design, refactor methods, improve readability, and help generate test cases.
- What kinds of prompts or questions were most helpful?
    - Asking how to simplify logic, improve readability, or verify correctness of algorithms was most useful.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    - I did not fully accept suggestions that added unnecessary complexity or extra classes.
- How did you evaluate or verify what the AI suggested?
    - I compared it against the project requirements and chose the simpler approach that still met the goals.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    - I tested task ordering, time limits, skipping completed tasks, recurring task creation, and conflict detection.
- Why were these tests important?
    - They verify the core scheduling logic and ensure the system behaves correctly in common and edge cases.

**b. Confidence**

- How confident are you that your scheduler works correctly?
    - I am fairly confident because the main behaviors are covered by tests.
- What edge cases would you test next if you had more time?
    - Overlapping recurring tasks, tasks without a scheduled time, and multiple pets with many tasks.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    - I am most satisfied with the scheduling logic and conflict detection working together cleanly.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    - I would improve the UI integration and add more flexible scheduling preferences.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    - Clear system design and careful testing make it much easier to use AI effectively without losing control of the project.
