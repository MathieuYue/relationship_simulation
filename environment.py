from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
import json
import os
from dotenv import load_dotenv
load_dotenv()

LAMBDA_API_KEY = os.getenv("LAMBDA_API_KEY")

llm = ChatOpenAI(
            model="qwen3-32b",
            openai_api_key=LAMBDA_API_KEY,
            openai_api_base="https://api.lambda.ai/v1"
        )

def next_scene(chapter: int, name1: str, name2: str, summary1: str, summary2: str):
    with open('scenarios/vacation.json', 'r') as f:
        vacation_data = json.load(f)
    system_prompt = f"""/no_think
    You are a creative writing assistant. Your task is to:
    1. Select a scene idea from the provided list given the provided summary of the prior conversation. If the summaries are empty, just pick a random scene.
    2. Rewrite the scene to incorporate {name1} and {name2} as the main characters
    3. Keep the core conflict or situation intact
    4. Add specific details that make the scene feel personal to these characters
    5. The scene should be 100 words or less
    6. Don't include any conversation between the characters, just the scene
    
    SCENE SUMMARY FOR {name1} - {summary1}

    SCENE SUMMARY FOR {name2} - {summary2}

    Here are the scene ideas to choose from:
    {json.dumps(vacation_data[str(chapter)], indent=2)}
    
    State what scene idea was chosen. Please provide your rewritten scene in a clear, narrative format."""
    response = llm.invoke(system_prompt)
    return response.content
    
