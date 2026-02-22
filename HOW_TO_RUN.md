# QuoteBot v2 - Reliable Run Guide

## 1) First-time setup
```bash
conda create -n rasa_env python=3.10 -y
conda activate rasa_env
cd "<project-folder-path>"
python -m pip install --upgrade pip
python -m pip install rasa
python -m pip install -r requirements-web.txt
```

## 2) Train model
```bash
conda activate rasa_env
cd "<project-folder-path>"
python -m rasa train
```

## 3) Start (recommended: 2 terminals)

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
- http://127.0.0.1:8010

## 4) Optional helper scripts (portable)
```bash
cd "<project-folder-path>"
./start_project.sh
./stop_project.sh
```

## 5) If outputs are wrong
1. Stop everything: `./stop_project.sh`
2. Retrain: `python -m rasa train`
3. Start again using the 2-terminal method above

## Notes
- Replace `<project-folder-path>` with your actual folder location.
- If your path has spaces, keep it in quotes.
