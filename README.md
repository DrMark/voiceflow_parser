# Voiceflow Parser

A tool to parse Voiceflow exports (.vf files) and generate structured project files.

## Overview

Voiceflow is a low-code LLM building system used for prototyping projects. When moving to production, the entire system needs to be rebuilt. This tool accelerates the rebuilding process by parsing the Voiceflow export (.vf file) and generating appropriate files and folders that match the structure of the original Voiceflow project.

## Installation

### Development Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd voiceflow_parser
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```
   pip install -e .
   ```

## Usage

### Basic Usage

```bash
# Parse a Voiceflow export file
voiceflow-parser parse path/to/export.vf

# Parse a Voiceflow export file with a specific output directory
voiceflow-parser parse path/to/export.vf --output custom_output_directory

# Analyze a Voiceflow export file
voiceflow-parser analyze path/to/export.vf

# Display version information
voiceflow-parser version
```

### Folder Structure

When you run the parser, it automatically organizes files into the following structure:

```
project_root/
├── voiceflow_exports/       # Contains original Voiceflow export files (.vf)
│   ├── project1.vf
│   ├── project2.vf
│   └── ...
│
└── voiceflow_projects/      # Contains generated project files
    ├── project1/            # Generated files for project1
    │   ├── diagrams/
    │   ├── intents/
    │   ├── variables/
    │   ├── responses/
    │   ├── prompts/         # Comprehensive prompt information
    │   │   ├── prompts.json             # Basic prompt information
    │   │   ├── prompts_detailed.json    # Detailed prompt data with extracted content
    │   │   └── <prompt_name>/           # Individual prompt directories
    │   │       ├── complete_prompt.txt  # Full prompt specification
    │   │       ├── system.txt           # System prompt content
    │   │       ├── system_messages.txt  # Role-specific system messages
    │   │       ├── user_messages.txt    # Role-specific user messages
    │   │       ├── messages.json        # Raw message data
    │   │       └── messages.txt         # Human-readable message content
    │   ├── agents/
    │   ├── buttons/
    │   ├── captures/
    │   ├── apis/
    │   ├── kb_searches/
    │   ├── choices/
    │   ├── cards/
    │   ├── project.json
    │   └── README.md
    │
    ├── project2/            # Generated files for project2
    └── ...
```

This organization provides a clear separation between source files and generated content, making it easier to manage multiple Voiceflow projects.

### Prompt Handling

The parser extracts comprehensive prompt information from multiple locations in the Voiceflow export:
- System prompts from the `programResources.prompts` section
- Message content from nested data structures in the `promptMessages` section
- Variable placeholders and cross-references between prompts

For each prompt, the parser generates:
- A complete specification file (`complete_prompt.txt`) containing all prompt elements
- Role-specific files for system and user messages
- JSON files containing the raw data and extracted content
- Human-readable text files for easy review

## Project Structure

```
voiceflow_parser/
├── voiceflow_parser/       # Main package
│   ├── models/            # Data models for Voiceflow exports
│   ├── services/          # Business logic for parsing and generating files
│   ├── utils/             # Utility functions
│   ├── main.py            # Main application logic
│   └── cli.py             # Command-line interface
├── tests/                 # Test suite
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── .venv/                 # Virtual environment (not tracked in git)
├── setup.py               # Package setup file
└── requirements.txt       # Development dependencies
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black voiceflow_parser tests
isort voiceflow_parser tests
```

### Type Checking

```bash
mypy voiceflow_parser
```

## License

[Add your license information here]
