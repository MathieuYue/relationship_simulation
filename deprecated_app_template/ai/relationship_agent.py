from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain.tools import Tool
from ..utils.prompt_utils import build_prompt_from_json, fill_chat_prompt
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from ..utils.json_utils import read_json_file

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set Lambda API key from environment variable
LAMBDA_API_KEY = os.getenv("LAMBDA_API_KEY")

class RelationshipAgent:
    def __init__(
        self,
        agent_json_path,
        partner_json_path,
        scenario_description = '',
        conversation_summary = '',
        context = '',
        temperature: float = 0.7
    ):
        # Initialize the LLM
        self.llm = ChatOpenAI(
            model="qwen3-32b",
            openai_api_key=LAMBDA_API_KEY,
            openai_api_base="https://api.lambda.ai/v1",
            temperature=temperature
        )

        self.persona = read_json_file(agent_json_path)
        self.partner_persona = read_json_file(partner_json_path)
        
        system_prompt = fill_chat_prompt(
            agent_name=self.persona['first_name'],
            agent_personality=self.persona['personality'],
            partner_name=self.partner_persona['first_name'],
            partner_personality=self.partner_persona['personality'],
            conversation_summary=conversation_summary,
            context=context,
            scenario_description=scenario_description
        )
        
        # Create system message
        self.system_message = SystemMessage(content=system_prompt)
        
        # Initialize tools (empty for now, can be extended)
        self.tools = []
        
        # Initialize memory saver
        self.memory = MemorySaver()
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_message.content),
            MessagesPlaceholder(variable_name="messages"),
            ("system", "You have {remaining_steps} steps remaining. This is {is_last_step} the last step.")
        ])
        
        # Create the agent
        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=self.prompt,
            checkpointer=self.memory
        )
    
    def run(self, user_input: str, config: dict, remaining_steps: int) -> str:
        """Run the agent with the given user input."""
        # Initialize the state
        state = {
            "messages": [{"role": "user", "content": user_input}],
            "is_last_step": "not",
            "remaining_steps": remaining_steps
        }
        
        # Run the agent with streaming
        result = ""
        for step in self.agent.stream(state, config, stream_mode="values"):
            if "messages" in step and step["messages"]:
                result = step["messages"][-1].content
        return result
    
    def summarize_conversation(self, config: dict) -> str:
        """
        Generate a summary of the current conversation, including emotional context and key points.
        
        Returns:
            str: A summary of the conversation with emotional analysis
        """
        summary_prompt = f"""/no_think
            Please analyze the conversation from the POV of {self.persona['first_name']} {self.persona['last_name']} and provide a JSON-formatted summary with the following structure:
            {{
                "key_points": ["List of main topics discussed"],
                "emotional_tone": {{
                    "overall_sentiment": "positive/negative/neutral",
                    "mood_changes": ["List of notable mood shifts"],
                    "tension_points": ["List of potential conflicts"]
                }},
                "decisions": ["List of important decisions or agreements made"]
            }}
            Keep the summary concise and focused on the most important elements."""
        
        # Initialize the state
        state = {
            "messages": [{"role": "system", "content": summary_prompt}],
            "is_last_step": "is",
            "remaining_steps": 1
        }
        
        try:
            # Run the agent with streaming
            result = ""
            for step in self.agent.stream(state, config, stream_mode="values"):
                if "messages" in step and step["messages"]:
                    result = step["messages"][-1].content
            return result
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def update_chat_prompt(self, new_scenario_description: str, new_context: str, new_conversation_summary: str) -> None:
        """
        Update the chat prompt with new scenario description and context.
        
        Args:
            new_scenario_description (str): New scenario description to set
            new_context (str): New context to set
        """
        self.scenario_description = new_scenario_description
        self.context = new_context
        self.conversation_summary = new_conversation_summary
        
        # Rebuild the chat prompt with updated values
        self.chat_prompt = fill_chat_prompt(
            agent_name=f"{self.persona['first_name']} {self.persona['last_name']}",
            agent_personality=self.persona['personality'],
            partner_name=f"{self.partner_persona['first_name']} {self.partner_persona['last_name']}",
            partner_personality=self.partner_persona['personality'],
            conversation_summary=self.conversation_summary,
            context=self.context,
            scenario_description=self.scenario_description
        )

        self.system_message = SystemMessage(content=self.chat_prompt)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_message.content),
            MessagesPlaceholder(variable_name="messages"),
            ("system", "You have {remaining_steps} steps remaining. This is {is_last_step} the last step.")
        ])

        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=self.prompt,
            checkpointer=self.memory
        )

    def generate_conversation_starter(self, config: dict = None) -> str:
        """
        Generate a conversation starter based on the current scenario.
        
        Args:
            config (dict): Configuration dictionary for the agent
            
        Returns:
            str: A conversation starter message
        """
        conversation_starter_prompt = f"""You are {self.persona['first_name']} {self.persona['last_name']}, a {self.persona['personality']}.
        
        Current scenario: {self.scenario_description}
        
        Based on this scenario, generate a natural conversation starter that {self.persona['first_name']} would say to {self.partner_persona['first_name']}. 
        The starter should be:
        - Authentic to {self.persona['first_name']}'s personality
        - Relevant to the current scenario
        - Engaging and natural
        - 1-2 sentences maximum
        
        Generate the conversation starter:"""
        
        # Initialize the state
        state = {
            "messages": [{"role": "system", "content": conversation_starter_prompt}],
            "is_last_step": "is",
            "remaining_steps": 1
        }
        
        try:
            # Run the agent with streaming
            result = ""
            for step in self.agent.stream(state, config or {}, stream_mode="values"):
                if "messages" in step and step["messages"]:
                    result = step["messages"][-1].content
            return result
        except Exception as e:
            return f"Error generating starter: {str(e)}"