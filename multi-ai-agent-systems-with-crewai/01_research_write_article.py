import os
import warnings
import re

from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task

warnings.filterwarnings('ignore')
load_dotenv()


class ResearchWriteArticle:

    def planner(self) -> Agent:
        return Agent(
            role="Content Planner",
            goal="Plan engaging and factually accurate content on {topic}",
            backstory="You're working on planning a blog article "
                      "about the topic: {topic}. "
                      "You collect information that helps the "
                      "audience learn something "
                      "and make informed decisions. "
                      "Your work is the basis for "
                      "the Content Writer to write an article on this topic.",
            allow_delegation=False,
            verbose=True
        )
    
    def writer(self) -> Agent:
        return Agent(
            role="Content Writer",
            goal="Write insightful and factually accurate "
                 "opinion piece about the topic: {topic}",
            backstory="You're working on a writing "
                      "a new opinion piece about the topic: {topic}. "
                      "You base your writing on the work of "
                      "the Content Planner, who provides an outline "
                      "and relevant context about the topic. "
                      "You follow the main objectives and "
                      "direction of the outline, "
                      "as provide by the Content Planner. "
                      "You also provide objective and impartial insights "
                      "and back them up with information "
                      "provide by the Content Planner. "
                      "You acknowledge in your opinion piece "
                      "when your statements are opinions "
                      "as opposed to objective statements.",
            allow_delegation=False,
            verbose=True
        )
    
    def editor(self) -> Agent:
        return Agent(
            role="Editor",
            goal="Edit a given blog post to align with "
                 "the writing style of the organization. ",
            backstory="You are an editor who receives a blog post "
                      "from the Content Writer. "
                      "Your goal is to review the blog post "
                      "to ensure that it follows journalistic best practices, "
                      "provides balanced viewpoints "
                      "when providing opinions or assertions, "
                      "and also avoids major controversial topics "
                      "or opinions when possible.",
            allow_delegation=False,
            verbose=True
        )  

    def plan(self) -> Task:
        return Task(
            description=(
                "1. Prioritize the latest trends, key players, "
                "and noteworthy news on {topic}.\n"
                "2. Identify the target audience, considering "
                "their interests and pain points.\n"
                "3. Develop a detailed content outline including "
                "an introduction, key points, and a call to action.\n"
                "4. Include SEO keywords and relevant data or sources."
            ),
            expected_output="A comprehensive content plan document "
                            "with an outline, audience analysis, "
                            "SEO keywords, and resources.",
            agent=self.planner()
        )
    
    def write(self) -> Task:
        return Task(
            description=(
                "1. Use the content plan to craft a compelling "
                "blog post on {topic}.\n"
                "2. Incorporate SEO keywords naturally.\n"
                "3. Sections/Subtitles are properly named "
                "in an engaging manner.\n"
                "4. Ensure the post is structured with an "
                "engaging introduction, insightful body, "
                "and a summarizing conclusion.\n"
                "5. Proofread for grammatical errors and "
                "alignment with the brand's voice.\n"
            ),
            expected_output="A well-written blog post "
                            "in markdown format, ready for publication, "
                            "each section should have 2 or 3 paragraphs.",
            agent=self.writer()
        )
    
    def edit(self) -> Task:
        return Task(
            description=("Proofread the given blog post for "
                         "grammatical errors and "
                         "alignment with the brand's voice."),
            expected_output="A well-written blog post in markdown format, "
                            "ready for publication, "
                            "each section should have 2 or 3 paragraphs and "
                            "should tranlate to {language}.",
            agent=self.editor()
        )  


    def crew(self) -> Crew:
        planner = self.planner()
        writer = self.writer()
        editor = self.editor()

        plan = self.plan()
        write = self.write()
        edit = self.edit()

        print(vars(planner))
        print(planner.llm)
        print(planner.llm.model)

        return Crew(
            agents=[planner, writer, editor],
            tasks=[plan, write, edit],
            process=Process.sequential,
            verbose=True
        )



if __name__ == "__main__":
    inputs = {
        "topic": "Best AI Toos to developers in 2025",
        "language": "Brazilian Portuguese"
    }
    result = ResearchWriteArticle().crew().kickoff(inputs)
    print(result)

    # --- Salvar resultado em arquivo markdown ---
    # Cria a pasta 'result' se não existir
    os.makedirs("result", exist_ok=True)

    # Sanitiza o nome do arquivo
    topic = inputs["topic"]
    topic_safe = re.sub(r'[^a-zA-Z0-9_\-]', '_', topic)[:50]

    # Descobre o modelo usado (exemplo usando o planner)
    planner = ResearchWriteArticle().planner()
    model_name = getattr(getattr(planner, "llm", None), "model", "unknown-model")

    filename = f"result/{topic_safe}__{model_name}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(result))

    print(f"\nArquivo salvo em: {filename}")