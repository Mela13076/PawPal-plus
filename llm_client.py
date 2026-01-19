import os
import google.generativeai as genai
from typing import List, Tuple, Dict, Any
from dotenv import load_dotenv
load_dotenv()

# Central place to update the model name if needed.
# You can swap this for a different Gemini model in the future.
GEMINI_MODEL_NAME = "gemini-2.5-flash"


class GeminiClient:
    """
    Simple wrapper around the Gemini model.

    Usage:
        client = GeminiClient()
        answer = client.answer_from_snippets(query, snippets)
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "Missing GEMINI_API_KEY environment variable. "
                "Set it in your shell or .env file to enable LLM features."
            )

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    


    def answer_from_snippets(
        self,
        owner_name: str,
        daily_time_available: int,
        pets: List[Dict[str, Any]],
        plan: List[Dict[str, Any]],
        conflicts: List[str],
        snippets: List[Tuple[str, str]],
    ) -> str:
        """
        Generate a PawPal+ explanation using retrieved snippets.

        pets: list like [{"name":"Luna","species":"Dog"}, ...]
        plan: list like [{"pet_name":"Luna","description":"Walk","time_hhmm":"08:00","duration":20,"priority":5}, ...]
        conflicts: list of warning strings from detect_conflicts()
        snippets: list of (filename, text) tuples from retrieval
        """
        if not snippets:
            return (
                "I could not find relevant care notes in the knowledge base. "
                "Here is the schedule based on your tasks and constraints."
            )

        context_blocks = []
        for filename, text in snippets:
            context_blocks.append(f"Source: {filename}\n{text}\n")

        context = "\n\n".join(context_blocks)

        prompt = f"""
            You are PetBot, a helpful assistant inside the PawPal+ scheduling app.

            Goal:
            Explain today's pet-care schedule clearly and safely, using the retrieved care notes as supporting context.

            Inputs:
            Owner: {owner_name}
            Daily time available (minutes): {daily_time_available}

            Pets:
            {pets}

            Today's scheduled tasks (already chosen by the scheduler):
            {plan}

            Conflict warnings detected by the system (may be empty):
            {conflicts}

            Retrieved care notes (use for grounding factual guidance):
            {context}

            What to produce:
            1) A short summary (3-5 sentences) explaining why this plan makes sense for the pets and the owner's time.
            2) Practical suggestions (1-3 bullets) to improve consistency or reduce stress, based only on the retrieved notes.
            3) If conflicts exist, provide a short "Warnings" section explaining the risk in plain language.

            Rules:
            - The schedule is already decided. Do NOT change task times or durations.
            - Use the retrieved care notes for any general pet-care guidance.
            - Do not invent medical facts, dosing instructions, or diagnoses.
            - If the retrieved notes are insufficient for a claim, say you are unsure based on available notes.
            - Keep the answer concise and friendly.

            Output format:
            Summary:
            ...

            Suggestions:
            - ...
            - ...

            Warnings:
            - ... (only if conflicts exist)
            """

        response = self.model.generate_content(prompt)
        return (response.text or "").strip()


def test_gemini_connection(prompt: str = "Say 'OK' if you can read this.") -> str:
    """
    Simple connectivity check. Returns the model's response text or raises.
    """
    client = GeminiClient()
    response = client.model.generate_content(prompt)
    return (response.text or "").strip()
