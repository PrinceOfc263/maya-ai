# Maya AI

Maya is a voice-first personal AI assistant being developed for Linux.

## Current status

Version 0.1.0 provides a basic command-line interface with:
- Greeting and help commands
- Local time and date
- Basic system information
- Web search link generation
- Safe command handling
- Automated unit tests

## Requirements

- Python 3.10 or newer
- Git

The initial core uses only Python's standard library.

## Run Maya

From the repository root:

```bash
python -m maya
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Development roadmap

1. Core assistant and command handling
2. Local microphone input and speech output
3. Hybrid AI reasoning using available free services
4. Local Linux desktop integration
5. Web research and coding tools
6. Permission-controlled automation and testing loops

Important: GitHub Codespaces runs in the cloud. Desktop automation and
microphone access for the user's physical computer require a separate
local runtime on that computer.

Maya must request appropriate approval before performing destructive
file operations, privileged system changes, or other sensitive actions.
