from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from relationship_agent import RelationshipAgent
import uuid
from environment import next_scene
from parser_utils import cleaned_response
from dotenv import load_dotenv
import os
import json
import glob

load_dotenv()

app = Flask(__name__)
CORS(app)

# Set Lambda API key from environment variable
LAMBDA_API_KEY = os.getenv("LAMBDA_API_KEY")

def get_available_agents():
    """Get all available agents from sample_agents directory"""
    agents = []
    agent_dirs = glob.glob("sample_agents/*/")
    
    for agent_dir in agent_dirs:
        agent_name = os.path.basename(os.path.dirname(agent_dir))
        basics_path = os.path.join(agent_dir, "basics.json")
        
        if os.path.exists(basics_path):
            try:
                with open(basics_path, 'r') as f:
                    agent_data = json.load(f)
                    agents.append({
                        "id": agent_name,
                        "name": f"{agent_data.get('first_name', '')} {agent_data.get('last_name', '')}".strip(),
                        "personality": agent_data.get('personality', ''),
                        "path": basics_path
                    })
            except Exception as e:
                print(f"Error loading agent {agent_name}: {e}")
    
    return agents

@app.route('/')
def index():
    """Main page with agent selection"""
    agents = get_available_agents()
    return render_template('index.html', agents=agents)

@app.route('/api/agents', methods=['GET'])
def get_agents():
    """Get available agents"""
    agents = get_available_agents()
    return jsonify(agents)

@app.route('/api/start-conversation', methods=['POST'])
def start_conversation():
    """Start a new conversation between two agents"""
    data = request.json
    agent1_id = data.get('agent1_id')
    agent2_id = data.get('agent2_id')
    temperature = data.get('temperature', 0.7)
    
    if not agent1_id or not agent2_id:
        return jsonify({"error": "Both agents must be selected"}), 400
    
    agents = get_available_agents()
    agent1_data = next((a for a in agents if a['id'] == agent1_id), None)
    agent2_data = next((a for a in agents if a['id'] == agent2_id), None)
    
    if not agent1_data or not agent2_data:
        return jsonify({"error": "Invalid agent selection"}), 400
    
    # Initialize agents
    agent1 = RelationshipAgent(
        agent_json_path=agent1_data['path'],
        partner_json_path=agent2_data['path'],
        temperature=temperature
    )
    
    agent2 = RelationshipAgent(
        agent_json_path=agent2_data['path'],
        partner_json_path=agent1_data['path'],
        temperature=temperature
    )
    
    # Load vacation scenario
    with open('scenarios/vacation.json', 'r') as f:
        scene_data = json.load(f)
    
    # Generate first scene
    curr_scenario = cleaned_response(next_scene(0, agent1_data['name'], agent2_data['name'], "", ""))
    
    # Update agents with scenario
    agent1.update_chat_prompt(curr_scenario, "", "")
    agent2.update_chat_prompt(curr_scenario, "", "")
    
    # Generate conversation starter
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    conversation_starter = cleaned_response(agent1.generate_conversation_starter(config))
    
    return jsonify({
        "conversation_id": thread_id,
        "scenario": curr_scenario,
        "starter": conversation_starter,
        "agent1_name": agent1_data['name'],
        "agent2_name": agent2_data['name'],
        "agent1_id": agent1_id,
        "agent2_id": agent2_id,
        "total_scenes": scene_data['length']
    })

@app.route('/api/continue-conversation', methods=['POST'])
def continue_conversation():
    """Continue the conversation with a response"""
    data = request.json
    conversation_id = data.get('conversation_id')
    agent1_id = data.get('agent1_id')
    agent2_id = data.get('agent2_id')
    current_message = data.get('message')
    remaining_turns = data.get('remaining_turns', 5)
    current_scene = data.get('current_scene', 0)
    agent1_summary = data.get('agent1_summary', '')
    agent2_summary = data.get('agent2_summary', '')
    
    if not agent1_id or not agent2_id:
        return jsonify({"error": "Agent IDs required"}), 400
    
    agents = get_available_agents()
    agent1_data = next((a for a in agents if a['id'] == agent1_id), None)
    agent2_data = next((a for a in agents if a['id'] == agent2_id), None)
    
    if not agent1_data or not agent2_data:
        return jsonify({"error": "Invalid agent selection"}), 400
    
    # Initialize agents
    agent1 = RelationshipAgent(
        agent_json_path=agent1_data['path'],
        partner_json_path=agent2_data['path']
    )
    
    agent2 = RelationshipAgent(
        agent_json_path=agent2_data['path'],
        partner_json_path=agent1_data['path']
    )
    
    config = {"configurable": {"thread_id": conversation_id}}
    
    # Generate response from agent2
    response = cleaned_response(agent2.run(current_message, config, remaining_turns))
    
    return jsonify({
        "response": response,
        "agent_name": agent2_data['name']
    })

@app.route('/api/next-scene', methods=['POST'])
def get_next_scene():
    """Get the next scene in the scenario"""
    data = request.json
    scene_number = data.get('scene_number')
    agent1_id = data.get('agent1_id')
    agent2_id = data.get('agent2_id')
    agent1_summary = data.get('agent1_summary', '')
    agent2_summary = data.get('agent2_summary', '')
    
    if not agent1_id or not agent2_id:
        return jsonify({"error": "Agent IDs required"}), 400
    
    agents = get_available_agents()
    agent1_data = next((a for a in agents if a['id'] == agent1_id), None)
    agent2_data = next((a for a in agents if a['id'] == agent2_id), None)
    
    if not agent1_data or not agent2_data:
        return jsonify({"error": "Invalid agent selection"}), 400
    
    # Generate next scene
    next_scenario = cleaned_response(next_scene(scene_number, agent1_data['name'], agent2_data['name'], agent1_summary, agent2_summary))
    
    return jsonify({
        "scenario": next_scenario
    })

@app.route('/api/summarize', methods=['POST'])
def summarize_conversation():
    """Generate conversation summaries for both agents"""
    data = request.json
    conversation_id = data.get('conversation_id')
    agent1_id = data.get('agent1_id')
    agent2_id = data.get('agent2_id')
    
    if not agent1_id or not agent2_id:
        return jsonify({"error": "Agent IDs required"}), 400
    
    agents = get_available_agents()
    agent1_data = next((a for a in agents if a['id'] == agent1_id), None)
    agent2_data = next((a for a in agents if a['id'] == agent2_id), None)
    
    if not agent1_data or not agent2_data:
        return jsonify({"error": "Invalid agent selection"}), 400
    
    # Initialize agents
    agent1 = RelationshipAgent(
        agent_json_path=agent1_data['path'],
        partner_json_path=agent2_data['path']
    )
    
    agent2 = RelationshipAgent(
        agent_json_path=agent2_data['path'],
        partner_json_path=agent1_data['path']
    )
    
    config = {"configurable": {"thread_id": conversation_id}}
    
    # Generate summaries
    agent1_summary = cleaned_response(agent1.summarize_conversation(config))
    agent2_summary = cleaned_response(agent2.summarize_conversation(config))
    
    return jsonify({
        "agent1_summary": agent1_summary,
        "agent2_summary": agent2_summary,
        "agent1_name": agent1_data['name'],
        "agent2_name": agent2_data['name']
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)