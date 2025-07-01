import os
import re
from crewai import Crew, Process, Task
from dotenv import load_dotenv
load_dotenv()

from agent import (
    therapeutic_partner_agent,
    psychoeducation_assistant_agent,
    pdf_research_agent,
    solution_agent,
)
from task import (
    create_therapeutic_partner_task,
    create_psychoeducation_assistant_task,
    create_solution_agent_task,
    create_pdf_search_task,
    get_therapeutic_chat_task,
)

def sanitize_output(response):
    if isinstance(response, list):
        return "\n".join([str(entry) for entry in response])
    elif isinstance(response, dict) and "description" in response:
        return response["description"]
    return str(response).strip()

interactive_chat_crew = Crew(
    agents=[therapeutic_partner_agent],
    tasks=[],
    process=Process.sequential,
    verbose=False,
    embedder={
        "provider": "google",
        "config": {
            "model": os.getenv("MODEL")
        }
    }
)

full_mental_health_crew = Crew(
    agents=[
        therapeutic_partner_agent, psychoeducation_assistant_agent, pdf_research_agent,
        solution_agent
    ],
    tasks=[],
    process=Process.sequential,
    verbose=False,
    embedder={
        "provider": "google",
        "config": {
            "model": os.getenv("MODEL")
        }
    }
)


if __name__ == "__main__":
    print("\n**Willkommen zum AI-Therapie-Chat! Zum Beenden schreibe 'exit' oder 'bye' ...")
    chat_history = []
    last_user_input_for_search = ""  # Variable zum Speichern der letzten Eingabe

    # --- Interaktiver Chat Teil ---
    # interactive_chat_crew.tasks = [get_therapeutic_chat_task()] # Optional: Initiale Task?
    while True:
        user_input = input("Patient (User): ")

        # Speichere die Eingabe, BEVOR auf "exit" geprüft wird
        if user_input.lower() not in ["exit", "bye"]:
            last_user_input_for_search = user_input

        if user_input.lower() in ["exit", "bye"]:
            print("\n**Chat beendet.**")
            break

# Generiert von Gemini
        dynamic_task = Task(
            # ... (Task Definition für interaktiven Chat) ...
            description=f"Patienteneingabe: '{user_input}'. Generiere eine therapeutische Antwort.",
            expected_output="stelle nur **eine einzige offene Rückfrage**, "
            "die sich auf den wichtigsten Aspekt der Patienteneingabe konzentriert. "
            "Stelle nicht mehrere Fragen auf einmal. Keine Aufzählungen. Keine Themenwechsel.",
            agent=therapeutic_partner_agent
        )
        # ... (Rest der interaktiven Schleife: kickoff, sanitize, print, append to history) ...
        interactive_chat_crew.tasks = [dynamic_task]
        agent_response = interactive_chat_crew.kickoff()
        cleaned_response = sanitize_output(agent_response)

        print(f"\nAI-Therapeut: {cleaned_response}\n")
        chat_history.append(f"Patient: {user_input}")
        chat_history.append(f"AI-Therapeut: {cleaned_response}")

    # --- Multi-Agenten Follow-up Teil (NACH der Schleife) ---
    print("\n**Starte Multi-Agenten-Follow-up...**")
    print(f"Gesammelter Chat-Verlauf: {chat_history}")

    # Setze die Suchanfrage auf die letzte Benutzereingabe
    # Füge eine Prüfung hinzu, falls der Chat sofort beendet wurde
    search_query = last_user_input_for_search
    if not search_query:
        print(
            "Warnung: Keine Benutzereingabe für die Suche vorhanden. Breche Follow-up ggf. ab oder nutze Standard-Query.")
        search_query = "Allgemeine Gesundheitsinformationen"  # Beispiel für Fallback

    # Debug Prints anpassen
    print(f"\n--- Verwende letzte Benutzereingabe als Query für PDF Search Task: '{search_query}' ---")

    # Erstelle die Follow-up Tasks mit der KORREKTEN search_query
    follow_up_tasks = [
        create_therapeutic_partner_task(chat_history),
        create_psychoeducation_assistant_task(chat_history),
        create_pdf_search_task(chat_history, search_query),  # Hier die Variable übergeben
        create_solution_agent_task(chat_history),
    ]
    full_mental_health_crew.tasks = follow_up_tasks

    # Starte den Follow-up Crew
    follow_up_results = full_mental_health_crew.kickoff()
    cleaned_results = sanitize_output(follow_up_results)

    print("\n**Multi-Agenten-Follow-up - Ergebnisse:**\n")
    print(cleaned_results)
    print("\n**Follow-up abgeschlossen.**\n")
