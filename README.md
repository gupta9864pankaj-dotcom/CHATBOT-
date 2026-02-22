# Quotes Recommendation Chatbot (Rasa + Flask)

An emotion-aware, multilingual chatbot that recommends realistic quotes and supportive replies based on user intent and mood.

## Features

- Intent-based quote recommendations: motivation, inspiration, success, love, funny
- Emotion support intents: stress, anxiety, sadness, lonely, failure
- Multilingual input examples: English, Hindi, Telugu
- Web chat UI (Flask) with live connection to Rasa REST API
- Helper scripts for one-command start/stop

## Tech Stack

- Python
- Rasa (NLU + Core)
- Flask
- YAML training/config files (`nlu.yml`, `stories.yml`, `rules.yml`, `domain.yml`)

## Project Structure

- `data/nlu.yml`: intent training data
- `data/stories.yml`: conversation stories
- `data/rules.yml`: rule-based behavior
- `domain.yml`: intents, responses, session config
- `config.yml`: pipeline and policies
- `app.py`: Flask web server + Rasa API bridge
- `templates/index.html`: web chat UI
- `start_project.sh`: auto train/start services
- `stop_project.sh`: stop running services

## Prerequisites

- Python 3.10 recommended
- Conda (optional but recommended on macOS)

## Setup

```bash
conda create -n rasa_env python=3.10 -y
conda activate rasa_env
cd "<project-folder-path>"
python -m pip install --upgrade pip
python -m pip install rasa
python -m pip install -r requirements-web.txt
```

## Train Model

```bash
conda activate rasa_env
cd "<project-folder-path>"
python -m rasa train
```

The trained model is saved in `models/`.

## Run (Recommended: 2 Terminals)

Terminal 1 (Rasa backend):

```bash
conda activate rasa_env
cd "<project-folder-path>"
python -m rasa run --model "$(ls -t models/*.tar.gz | head -1)" --enable-api --cors "*" --port 5005
```

Terminal 2 (Web app):

```bash
conda activate rasa_env
cd "<project-folder-path>"
WEB_PORT=8010 RASA_ENDPOINT="http://127.0.0.1:5005/webhooks/rest/webhook" python app.py
```

Open:

- `http://127.0.0.1:8010`

## Run (One Command)

```bash
cd "<project-folder-path>"
./start_project.sh
```

Stop services:

```bash
cd "<project-folder-path>"
./stop_project.sh
```

## Testing

Interactive shell test:

```bash
python -m rasa shell
```

Automated story tests:

```bash
python -m rasa test
```

## Troubleshooting

- `No module named rasa`
  - Fix: activate the correct environment and install rasa there.
  - `conda activate rasa_env && python -m pip install rasa`

- `zsh: command not found: rasa`
  - Fix: use module execution style:
  - `python -m rasa train`

- `Could not reach Rasa server`
  - Start backend first:
  - `python -m rasa run --enable-api --cors "*"`

- `cd: no such file or directory: <project-folder-path>`
  - Wrap path in quotes because of space:
  - `cd "<project-folder-path>"`

## License

For academic and learning use.
