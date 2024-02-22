import os
from crewai import Agent, Task, Crew, Process
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from duckduckgo_search import DDGS

os.environ["OPENAI_API_BASE"] = os.environ["OPENAI_API_BASE"] if "OPENAI_API_BASE" in os.environ else 'http://localhost:11434/v1'
os.environ["OPENAI_MODEL"] = os.environ["OPENAI_MODEL"] if "OPENAI_MODEL" in os.environ else "eas/nous-hermes-2-solar-10.7b"
os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"] if "OPENAI_API_KEY" in os.environ else 'IGNORED'

llm=ChatOpenAI(base_url=os.environ["OPENAI_API_BASE"], api_key=os.environ["OPENAI_API_KEY"], model=os.environ["OPENAI_MODEL"])

class DDGTools():

    # Anotate the fuction with the tool decorator from LangChain
    @tool("InternetSearch")
    def internet_search(query):
        '''Execute a Duck Duck go search to find articles, websites, and content on the internet. 
        Receives a query to search on, and returns the top 5 results as dictionaries. 
        The results will provide title, href, and the body of the search result text. "
        '''
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=5)]
            print(results)
        return results

# Define your agents with roles and goals
researcher = Agent(
  role='Senior Research Analyst',
  goal='Uncover cutting-edge developments in AI and data science',
  backstory="""You work at a leading tech think tank.
  Your expertise lies in identifying emerging trends.
  You have a knack for dissecting complex data and presenting actionable insights.
  These keywords must never be translated and transformed:
  - Action:
  - Thought:
  - Action Input:
  - Final Answer:
  because they are part of the thinking process instead of the output.
  """,
  verbose=True,
  allow_delegation=False,
  tools=[DDGTools().internet_search],
  llm=llm
  # You can pass an optional llm attribute specifying what mode you wanna use.
  # It can be a local model through Ollama / LM Studio or a remote
  # model like OpenAI, Mistral, Antrophic or others (https://python.langchain.com/docs/integrations/llms/)
  #
  # Examples:
  #
  # from langchain_community.llms import Ollama
  # llm=ollama_llm # was defined above in the file
  #
  # from langchain_openai import ChatOpenAI
  # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
)

# Create tasks for your agents
task1 = Task(
  description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
  Identify key trends, breakthrough technologies, and potential industry impacts.
  Your final answer MUST be short 100 word article summarizing the findings.""",
  agent=researcher
)

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[researcher],
  tasks=[task1],
  verbose=True, # You can set it to 1 or 2 to different logging levels
  process=Process.hierarchical,
  manager_llm=llm
)

result = crew.kickoff()
print("######################")
print(result)
