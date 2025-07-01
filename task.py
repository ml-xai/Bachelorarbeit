from crewai import Task
#from tools import pdf_search_tool
from agent import (
    therapeutic_partner_agent,
    psychoeducation_assistant_agent,
    pdf_research_agent,
    solution_agent,
)
from tools import PDFSearchTool
import json

from crewai import Task
from crewai_tools import FileReadTool


def get_therapeutic_chat_task():
    return Task(
        description="Führe ein therapeutisches Gespräch mit dem Patienten.",
        expected_output="Antworte therapeutisch auf den Userinput. Versuche Lösungsorientiert zu denken. Nutze Psychologische Konzepte.",
        agent=therapeutic_partner_agent
    )


def create_therapeutic_partner_task(chat_history):
    return Task(
        description=f"Basierend auf dem vorherigen therapeutischen Chat-Verlauf: '{chat_history}'. Fasse das Gespräch kurz zusammen und gib abschließende Worte.",
        expected_output="Eine kurze Zusammenfassung des therapeutischen Gesprächs, einschließlich der wichtigsten besprochenen Themen, der emotionalen Zustände des Patienten und der vereinbarten nächsten Schritte. Abschließende, einfühlsame Worte, die den Patienten unterstützen und ermutigen.",
        agent=therapeutic_partner_agent
    )


def create_psychoeducation_assistant_task(chat_history):
    return Task(
        description=f"Basierend auf dem vorherigen therapeutischen Chat-Verlauf: '{chat_history}'. Gib dem Patienten *Psychoedukation* zum Thema Stressbewältigung, angepasst an den Chat-Verlauf.",
        expected_output="Psychoedukative Informationen zum Thema Stressbewältigung, angepasst an den vorherigen Chat-Verlauf. Erkläre die Grundlagen von Stress, wie er sich auf Körper und Geist auswirkt, und stelle evidenzbasierte Strategien zur Stressbewältigung vor, wie z. B. Achtsamkeit, Entspannungstechniken und kognitive Umstrukturierung.",
        agent=psychoeducation_assistant_agent
    )


from crewai import Task
from agent import pdf_research_agent

def create_pdf_search_task(chat_history, search_query):
    return Task(
        description=f"Führe eine Suche in der ChromaDB Wissensdatenbank durch. Konzentriere dich auf Informationen bezüglich dieser Anfrage: '{search_query}'. Nutze dein 'ChromaDB PDF Search' Tool dafür.",
        agent=pdf_research_agent,
        expected_output="Relevante Informationen aus den PDF-Dokumenten, die die Suchanfrage beantworten." # Hinzugefügt
    )

def create_solution_agent_task(chat_history):
    return Task(
        description=f"Basierend auf dem vorherigen therapeutischen Chat-Verlauf: '{chat_history}'. Analysiere die emotionale Lage des 'Patienten' und biete eine Lösungsorientierte Methode an. Biete zusätzlich eine weitere Methode an, die dem Patienten helfen kann. Es muss nicht gleich zu einem Ergebnis kommen.",
        expected_output="Eine Einschätzung der emotionalen Lage des 'Patienten' basierend auf dem Chat-Verlauf. Eine Lösungsorientierte Methode, die dem Patienten helfen kann, mit seinen Problemen umzugehen. Eine weitere Methode, die dem Patienten helfen kann. Die Methoden sollen auf die spezifischen Bedürfnisse und Herausforderungen des 'Patienten' im Chat-Verlauf abgestimmt sein.",
        agent=solution_agent
    )

