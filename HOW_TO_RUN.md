# QuoteBot v2 - Reliable Run Guide

## First time setup
```bash
conda activate rasa_env
cd "/Users/aanyagarg/Desktop/PROJECT 1"
python -m pip install -r requirements-web.txt
```

## Train model
```bash
conda activate rasa_env
cd "/Users/aanyagarg/Desktop/PROJECT 1"
python -m rasa train
```

## Start (recommended: 2 terminals)

Terminal 1 (Rasa backend):
```bash
conda activate rasa_env
cd "/Users/aanyagarg/Desktop/PROJECT 1"
python -m rasa run --model "$(ls -t models/*.tar.gz | head -1)" --enable-api --cors "*" --port 5005
```

Terminal 2 (Web app):
```bash
conda activate rasa_env
cd "/Users/aanyagarg/Desktop/PROJECT 1"
WEB_PORT=8010 RASA_ENDPOINT="http://127.0.0.1:5005/webhooks/rest/webhook" python app.py
```

Open:
- http://127.0.0.1:8010

## Optional helper scripts
```bash
cd "/Users/aanyagarg/Desktop/PROJECT 1"
./start_project.sh
./stop_project.sh
```

## If you still get wrong outputs
1. Stop everything: `./stop_project.sh`
2. Retrain: `python -m rasa train`
3. Start again using the 2-terminal method above
