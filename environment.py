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
    

class EnvironmentAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="qwen3-32b",
            openai_api_key=LAMBDA_API_KEY,
            openai_api_base="https://api.lambda.ai/v1"
        )
        self.world_state = self._init_world()
        
        # Define tools
        self.tools = [
            Tool(
                name="generate_environmental_cues",
                func=self._generate_cues,
                description="Generate location-based sensory details"
            ),
            Tool(
                name="update_world_state",
                func=self._update_world,
                description="Modify global world parameters"
            )
        ]
        
        # Agent executor
        self.agent = AgentExecutor.from_agent_and_tools(
            agent=self._create_agent(),
            tools=self.tools,
            memory=self.npc_memory,
            verbose=True
        )
    
    def _create_agent(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are a World Simulator for relationship dynamics. Your tasks:
            1. Generate environmental context
            2. Manage NPC interactions
            3. Track world state changes
            
            Current World Properties:
            - Locations: {locations}
            - Active NPCs: {npcs}
            - Time: {time}
            """),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ])
        
        return {
            "input": lambda x: x["input"],
            "chat_history": lambda x: x["chat_history"],
            "agent_scratchpad": lambda x: x["agent_scratchpad"],
            "locations": lambda _: str(self.world_state["locations"]),
            "npcs": lambda _: str(self.world_state["npcs"]),
            "time": lambda _: str(self.world_state["time"])
        } | prompt | self.llm

    def _init_world(self):
        return {
            "locations": {
                "home": {"privacy": 0.9, "triggers": ["wedding_photo"]},
                "cafe": {"privacy": 0.4, "triggers": ["jazz_music"]}
            },
            "npcs": {
                "ex_partner": {"influence": 0.3, "last_seen": -1},
                "therapist": {"influence": 0.8, "availability": 0.5}
            },
            "time": {
                "hour": 14,
                "day_type": "weekend"
            }
        }

    @tool
    def _generate_cues(self, location: str) -> dict:
        """Generate sensory details for a location"""
        prompt = f"""
        Generate 3 environmental cues for {location} considering:
        - Privacy: {self.world_state['locations'][location]['privacy']}
        - Current time: {self.world_state['time']['hour']}:00
        - Common triggers: {self.world_state['locations'][location]['triggers']}
        
        Respond with JSON:
        {{
            "visual": "...",
            "auditory": "...",
            "olfactory": "...",
            "emotional_impact": 0-10
        }}
        """
        return self.llm.invoke(prompt)