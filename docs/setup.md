# Setup

The course works the same way on macOS, Linux, and Windows. The only thing that changes is the shell.

## Prerequisites

- **Python 3.10 or newer** (tested up to 3.12).
  - macOS: `brew install python@3.12`
  - Ubuntu/Debian: `sudo apt-get install python3.12 python3.12-venv`
  - Windows: install from [python.org](https://www.python.org/downloads/) and tick *"Add python.exe to PATH"*.
- **Git** for cloning.

Confirm:

```bash
python3 --version    # macOS / Linux
py -3 --version      # Windows alternative
```

## Clone

```bash
git clone https://github.com/boblee0717/ai-agent-learning-lab.git
cd ai-agent-learning-lab
```

## Create a virtual environment and install

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
```

### Windows — PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

> If PowerShell refuses to run the activate script, allow it once for the current user:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### Windows — cmd.exe

```bat
py -3 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Verify everything works

```bash
# Smoke test
python examples/00_hello.py

# Run the agent from the command line
python -m agent_course "What is 8 * 7?"

# Course test suite (should be all green)
pytest

# Lint
ruff check .
```

The project uses forward-slash paths everywhere — they work on Windows too because Python normalizes them. There is no need to translate `examples/00_hello.py` into `examples\00_hello.py`.

## Optional: real LLM brain

```bash
pip install -e ".[llm]"
```

Then export your key. macOS / Linux:

```bash
export OPENAI_API_KEY="sk-..."
export USE_OPENAI=1
python examples/05_llm_brain.py
```

PowerShell:

```powershell
$env:OPENAI_API_KEY = "sk-..."
$env:USE_OPENAI = "1"
python examples/05_llm_brain.py
```

cmd.exe:

```bat
set OPENAI_API_KEY=sk-...
set USE_OPENAI=1
python examples/05_llm_brain.py
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: agent_course` | Forgot `pip install -e .` | Re-run install inside the activated venv |
| Tests pass on Windows but fail on macOS/Linux with strange whitespace diffs | Editor saved with CRLF line endings | The repo ships `.gitattributes` enforcing LF — re-checkout the file: `git checkout -- <file>` |
| `Activate.ps1 cannot be loaded because running scripts is disabled` | Default Windows execution policy | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `command not found: python` on macOS | macOS ships only `python3` | Use `python3` everywhere or `alias python=python3` in `~/.zshrc` |
| `permission denied` writing in `examples/04_memory.py` | Running from a read-only directory | `cd` into a writable location |
