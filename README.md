# Quotes Recommendation Chatbot (Rasa + Flask)

An emotion-aware, multilingual chatbot that recommends realistic quotes and supportive replies based on user intent and mood.

## Problem Statement

In today's fast-paced digital life, many users experience stress, demotivation, emotional imbalance, or lack of inspiration due to academic, professional, or personal pressure.
Although motivational and emotional support content is widely available online, users often need to manually search across websites and social media, which is slow, repetitive, and not personalized.

This project solves that gap by building an interactive chatbot that:

- understands user intent and emotional context in natural language
- returns relevant quote categories in real time (motivation, inspiration, love, success, humor, and emotional support)
- provides a conversational and personalized experience instead of static quote browsing

The goal is to improve accessibility to uplifting content, increase user engagement, and provide quick emotional encouragement through AI-driven conversation.

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

## Quick Fix: "Rasa server is offline"

If the web page shows this error, it means `app.py` is running but Rasa backend is not reachable on port `5005`.

Use this direct method:

1. Start Rasa backend first (Terminal 1):
```bash
cd Project
conda activate rasa_env
python -m rasa train
python -m rasa run --enable-api --cors "*" --port 5005 --debug
```

2. Start web app second (Terminal 2):
```bash
cd Project
conda activate rasa_env
RASA_ENDPOINT="http://127.0.0.1:5005/webhooks/rest/webhook" python app.py
```

3. Open browser:
- `http://127.0.0.1:8010`

4. Verify backend is live:
- `http://127.0.0.1:5005/status`

If `/status` does not open, Rasa backend is not running correctly. Check Terminal 1 logs and fix that first.

## License

For academic and learning use.
