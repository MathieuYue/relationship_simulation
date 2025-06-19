from dotenv import load_dotenv
from relationship_agent import RelationshipAgent
import uuid
from environment import next_scene
from parser_utils import cleaned_response
load_dotenv()
import os

# Set Lambda API key from environment variable
LAMBDA_API_KEY = os.getenv("LAMBDA_API_KEY")

from prompt_utils import fill_chat_prompt,build_prompt_from_json
# Create prompts for both agents
# Initialize both agents
agent1 = RelationshipAgent(
    agent_json_path="sample_agents/blake_lively/basics.json",
    partner_json_path="sample_agents/ryan_reynolds/basics.json",
    temperature=0.7
)

agent2 = RelationshipAgent(
    agent_json_path="sample_agents/ryan_reynolds/basics.json",
    partner_json_path="sample_agents/blake_lively/basics.json",
    temperature=0.7
)

def main():
    import json
    
    # Load vacation.json
    with open('scenarios/vacation.json', 'r') as f:
        scene_data = json.load(f)
    
    total_scenes = scene_data['length']
    agent1_summary = ""
    agent2_summary = ""

    
    print("Welcome to the Relationship Agent Chat!")
    for scene in range(total_scenes):
        curr_scenario = cleaned_response(next_scene(scene, "Blake", "Ryan", agent1_summary, agent2_summary))
        print(f"\033[93m{curr_scenario}\033[0m")
        agent1.update_chat_prompt(curr_scenario, "", "")
        agent2.update_chat_prompt(curr_scenario, "", "")
        num_turns = int(input("How many conversation turns would you like to simulate? "))
        thread_id = uuid.uuid4()
        config = {"configurable": {"thread_id": thread_id}}
        # Initialize conversation
        # generate first input
        current_input = cleaned_response(agent1.generate_conversation_starter({'configurable': {"thread_id": 0}}))
        print(f"\033[95mBlake: {current_input}\033[0m")
        
        for turn in range(num_turns):
            try:
                # Agent 2 (Ryan) responds
                response = cleaned_response(agent2.run(current_input, config, num_turns - turn))
                print(f"\033[94mRyan: {response}\033[0m")
                
                # Agent 1 (Blake) responds
                current_input = cleaned_response(agent1.run(response, config, num_turns - turn))
                print(f"\033[95mBlake: {current_input}\033[0m")
                
            except Exception as e:
                print(f"\nError: {str(e)}")
                break
        
        print("\nScene complete!")
        agent1_summary = cleaned_response(agent1.summarize_conversation(config))
        agent2_summary = cleaned_response(agent2.summarize_conversation(config))
        print(f"\033[95mBlake Summary: {agent1_summary}\033[0m")
        print(f"\033[94mRyan Summary: {agent2_summary}\033[0m")

if __name__ == "__main__":
    main()
