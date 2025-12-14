# Vaisiri Voice Assistant

Lightweight, local-first voice assistant for running LLM-based assistants and local TTS/STT.

## Quickstart

1. Create a virtualenv and install dependencies:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the assistant (example):

```powershell
python -m src.vaisiri.main
```

3. Run tests:

```powershell
pytest
```

## Project layout

- `src/vaisiri/` — core package
- `config/` — configuration files
- `scripts/` — helper scripts (data/indexing)

## Contributing

- Open issues or PRs on GitHub: https://github.com/hemanth-ramesh/Vaisiri-Voice-Assistant

## License

Add your license here.
