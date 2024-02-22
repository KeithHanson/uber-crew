# uber-crew
WIP: A crew.ai that is primarily developed with LMStudio or Ollama in mind. This docker stack provides the CrewAI code for running a selenium browser to not just pull information but click buttons and interact with the web. 

## Getting Started

1. Install Docker or Docker Desktop for your platform
2. Run LM Studio or Ollama 
3. Open a terminal
4. Run `git clone https://github.com/KeithHanson/uber-crew.git` and `cd uber-crew`
5. Copy the .env.example file to .env: `cp .env.example .env` (this allows you to customize how to connect to your LLM)
6. Set the three environment variables to your configuration so the agent knows how to talk to your local LLM (see the comments in the example)
7. Run `docker compose up` 

## Notes

Currently, this docker compose script starts up a Selenium Standalone grid. In the future, this will be used for browsing the web. 

At the moment, this is a sample script to test the integration of a local LLM with a dockerized CrewAI python script. 
