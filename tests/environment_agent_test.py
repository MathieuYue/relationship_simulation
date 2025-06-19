from environment import EnvironmentAgent

def demo_environment_agent():
    agent = EnvironmentAgent()
    cues = agent._generate_cues("home")
    print(cues)

    agent._update_world({"location": "home", "privacy": 0.5})
    print(agent.world_state)
    result = agent.agent.invoke({
        "input": "Describe the environment at home.",
        "chat_history": [],
        "agent_scratchpad": []
    })
    print(result)

if __name__ == "__main__":
    demo_environment_agent()

