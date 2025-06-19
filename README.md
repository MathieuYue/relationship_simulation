# Agent Chat Simulator Web App

A web application that allows you to choose any two agents from the sample agents and watch them interact in conversation scenarios. Built with Flask and modern web technologies.

## Features

- 🤖 **Dynamic Agent Selection**: Choose any two agents from the available sample agents
- 💬 **Interactive Conversations**: Watch AI agents have realistic conversations
- 🎭 **Scenario-Based**: Agents interact within vacation scenarios
- 📊 **Conversation Analysis**: Generate summaries of conversations from each agent's perspective
- 🎨 **Modern UI**: Beautiful, responsive interface with real-time updates
- ⚙️ **Creativity Control**: Adjust the AI's creativity level with temperature settings

## Available Agents

The app automatically detects all agents in the `sample_agents/` directory, including:
- Blake Lively
- Ryan Reynolds  
- Emily Blunt
- John Krasinski
- Taylor Swift
- Travis Kelce
- Kim Kardashian
- Kanye West
- Zendaya
- Tom Holland
- And any other agents you add to the directory

## Prerequisites

- Python 3.8+
- Lambda AI API key
- Internet connection

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

Create a `.env` file in the root directory:

```bash
LAMBDA_API_KEY=your_lambda_api_key_here
```

### 3. Run the Application

```bash
python run.py
```

Or directly:

```bash
python app.py
```

The web app will be available at: **http://localhost:5000**

## How to Use

1. **Select Agents**: Choose any two agents from the dropdown menus
2. **Adjust Creativity**: Use the slider to control how creative the AI responses are
3. **Start Conversation**: Click "Start Conversation" to begin
4. **Watch & Interact**: 
   - Use "Continue Conversation" to let the agents keep talking
   - Use "Next Scene" to move to a new scenario
   - Use "Summarize" to get AI analysis of the conversation
5. **Reset**: Start over with different agents

## API Endpoints

- `GET /` - Main web interface
- `GET /api/agents` - Get list of available agents
- `POST /api/start-conversation` - Start a new conversation
- `POST /api/continue-conversation` - Continue the conversation
- `POST /api/next-scene` - Move to next scenario
- `POST /api/summarize` - Generate conversation summaries

## Project Structure

```
├── app.py                 # Flask web application
├── run.py                 # Startup script with error checking
├── requirements.txt       # Python dependencies
├── relationship_agent.py  # AI agent implementation
├── environment.py         # Scenario generation
├── parser_utils.py        # Response parsing utilities
├── prompt_utils.py        # Prompt management
├── json_utils.py          # JSON file utilities
├── templates/
│   └── index.html         # Main web interface
├── sample_agents/         # Agent personality data
├── scenarios/             # Scenario definitions
└── README.md             # This file
```

## Adding New Agents

1. Create a new directory in `sample_agents/` with the agent's name
2. Add a `basics.json` file with the agent's personality data
3. The web app will automatically detect and include the new agent

Example `basics.json`:
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "personality": "Friendly and outgoing person who loves adventure"
}
```

## Customization

### Modifying Scenarios
Edit `scenarios/vacation.json` to add new scenarios or modify existing ones.

### Adjusting AI Behavior
- Use the temperature slider in the web interface (0 = conservative, 1 = creative)
- Modify the `RelationshipAgent` class in `relationship_agent.py` for more advanced customization

### Styling
The web interface uses Tailwind CSS. Modify the classes in `templates/index.html` to change the appearance.

## Troubleshooting

### Common Issues

1. **"LAMBDA_API_KEY not found"**
   - Create a `.env` file with your API key
   - Make sure the file is in the root directory

2. **"Module not found" errors**
   - Install dependencies: `pip install -r requirements.txt`

3. **"Required file not found"**
   - Make sure all the original files from your project are present
   - Check that `sample_agents/` and `scenarios/` directories exist

4. **Port already in use**
   - Change the port in `app.py` or `run.py`
   - Kill any existing processes using port 5000

### Debug Mode

The app runs in debug mode by default. Check the terminal for detailed error messages.

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## License

This project is for educational and entertainment purposes.

## Acknowledgments

- Lambda AI for providing the language model API
- LangChain for the AI framework
- Flask for the web framework
- Tailwind CSS for the styling 