def fill_chat_prompt(agent_name: str, agent_personality: str, partner_name: str, 
                       partner_personality: str, conversation_summary: str, context: str,
                       scenario_description: str) -> str:
    """
    Fill in the chat prompt template with the provided parameters.
    
    Args:
        agent_name: Name of the agent
        agent_personality: Personality description of the agent
        partner_name: Name of the partner
        partner_personality: Personality description of the partner
        conversation_summary: Summary of past conversation
        scenario_description: Description of current scenario
        
    Returns:
        str: Filled prompt template
    """
    with open('chat_prompt_v1.txt', 'r') as f:
        prompt_template = f.read()
    
    # The template uses Jinja-style {{var}} placeholders, not .format() style.
    # Replace the placeholders manually.
    prompt_filled = prompt_template
    prompt_filled = prompt_filled.replace("{{agent_name}}", agent_name)
    prompt_filled = prompt_filled.replace("{{agent_personality}}", agent_personality)
    prompt_filled = prompt_filled.replace("{{partner_name}}", partner_name)
    prompt_filled = prompt_filled.replace("{{partner_personality}}", partner_personality)
    prompt_filled = prompt_filled.replace("{{conversation_summary}}", conversation_summary)
    prompt_filled = prompt_filled.replace("{{scenario_description}}", scenario_description)
    prompt_filled = prompt_filled.replace("{{conversation_history}}", context)
    return prompt_filled

import json
import os

def build_prompt_from_json(agent_json_path: str, partner_json_path: str, 
                           conversation_summary: str, context: str, scenario_description: str) -> str:
    """
    Build a chat prompt by loading agent and partner data from JSON files.

    Args:
        agent_json_path: Path to the agent's JSON file (e.g., sample_agents/blake_lively/basics.json)
        partner_json_path: Path to the partner's JSON file
        conversation_summary: Summary of past conversation
        context: Conversation history/context
        scenario_description: Description of the current scenario

    Returns:
        str: Filled chat prompt
    """
    # Load agent data
    with open(agent_json_path, 'r') as f:
        agent_data = json.load(f)
    # Load partner data
    with open(partner_json_path, 'r') as f:
        partner_data = json.load(f)

    # Compose names
    agent_name = f"{agent_data.get('first_name', '')} {agent_data.get('last_name', '')}".strip()
    partner_name = f"{partner_data.get('first_name', '')} {partner_data.get('last_name', '')}".strip()

    # Compose personalities (fallback to occupation/nationality/age if no explicit personality field)
    agent_personality = agent_data.get('personality', 
        f"{agent_data.get('age', '')} year old {agent_data.get('nationality', '')} {agent_data.get('occupation', '')}".strip())
    partner_personality = partner_data.get('personality', 
        f"{partner_data.get('age', '')} year old {partner_data.get('nationality', '')} {partner_data.get('occupation', '')}".strip())

    # Call the prompt filler
    prompt = fill_chat_prompt(
        agent_name=agent_name,
        agent_personality=agent_personality,
        partner_name=partner_name,
        partner_personality=partner_personality,
        conversation_summary=conversation_summary,
        context=context,
        scenario_description=scenario_description
    )
    return prompt
