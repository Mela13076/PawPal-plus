# PawPal+ — RAG-Powered Pet Care Scheduler

## Title and Summary

PawPal+ is an AI-assisted pet care scheduling system that generates daily routines for pets and provides grounded explanations using Retrieval-Augmented Generation (RAG). The system first creates a deterministic schedule using priorities and time constraints, then retrieves relevant pet-care knowledge and uses a Gemini LLM to explain the reasoning and suggest improvements.

This project extends the original PawPal+ scheduler by adding a retrieval-based AI explanation layer that grounds recommendations in domain knowledge instead of generic template explanations.



# Original Project 

The original PawPal+ project was a deterministic scheduling system that allowed users to create pets, define tasks, and generate a daily plan based on priority and available time. The scheduler selected tasks that fit within the daily time budget, skipped completed tasks, and detected scheduling conflicts.

The system also provided rule-based explanations describing why tasks were scheduled or skipped.

Limitations of the original system:

* Explanations were static and template-based
* No domain knowledge grounding
* No contextual pet-care suggestions
* No AI reasoning layer
* No knowledge-based warnings

This final project extends the scheduler with a RAG pipeline that retrieves pet-care documentation and generates grounded explanations.



# Architecture Overview

PawPal+ uses a hybrid architecture combining deterministic scheduling with retrieval-based AI reasoning.

System Flow

User inputs pets + tasks
→ Scheduler.generate_plan() builds schedule
→ detect_conflicts() checks overlaps
→ build_query_from_tasks() creates RAG query
→ load_knowledge_chunks() loads markdown knowledge base
→ retrieve_context() finds relevant chunks
→ GeminiClient generates explanation
→ UI displays schedule + AI explanation

The scheduler determines the plan.
The AI only explains the decisions and suggests improvements.

This separation keeps scheduling deterministic and AI reasoning safe.


# How RAG Works

The RAG pipeline uses a lightweight retrieval system:

1. Markdown files are loaded from the knowledge directory
2. Files are split into overlapping chunks
3. Query is built from:

   * task descriptions
   * pet species
   * scheduling keywords
4. Keyword scoring ranks chunks
5. Top-k chunks are retrieved
6. Snippets are passed to Gemini
7. Gemini generates grounded explanation

The AI is not allowed to modify the schedule — only explain it.



# Knowledge Base

The system retrieves from:

* dog_care.md
* cat_care.md
* general_pet_scheduling.md
* pet_medication_safety.md

These documents provide domain grounding for AI explanations.



# Setup Instructions

## Clone Repository

git clone [https://github.com/yourusername/pawpal-plus](https://github.com/yourusername/pawpal-plus)
cd pawpal-plus

## Install Dependencies

pip install -r requirements.txt


## Add Environment Variables

Create `.env`

GEMINI_API_KEY=your_api_key_here

## Run App

streamlit run app.py



# Sample Interactions

## Example 1 — Balanced Schedule

Input

Morning walk
Give medicine
Feed

Generated Schedule

08:00 — Morning walk
13:00 — Give medicine
15:30 — Feed

AI Explanation

Today's schedule covers essential care tasks and spaces them throughout the day. Exercise is prioritized first, followed by medication and feeding, which helps maintain a consistent routine. This structure supports both physical activity and predictable care timing.

Suggestions

* Add short play session later in the day
* Maintain consistent medication timing
* Consider second walk for stimulation



## Example 2 — Conflict Warning

Input

Medication at 10:00
Walk at 10:05

Output

Conflict detected

AI Explanation

The schedule contains overlapping tasks. Medication timing should be prioritized, and flexible activities like walks may need adjustment to avoid stress.

Warnings

* Medication overlaps with walk



## Example 3 — Limited Time

Input

Daily time available = 30 minutes

Output

Only highest priority tasks scheduled

AI Explanation

Given limited available time, essential care tasks were prioritized. Additional activities such as playtime may be scheduled when more time becomes available.



# Design Decisions

Deterministic Scheduling First
The scheduler always decides the plan. AI never modifies task order.

Lightweight Retrieval Instead of Vector DB
Used keyword scoring to keep system dependency-free and fast.

Chunked Knowledge Retrieval
Documents are split into chunks for more precise context.

AI Only Explains Decisions
Prevents hallucinated scheduling logic.

Tradeoffs

More logic complexity for safer AI
Limited retrieval accuracy vs simplicity
Smaller knowledge base vs faster runtime



# Testing Summary

What Worked

* Scheduler produces valid plans
* RAG retrieves relevant knowledge chunks
* Gemini explanations grounded in context
* Conflict detection integrated into AI output

What Didn't Work Initially

* Retrieval returned irrelevant chunks
* AI responses too long
* Suggestions too generic

Fixes

* Added minimum score threshold
* Limited top-k retrieval
* Improved prompt formatting

# Reliability and Evaluation

Reliability and evaluation in PawPal+ are supported primarily through automated unit tests and retrieval checks. I wrote tests for scheduling behavior, time-limit filtering, completed-task handling, recurring task creation, conflict detection, knowledge loading, retrieval relevance, and Gemini connectivity. I also added basic runtime safeguards, such as clear errors when the knowledge base or API key is missing and a safe fallback response when no relevant knowledge snippets are found. Current limitations are that the system does not yet compute confidence scores, use structured logging, or include a dedicated evaluation harness that summarizes full end-to-end AI performance across multiple test cases.


Here is a **shortened version** that still covers everything required:

---

# Reflection

This project demonstrated how AI can enhance deterministic systems without replacing core logic. By separating scheduling from explanation, the system remains reliable while providing grounded reasoning using retrieved pet-care knowledge.

I learned:

* RAG improves explainability and trust
* AI should not control scheduling decisions
* Prompt structure affects reasoning clarity
* Retrieval grounding improves output quality

## Limitations and Biases

The system relies on a small knowledge base, so suggestions are limited to available documents. Retrieval uses keyword scoring, which may miss relevant context. The AI also does not account for breed-specific needs, medical conditions, or dynamic real-world changes.

## Potential Misuse and Mitigation

Users could misuse the AI for medical decisions. To reduce this risk, the scheduler remains deterministic, the AI only explains decisions, and responses are grounded in retrieved notes rather than invented advice.

## Reliability Testing Insights

Testing showed that retrieval quality directly affects explanation accuracy. Limiting retrieved chunks and improving query construction produced clearer and more relevant suggestions. Separating scheduling from AI reasoning also ensured the schedule remains correct even if retrieval fails.

## AI Collaboration

AI helped refine the structured output format (summary, suggestions, warnings), improving readability. One flawed suggestion was allowing the LLM to modify the schedule, which caused inconsistent behavior. I instead restricted the AI to explanation-only mode.

This project highlights how applied AI systems benefit from combining traditional algorithms with LLM reasoning.




# Project Structure

app.py — UI and orchestration
pawpal_system.py — scheduling logic
rag.py — retrieval system
llm_client.py — Gemini wrapper
knowledge/ — markdown knowledge base
tests/ — unit tests for scheduler and RAG



# Future Improvements

Add citations in UI
Add confidence scoring
Add multi-day scheduling
Add agent planning layer
Add vector embeddings retrieval
Add timeline visualization


# Screenshots 

![PawPal+ Screenshot](assets/pawpalplus.png)
![AI Explanation Screenshot](assets/rag_output.png)


## Demo Video

[![Watch the demo](https://www.loom.com/embed/ddda93fc21a147e098b3ac19084351b4)](https://www.loom.com/share/ddda93fc21a147e098b3ac19084351b4)
