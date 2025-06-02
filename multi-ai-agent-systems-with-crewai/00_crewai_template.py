import os
import re
import warnings

from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task

warnings.filterwarnings('ignore')
load_dotenv()


class CrewAiTemplate:

    def agent(self) -> Agent:
        return Agent(
            role="",
            goal="",
            backstory="",
            allow_delegation=False,
            verbose=True
        )
    
   
    def task(self) -> Task:
        return Task(
            description=(
                ""
            ),
            expected_output="",
            agent=self.planner()
        )
    
   

    def crew(self) -> Crew:
        agent = self.agent()
   
        task = self.tast()
   
        return Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )



if __name__ == "__main__":
    inputs = {
        "topic": "",
    }
    result = CrewAiTemplate().crew().kickoff(inputs)
    print(result)

    # --- Salvar resultado em arquivo markdown ---
    # Cria a pasta 'result' se não existir
    os.makedirs("result", exist_ok=True)

    # Sanitiza o nome do arquivo
    topic = inputs["topic"]
    topic_safe = re.sub(r'[^a-zA-Z0-9_\-]', '_', topic)[:50]

    # Descobre o modelo usado (exemplo usando o planner)
    model_name = os.getenv("OPENAI_MODEL_NAME", "unknown-model")

    filename = f"result/{topic_safe}__{model_name}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(result))

    print(f"\nArquivo salvo em: {filename}")