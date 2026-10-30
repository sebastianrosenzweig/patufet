# Installation & Run

For running the server, we need to install the open-source speech synthesizer eSpeak NG:

```
sudo apt-get update
sudo apt-get install espeak-ng
```

Also, we need to install the Python environment defined in `pyproject.toml`. 
For this one can use tools like poetry and the command: `poetry install`
Run the server by `poetry run python -m patufet`.

All required AI models will be downloaded automatically on first run.
