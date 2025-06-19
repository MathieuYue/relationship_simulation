from relationship_agent import RelationshipAgent
import json
import os
import uuid

def main():
    # Check if required JSON files exist
    # Initialize the relationship agent
    agent = RelationshipAgent(
    agent_json_path="sample_agents/blake_lively/basics.json",
    partner_json_path="sample_agents/ryan_reynolds/basics.json",
    scenario_description="The partners are deciding where to go for vacation. Blake wants to go to Paris, but Ryan wants to go to Tokyo.",
    conversation_summary="",
    context="",
    temperature=0.7
)

    print("Welcome to the Relationship Agent REPL!")
    print("Type 'exit' to quit, 'summary' to get a conversation summary")
    print("-" * 50)

    thread_id = uuid.uuid4()
    config = {"configurable": {"thread_id": thread_id}}

    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for exit command
            if user_input.lower() == 'exit':
                print("\nGoodbye!")
                break
            
            # Check for summary command
            if user_input.lower() == 'summary':
                summary = agent.summarize_conversation(config={})
                print("\nConversation Summary:")
                print(summary)
                continue
            
            # Process the input through the agent
            response = agent.run(user_input, config=config)
            print(f"\nAgent: {response}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()
