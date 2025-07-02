# KI-basierter KVT-Agent – Bachelorarbeit

Dieses Repository enthält den Prototyp eines KI-basierten Agenten, der im Rahmen meiner Bachelorarbeit an der Hochschule Pforzheim entwickelt wurde. Die Arbeit mit dem Titel **„Potenziale und Limitationen eines KI-basierten KVT-Agenten: Eine qualitative Analyse von Nutzerinteraktionen und -Feedback“** untersucht die Chancen und Herausforderungen meines KI-Agenten.

---

## Motivation

Gesundheitssysteme stoßen bei der Versorgung im Bereich der mentalen Gesundheit zunehmend an ihre Grenzen. Lange Wartezeiten auf Therapieplätze und die Angst vor Stigmatisierung stellen für viele Menschen eine große Hürde dar. Gleichzeitig suchen Personen, die sich bereits in kognitiver Verhaltenstherapie (KVT) befinden, nach Wegen, das Gelernte im Alltag umzusetzen.

## Ziel

Das Ziel der Arbeit war nicht die Entwicklung eines marktreifen Produkts, sondern die wissenschaftliche Analyse von realen Nutzererfahrungen. Im Fokus stand die Beantwortung der Forschungsfrage:

**„Welche Potenziale und Limitationen weist ein Prototyp eines KI-basierten KVT-Agenten bei der Unterstützung von Nutzern auf, basierend auf einer qualitativen Analyse von Nutzerinteraktionen und -Feedback?“**

Mithilfe einer qualitativen Untersuchung sollten die Perspektiven von Nutzern auf den Agenten herausgearbeitet werden, um Potenziale zu identifizieren und Limitationen aufzuzeigen.

## Kerntechnologien

Der Prototyp wurde mit folgenden Technologien und Frameworks umgesetzt:

* **Programmiersprache:** Python
* **KI-Agenten-Framework:** CrewAI, ein Open-Source-Framework zur Orchestrierung von Multi-Agenten-Systemen
* **Large Language Model (LLM):** Google Gemini (gemini-1.5-flash-8b), angebunden über die AI-Studio API
* **Wissensbasis (RAG):** Zur Anreicherung der Antworten wurde eine Retrieval-Augmented Generation (RAG) Architektur implementiert.
* **Vektordatenbank:** Eine lokale ChromaDB-Instanz dient zur Speicherung und Abfrage von Fachinformationen aus PDF-Dokumenten.
* **Zusätzliche Tools:** Die Agenten nutzen unter anderem das SerperDevTool für die Google-Suche und das ScrapeWebsiteTool zum Extrahieren von Webinhalten.


# GeminiAgents Crew

Welcome to the GeminiAgents Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the Gemini_Agents Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The Gemini_Agents Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the GeminiAgents Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
