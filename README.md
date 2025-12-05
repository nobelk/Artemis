# Artemis

**A**gent **R**eputation & **T**rust **E**nvironment for **M**acro-scale **I**nteraction **S**imulation

A Python-based multiagent environment for simulating macro-scale interactions between AI-powered agents. Built on the Qwen Agent framework, Artemis provides a flexible platform for exploring agent behavior, memory systems, and social dynamics in configurable simulation environments.

## Architecture

Artemis follows a modular, layered architecture designed for extensibility and experimentation:

### Core Components

```
artemis/
├── src/
│   ├── core/              # Simulation engine
│   ├── agent/             # AI agent system with memory
│   └── functions/         # Extensible tool system
├── tests/                 # Comprehensive test suite
└── main.py               # Interactive chat application
```

#### Simulation Engine (`src/core/`)

- **ArtemisModel**: Core simulation model with deterministic random number generation using seeded RNG
- **SimulationConfig**: Comprehensive configuration system using dataclasses and enums
  - Space types: GRID_2D, CONTINUOUS_2D, NETWORK
  - Topology types: BOUNDED (hard boundaries), TORUS (wrapped edges)
  - Neighborhood types: MOORE (8 neighbors), VON_NEUMANN (4 neighbors), CUSTOM
  - Scheduler types: RANDOM, SEQUENTIAL, STAGED

#### Agent System (`src/agent/`)

**AI Assistant** (`assistant.py`):
- Powered by Qwen Agent framework with local Ollama LLM server
- Default model: `qwen2.5:1.5b`
- Configurable parameters: top_p=0.8, temperature=0.7, max_input_tokens=4096
- Extensible tool system via function registration

**Memory System** (Abstract hierarchy):
- **Memory**: Abstract base class defining `get()` and `put()` interface
- **ShortTermMemory**: Unlimited message storage
- **ContextWindowMemory**: Token-limited storage (default 2048 tokens) with system message preservation
- **SummarizationBasedMemory**: AI-powered conversation summarization (configurable 3-5 sentence summaries)

#### Tool System (`src/functions/`)

Extensible tool framework using `@register_tool` decorator pattern:
- **Calculator**: Example implementation demonstrating tool creation
- Easy extension: create new tools by implementing description, parameters, and `call()` method

### Design Patterns

- **Abstract Base Classes**: Extensible memory system
- **Dataclasses**: Type-safe configuration
- **Enums**: Clear simulation parameter definitions
- **Dependency Injection**: Configurable component initialization
- **Decorator Pattern**: Tool registration system
- **Strategy Pattern**: Multiple memory implementations with common interface

## Codebase Overview

- **Language**: Python 3.13.4+
- **Total Code**: ~528 lines (excluding comments and blank lines)
- **Test Coverage**: 30 test cases across core components
- **Version**: 0.1.0 (early development)
- **License**: Apache License 2.0

### Key Dependencies

- **qwen-agent** (>=0.0.10): Core agent framework
- **python-dateutil** (>=2.8.2): Date/time utilities
- **pytest** (>=9.0.1): Testing framework
- **black** (>=25.11.0): Code formatter
- **isort** (>=7.0.0): Import sorter

## Build Instructions

### Prerequisites

- Python 3.13.4 or higher
- `uv` package manager (recommended) or `pip`
- Ollama server (optional, for interactive chat)

### Installation

#### Using uv (recommended)

```bash
# Install dependencies
uv sync

# Build package
uv build
```

#### Using pip

```bash
# Install in development mode
pip install -e .
```

### Code Quality

Format code and sort imports:

```bash
# Format code
black .

# Sort imports
isort .

# Run both
isort . && black .
```

## Run Instructions

### Interactive Chat Application

Start an interactive chat session with the AI assistant:

```bash
python main.py
```

The application:
- Streams responses from the AI agent
- Maintains conversation history
- Type `exit` or `quit` to terminate

**Note**: Requires Ollama running locally at `http://localhost:11434/v1` with the `qwen2.5:1.5b` model.

### Example Simulation Usage

```python
from src.core.simulation_config import (
    SimulationConfig, SpaceType, TopologyType,
    NeighborhoodType, SchedulerType
)
from src.core.artemis_model import ArtemisModel

# Create custom configuration
config = SimulationConfig(
    space_type=SpaceType.GRID_2D,
    topology=TopologyType.TORUS,
    neighborhood_type=NeighborhoodType.MOORE,
    scheduler=SchedulerType.RANDOM,
    dimensions=(10, 10),
    num_agents=50,
    max_steps=100,
    seed=42  # Deterministic RNG
)

# Initialize simulation
model = ArtemisModel(simulationConfig=config)
random_value = model.get_random_int()  # 0-100
random_float = model.get_random_float()  # 0.0-1.0
```

### Creating Custom Tools

Extend agent capabilities by adding tools:

```python
from qwen_agent.tools.base import register_tool, BaseTool

@register_tool('my_tool')
class MyTool(BaseTool):
    description = 'Description of what my tool does'
    parameters = [{
        'name': 'param1',
        'type': 'string',
        'description': 'Parameter description',
        'required': True
    }]

    def call(self, params: str, **kwargs) -> str:
        # Parse params (JSON string)
        # Implement tool logic
        return 'Result'
```

## Test Instructions

### Running Tests

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Run specific test file
pytest tests/test_artemis_model.py

# Run with coverage
pytest --cov=src tests/

# Run with coverage report
pytest --cov=src --cov-report=html tests/
```

### Test Suite Coverage

- **test_artemis_model.py** (9 tests): Core simulation model functionality
  - Initialization and configuration
  - RNG determinism and range validation
- **test_short_term_memory.py** (8 tests): Basic memory implementation
  - Message storage and retrieval
  - Inheritance validation
- **test_summarization_based_memory.py** (13 tests): AI-powered memory
  - Mock-based testing of summarization logic
  - Message filtering and system message preservation

### Continuous Integration

GitHub Actions workflow automatically runs on push and pull requests:
1. Code formatting checks (`isort`, `black`)
2. Full test suite execution
3. Code coverage analysis (via codecov)
4. Package build verification

## Project Status

Artemis is in early development (v0.1.0). Current focus areas:
- Core simulation engine and configuration system
- Agent memory architectures
- Tool extensibility framework

## Contributing

Contributions welcome! Please ensure:
- Code is formatted with `black` and `isort`
- All tests pass (`pytest`)
- New features include tests

## License

Apache License 2.0
