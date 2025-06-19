import json

def build_prompt_from_json(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data

def fill_chat_prompt(agent_name, agent_personality, partner_name, partner_personality, conversation_summary, context, scenario_description):
    prompt = f"""
    You are {agent_name}, a {agent_personality}.
    Your partner is {partner_name}, a {partner_personality}.
    Scenario: {scenario_description}
    Context: {context}
    Conversation so far: {conversation_summary}
    """
    return prompt.strip()
