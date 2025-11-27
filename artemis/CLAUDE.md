# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Artemis is a **Multiagent Environment for Macro-scale Interaction Simulation**. It's a Python-based simulation framework for AI agent interactions built on the Qwen Agent framework.

## Development Commands

### Environment Setup
- Python version: 3.13.4+
- Package manager: `uv` (recommended) or `pip`
- Install dependencies: `uv sync` or `pip install -e .`

### Running the Application
- Main application: `python main.py`
  - Interactive chat interface with an AI assistant
  - Type 'exit' or 'quit' to terminate

### Testing
- Run all tests: `pytest`
- Run tests with verbose output: `pytest -v`
- Run specific test file: `pytest tests/test_filename.py`

### Code Formatting
- Format code: `black .`
- Sort imports: `isort .`
- Format and sort together: `isort . && black .`

## Architecture

### Core Components

**Simulation Core** (`src/core/`)
- `artemis_model.py`: Core simulation model with deterministic random number generation
  - Takes `SimulationConfig` to initialize simulation parameters
  - Uses seeded random number generator for reproducible results
  - Provides `get_random_int()` and `get_random_float()` utility methods
- `simulation_config.py`: Comprehensive simulation configuration system
  - `SpaceType`: Defines simulation space types (GRID_2D, CONTINUOUS_2D, NETWORK)
  - `TopologyType`: Boundary conditions (BOUNDED, TORUS)
  - `NeighborhoodType`: Agent interaction patterns (MOORE, VON_NEUMANN, CUSTOM)
  - `SchedulerType`: Agent activation scheduling (RANDOM, SEQUENTIAL, STAGED)
  - `SimulationConfig`: Dataclass for complete simulation configuration with defaults

**Agent System** (`src/agent/`)
- `assistant.py`: Creates and configures AI assistants using Qwen Agent
  - Default model: `qwen2.5:1.5b` running via local Ollama server at `http://localhost:11434/v1`
  - Agents are created with a function list and system message configuration
  - LLM configuration includes top_p, temperature, and max_input_tokens settings
- **Agent Memory System**: Abstract memory management for conversation history
  - `memory.py`: Base `Memory` abstract class defining `get()` and `put()` interface
  - `short_term_memory.py`: Simple message list storage for recent interactions
  - `context_window_memory.py`: Token-limited memory that preserves system messages and recent context
  - `summarization_based_memory.py`: AI-powered conversation summarization using the assistant
    - Configurable min/max summary length
    - Automatically summarizes conversation history using the LLM

**Tools/Functions** (`src/functions/`)
- Tools extend `BaseTool` from `qwen_agent.tools.base`
- Register tools with `@register_tool('tool_name')` decorator
- Tools must implement:
  - `description`: String describing the tool
  - `parameters`: List of dicts defining name, type, and required status
  - `call(params: str, **kwargs) -> str`: Main execution method that receives JSON string params

**Main Application** (`main.py`)
- Interactive message loop that maintains conversation history
- Streams responses from the agent using `bot.run(messages=messages)`
- Messages follow the standard role/content format: `{'role': 'user', 'content': query}`

### Key Dependencies

- **qwen-agent**: Core agent framework providing Assistant and tool infrastructure
- **python-dateutil**: Date/time utilities
- **pytest**: Testing framework
- **black**: Code formatter
- **isort**: Import sorter

### Project Structure

```
artemis/
├── src/
│   ├── core/           # Simulation model and configuration
│   │   ├── artemis_model.py       # Core simulation model
│   │   └── simulation_config.py   # Configuration enums and dataclasses
│   ├── agent/          # Agent system and memory management
│   │   ├── assistant.py                    # Agent creation and configuration
│   │   ├── memory.py                       # Abstract memory interface
│   │   ├── short_term_memory.py            # Simple message storage
│   │   ├── context_window_memory.py        # Token-limited memory
│   │   └── summarization_based_memory.py   # AI-powered summarization
│   └── functions/      # Tool implementations
│       └── calculator.py           # Calculator tool example
├── tests/              # Test suite
│   ├── test_artemis_model.py              # Core model tests
│   ├── test_short_term_memory.py          # Memory implementation tests
│   └── test_summarization_based_memory.py # Summarization tests
└── main.py             # Interactive chat application
```

## Adding New Tools

1. Create a new file in `src/functions/`
2. Import `BaseTool` and `register_tool` from `qwen_agent.tools.base`
3. Define a class decorated with `@register_tool('tool_name')`
4. Implement `description`, `parameters`, and `call()` method
5. Import the tool class in `src/agent/assistant.py`
6. Add the tool name to the `function_list` in `create_assistant()`

Example pattern (see `src/functions/calculator.py`):
```python
@register_tool('tool_name')
class ToolName(BaseTool):
    description = 'Tool description'
    parameters = [{'name': 'param', 'type': 'string', 'required': True}]

    def call(self, params: str, **kwargs) -> str:
        data = json.loads(params)
        # Implementation
        return json.dumps({'result': result})
```

## Working with Simulation Configuration

The simulation configuration system provides a flexible way to configure agent-based simulations:

**Creating a Configuration** (see `src/core/simulation_config.py`):
```python
from src.core.simulation_config import (
    SimulationConfig, SpaceType, TopologyType,
    NeighborhoodType, SchedulerType
)

config = SimulationConfig(
    space_type=SpaceType.GRID_2D,
    topology=TopologyType.TORUS,
    neighborhood_type=NeighborhoodType.MOORE,
    scheduler=SchedulerType.RANDOM,
    dimensions=(10, 10),
    num_agents=50,
    max_steps=100,
    seed=42  # For reproducible simulations
)
```

**Using with ArtemisModel** (see `src/core/artemis_model.py`):
```python
from src.core.artemis_model import ArtemisModel

model = ArtemisModel(simulationConfig=config)
# Random number generation is now seeded and deterministic
random_int = model.get_random_int()    # Returns int between 0-100
random_float = model.get_random_float()  # Returns float between 0.0-1.0
```

## Working with Agent Memory

The memory system allows agents to manage conversation history in different ways:

**Short-Term Memory** - Stores all messages:
```python
from src.agent.short_term_memory import ShortTermMemory

memory = ShortTermMemory()
# Add messages to memory._messages list
# Call memory.get() to retrieve all messages
```

**Context Window Memory** - Limits messages by token count:
```python
from src.agent.context_window_memory import ContextWindowMemory

memory = ContextWindowMemory(max_tokens=2048)
# Automatically preserves system messages and recent context
messages = memory.get()  # Returns system msgs + recent messages
```

**Summarization-Based Memory** - AI-powered summarization:
```python
from src.agent.summarization_based_memory import SummarizationBasedMemory
from src.agent.assistant import create_assistant

bot = create_assistant()
memory = SummarizationBasedMemory(bot, min_length=3, max_length=5)
# Add messages to memory._messages list
summary = memory.get()  # Returns AI-generated summary of conversation
```

## Local LLM Server

The project uses Ollama for local LLM inference. Ensure Ollama is running before starting the application:
- Server endpoint: `http://localhost:11434/v1`
- Default model: `qwen2.5:1.5b`
- API key configured as 'EMPTY' for local server
- Generation config includes top_p (0.8), temperature (0.7), and max_input_tokens (4096)

To change the model or server, modify the `llm_cfg` in `src/agent/assistant.py:8-17`.
