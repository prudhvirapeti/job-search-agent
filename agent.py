"""
Job Search Agent
----------------
Give it a job title → finds required skills → gaps in your profile → what to learn next.

Run:
    python agent.py "AI Engineer"
    python agent.py "Data Engineer"
"""

import sys
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ── Knowledge base (tools) ────────────────────────────────────────────────────

SKILLS_DB = {
    "ai engineer": [
        "Python", "LangChain", "RAG pipelines", "LLM APIs (OpenAI/Anthropic)",
        "Vector databases (ChromaDB/Pinecone)", "FastAPI", "Docker",
        "Prompt engineering", "LangGraph", "MLOps basics"
    ],
    "data engineer": [
        "Python", "SQL", "Apache Spark", "Airflow", "dbt",
        "AWS/GCP/Azure", "Kafka", "Data modeling", "ETL pipelines", "Docker"
    ],
    "data analyst": [
        "SQL", "Python", "Tableau or Power BI", "Excel",
        "Statistics", "Data cleaning", "Pandas", "Communication"
    ],
}

MY_SKILLS = [
    "Python", "SQL", "LangChain", "FastAPI", "ChromaDB",
    "RAG pipelines", "Prompt engineering", "Power BI",
    "LLM APIs (OpenAI/Anthropic)", "Git"
]

RESOURCES = {
    "LangGraph":              "LangGraph docs quickstart → https://langchain-ai.github.io/langgraph/",
    "Docker":                 "freeCodeCamp Docker course (free, 4hrs) on YouTube",
    "Apache Spark":           "PySpark for Beginners on DataCamp free tier",
    "Airflow":                "Astronomer free tutorials → https://astronomer.io/learn",
    "dbt":                    "dbt Learn (free, official) → https://courses.getdbt.com",
    "MLOps basics":           "Made With ML → https://madewithml.com (free, project-based)",
    "AWS/GCP/Azure":          "Google Cloud Skills Boost free tier or AWS free tier + their free courses",
    "Kafka":                  "Confluent free Kafka course → https://developer.confluent.io/courses",
    "Data modeling":          "'Learning SQL' by Alan Beaulieu (free on O'Reilly with library card)",
    "ETL pipelines":          "Practical guide on DataTalks.Club free Data Engineering Zoomcamp",
    "Statistics":             "StatQuest with Josh Starmer on YouTube — free and beginner-friendly",
    "Tableau or Power BI":    "Microsoft Power BI free learning path → https://learn.microsoft.com",
}


def get_required_skills(job_title: str) -> list[str]:
    for role, skills in SKILLS_DB.items():
        if role in job_title.lower():
            return skills
    return []


def get_skill_gaps(required: list[str]) -> list[str]:
    my = set(MY_SKILLS)
    return [s for s in required if s not in my]


def get_resource(skill: str) -> str:
    return RESOURCES.get(skill, f"Search 'learn {skill} free 2026' on YouTube")


# ── LLM ───────────────────────────────────────────────────────────────────────

llm = ChatOllama(model="llama3.2")


# ── Agent steps ───────────────────────────────────────────────────────────────

def run_agent(job_title: str):
    print(f"\nJob Search Agent — '{job_title}'")
    print("=" * 60)

    # Step 1 — Get required skills
    print("\n[Step 1] Looking up required skills...")
    required = get_required_skills(job_title)
    if not required:
        print(f"No data for '{job_title}'. Try: AI Engineer, Data Engineer, Data Analyst.")
        return
    print(f"Found {len(required)} required skills.")

    # Step 2 — Find gaps
    print("\n[Step 2] Comparing with your current skills...")
    gaps = get_skill_gaps(required)
    if not gaps:
        print("You already have all required skills!")
        return
    print(f"Found {len(gaps)} skill gaps: {', '.join(gaps)}")

    # Step 3 — Get resources for each gap
    print("\n[Step 3] Finding best learning resources...")
    gap_resources = {gap: get_resource(gap) for gap in gaps}

    # Step 4 — Ask LLM to create an actionable learning plan
    print("\n[Step 4] Generating your personalized learning plan...\n")

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a career coach for AI and data engineering roles. "
         "Give clear, motivating, actionable advice. Be concise."),
        ("human",
         "I want to become a {job_title}.\n\n"
         "Required skills for this role:\n{required}\n\n"
         "Skills I already have:\n{my_skills}\n\n"
         "My skill gaps and the best resources to fill them:\n{gaps_with_resources}\n\n"
         "Please give me:\n"
         "1. A brief assessment of how close I am to this role\n"
         "2. A prioritized 30-day learning plan covering the gaps\n"
         "3. One motivating sentence to keep me going")
    ])

    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({
        "job_title": job_title,
        "required": "\n".join(f"- {s}" for s in required),
        "my_skills": "\n".join(f"- {s}" for s in MY_SKILLS),
        "gaps_with_resources": "\n".join(
            f"- {gap}: {res}" for gap, res in gap_resources.items()
        )
    })

    print(result)
    print("\n" + "=" * 60)
    print("Skill gaps summary:")
    for gap, res in gap_resources.items():
        print(f"  • {gap}: {res}")


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    job_title = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "AI Engineer"
    run_agent(job_title)
