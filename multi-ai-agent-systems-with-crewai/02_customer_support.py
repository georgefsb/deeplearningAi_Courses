import os
import re
import warnings

from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool
from IPython.display import Markdown

warnings.filterwarnings('ignore')
load_dotenv()

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
docs_scrape_tool = ScrapeWebsiteTool(
    website_url="https://docs.crewai.com/guides/agents/crafting-effective-agents"
)


class CustomerSuport:

    def support_agent(self) -> Agent:
        return Agent(
            role="Senior Support Representative",
            goal="Be the most friendly and helpful support representative in your team",
            backstory=("""
                You work at crewAI (https://crewai.com) and
                are now working on providing
                support to {customer}, a super important customer
                for your company.
                You need to make sure that you provide the best support!
                Make sure to provide full complete answers, 
                and make no assumptions.
            """),
            allow_delegation=False,
            verbose=True
        )
    
    def support_quality_assurance_agent(self) -> Agent:
        return Agent(
            role="Support Quality Assurance Specialist",
            goal="Get recognition for providing the best support quality assurance in your team",
            backstory=("""
                You work at crewAI (https://crewai.com) and are now working with your team
                on a request from {customer} ensuring that the support representative is
                providing the best support possible.
                You need to make sure that the support representative is providing full
                complete answers, and make no assumptions.
            """),
            verbose=True
        )
    
   
    def inquiry_resolution(self) -> Task:
        return Task(
            description=(
                "{customer} just reached out with a super important ask:\n"
                "{inquiry}\n\n"
                "{person} from {customer} is the one that reached out. "
                "Make sure to use everything you know "
                "to provide the best support possible."
                "You must strive to provide a complete "
                "and accurate response to the customer's inquiry."
            ),
            expected_output=(
                "A detailed, informative response to the "
                "customer's inquiry that addresses "
                "all aspects of their question.\n"
                "The response should include references "
                "to everything you used to find the answer, "
                "including external data or solutions. "
                "Ensure the answer is complete, "
                "leaving no questions unanswered, and maintain a helpful and friendly "
                "tone throughout."
            ),
            tools=[docs_scrape_tool],
            agent=self.support_agent(),
        )

    def quality_assurance_review(self) -> Task:
        return Task(
            description=(
                "Review the response drafted by the Senior Support Representative for {customer}'s inquiry. "
                "Ensure that the answer is comprehensive, accurate, and adheres to the "
                "high-quality standards expected for customer support.\n"
                "Verify that all parts of the customer's inquiry "
                "have been addressed "
                "thoroughly, with a helpful and friendly tone.\n"
                "Check for references and sources used to "
                " find the information, "
                "ensuring the response is well-supported and "
                "leaves no questions unanswered."
            ),
            expected_output=(
                "A final, detailed, and informative response "
                "ready to be sent to the customer.\n"
                "This response should fully address the "
                "customer's inquiry, incorporating all "
                "relevant feedback and improvements.\n"
                "Don't be too formal, we are a chill and cool company "
                "but maintain a professional and friendly tone throughout."
            ),
            agent=self.support_quality_assurance_agent(),
        )
    
   

    def crew(self) -> Crew:
        return Crew(
            agents=[self.support_agent(), self.support_quality_assurance_agent()],
            tasks=[self.inquiry_resolution(), self.quality_assurance_review()],
            #process=Process.sequential,
            verbose=True,
            memory=True
        )
    



if __name__ == "__main__":
    inputs = {
        "customer": "DeepLearningAI_Agent01",
        "person": "Andrew Ng",
        "inquiry": """I need help with setting up a Crew 
                and kicking it off, specifically
                how can I create a efficient agent in crew?
                Can you provide guidance with steps and a template?"""
    }
    result = CustomerSuport().crew().kickoff(inputs)
    print(result)


    # --- Salvar resultado em arquivo markdown ---
    # Cria a pasta 'result' se não existir
    os.makedirs("result", exist_ok=True)

    # Sanitiza o nome do arquivo
    topic = inputs["customer"]
    topic_safe = re.sub(r'[^a-zA-Z0-9_\-]', '_', topic)[:50]

    # Descobre o modelo usado (exemplo usando o planner)
    model_name = os.getenv("OPENAI_MODEL_NAME", "unknown-model")

    filename = f"result/{topic_safe}__{model_name}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(result))

    print(f"\nArquivo salvo em: {filename}")