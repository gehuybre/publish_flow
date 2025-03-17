# Press Release Enhancement System

This system uses a multi-agent approach powered by Google Generative AI and CrewAI to create high-quality press releases. The system includes specialized agents for different stages of the press release creation process, working together in a coordinated workflow.

## Features

- **Multi-agent architecture**: Specialized agents for strategic planning, writing, fact-checking, editing, copywriting, quality assurance, and HTML formatting
- **Modular design**: Clean separation of agents and tasks into individual components
- **Flexible API key handling**: Works in various environments (Colab, local development)
- **Special instructions handling**: Automatically detects topics and applies relevant special instructions
- **Legacy mode**: Supports both multi-agent and single-model approaches

## Setup

### Prerequisites

- Python 3.8 or higher
- Google Generative AI API key

### Installation

1. Clone the repository or download the source code:

2. Install dependencies:
   ```
   python setup.py
   ```

3. Configure your API key (any of these methods will work):
   - Set an environment variable: `export AI_STUDIO_API=your_api_key`
   - Use the `--api_key` flag when running setup or main scripts
   - Store the key in a file at `~/.ai_studio_api`
   - In Colab, use `userdata.set('AI_STUDIO_API', 'your_api_key')`

### Project Structure

```
publish_flow/
├── agents/                   # Agent modules
│   ├── __init__.py
│   ├── agent_base.py         # Base agent class
│   ├── content_strategist.py # Content strategy agent
│   ├── press_release_writer.py # Press release writing agent
│   └── ...                   # Other agent modules
├── tasks/                    # Task modules
│   ├── __init__.py
│   ├── task_base.py          # Base task class
│   ├── strategy_task.py      # Strategic framework task
│   ├── writing_task.py       # Press release writing task
│   └── ...                   # Other task modules
├── data/                     # Data files
│   ├── emv_pers.json         # Input JSON data
│   ├── output.txt            # Generated output
│   └── drafts/               # Storage for draft versions
├── prompts/                  # Prompt templates
│   ├── system_prompt.txt     # Base system prompt
│   ├── hyperlink_requirements.txt # Hyperlink instructions
│   └── special_instructions/ # Topic-specific instructions
├── user_input/               # User input files
│   └── prompt_1.txt          # User prompt
├── api_key_helper.py         # Helper for API key handling
├── press_release_system.py   # Main system class
├── main.py                   # Entry point script
├── setup.py                  # Installation script
└── README.md                 # This file
```

## Usage

### Running the System

To run the system with default settings:

```bash
python main.py
```

### Command-line Options

The main script accepts several command-line options:

- `--base_path`: Path to the project directory (default: "/content/drive/MyDrive/Colab Notebooks/publish_flow")
- `--mode`: Mode to run, either "crew" (multi-agent) or "legacy" (single model) (default: "crew")
- `--api_key`: Google AI API key (optional if set elsewhere)

Example:

```bash
python main.py --base_path /path/to/project --mode crew --api_key your_api_key
```

### Setting Up in Colab

If running in Colab, you can set up your API key in a separate cell:

```python
import os
os.environ['AI_STUDIO_API'] = "your_api_key"

# You can verify it's set correctly
print(f"API key is set: {os.environ.get('AI_STUDIO_API') is not None}")
```

## Customization

### Adding New Agents

To add a new agent:

1. Create a new file in the `agents/` directory (e.g., `agents/new_agent.py`)
2. Implement a class that extends `BaseAgent`
3. Add the agent to `agents/__init__.py`
4. Update `press_release_system.py` to use the new agent

### Adding New Tasks

To add a new task:

1. Create a new file in the `tasks/` directory (e.g., `tasks/new_task.py`)
2. Implement a class that extends `BaseTask`
3. Add the task to `tasks/__init__.py`
4. Update `press_release_system.py` to use the new task

### Modifying Prompts

- Edit `prompts/system_prompt.txt` to change the base system prompt
- Edit or add files in `prompts/special_instructions/` for topic-specific instructions

## Troubleshooting

### API Key Issues

If you encounter API key errors:

1. Verify your API key is correct
2. Check that it's being loaded correctly (try printing `os.environ.get('AI_STUDIO_API')`)
3. Try explicitly passing the key via the command line: `python main.py --api_key your_api_key`

### Google API Compatibility

If you encounter compatibility issues with the Google API:

1. Check your installed version: `pip show google-generativeai`
2. Update to the latest version: `pip install --upgrade google-generativeai`

The system is designed to handle different versions of the API, but you may need to adjust code if using a very old or new version.

## License

This project is licensed under the MIT License - see the LICENSE file for details.