# Quotes Recommendation Chatbot Using Rasa NLU

## 1. Abstract
This project presents an AI-based Quotes Recommendation Chatbot developed using Rasa NLU and Flask. The chatbot is designed to support users who experience stress, low motivation, emotional imbalance, or a need for inspiration. Instead of manually browsing websites and social media for suitable quotes, users can directly interact with the chatbot and receive relevant responses in real time. The system supports quote categories such as motivation, inspiration, success, love, and humor, and also supports emotional support intents such as stress, anxiety, sadness, loneliness, and failure. The chatbot is deployed through a browser-based interface and tested using both manual and story-based methods.

## 2. Problem Definition
In fast-paced academic and professional life, users often need motivational or emotionally supportive content quickly. Traditional methods are manual, slow, and non-personalized. Existing quote platforms are mostly static and do not provide conversational engagement.

The core problem addressed is:

- lack of a fast and intelligent conversational system that understands user intent/emotion and returns relevant quotes instantly.

## 3. Objectives
The main objectives of this project are:

- build a chatbot that understands user input using intent classification.
- deliver relevant quote categories through natural conversation.
- support multilingual user inputs (English, Hindi, Telugu examples).
- provide a web-based interface for easy user access.
- ensure reliable testing, model reusability, and deployment readiness.

## 4. Milestone-Wise Methodology

### Milestone 1: Problem Understanding
Activities completed:

- Business problem identification: manual quote search is inefficient.
- Business requirements definition: intent accuracy, engagement, accessibility.
- Literature survey: recommendation chatbots, NLP techniques, rule vs ML approaches.
- Social/business impact mapping.

### Milestone 2: Environment Setup
Activities completed:

- Python environment setup for Rasa-compatible versions.
- Rasa project setup with standard structure.
- Initialization of key files: `data/nlu.yml`, `data/stories.yml`, `data/rules.yml`, `domain.yml`, `config.yml`, `credentials.yml`, `endpoints.yml`.

### Milestone 3: Data Collection and Model Building
Activities completed:

- User training data preparation in `data/nlu.yml`.
- Response and intent mapping in `domain.yml`.
- Dialogue flow design in `data/stories.yml`.
- Rule-based handling in `data/rules.yml`.
- Model training using `python -m rasa train`.
- Model storage in `models/` for reuse.

### Milestone 4: Testing and Deployment
Activities completed:

- Manual testing via `python -m rasa shell`.
- Story-based testing via `tests/test_stories.yml`.
- Web deployment using Flask (`app.py`) and Rasa REST API.
- End-to-end validation in browser.

## 5. System Requirements

### Software Requirements

- Python 3.10
- Rasa 3.6.21
- Flask
- YAML-based Rasa training/config files
- Git (for version control and deployment)

### Development Tools

- Visual Studio Code (or any IDE)
- Terminal/PowerShell
- Browser for chatbot interface testing

## 6. Project Architecture
The system follows a three-layer architecture:

1. User Interface Layer:
- Flask web page (`templates/index.html`) and API routes in `app.py`.

2. NLP and Dialogue Layer:
- Rasa NLU for intent classification.
- Rasa Core for dialogue policy and rule/story execution.

3. Response Layer:
- Predefined, category-specific quote responses in `domain.yml`.
- Follow-up prompts and feedback handling.

Request flow:

- user enters message in web UI.
- Flask sends message to Rasa REST webhook (`/webhooks/rest/webhook`).
- Rasa predicts intent and selects action/response.
- Flask returns response to UI.

## 7. Data and Intent Design
The NLU dataset is defined in `data/nlu.yml` with multiple examples per intent. Implemented intents include:

- `greet`, `goodbye`
- `ask_motivation`, `ask_inspiration`, `ask_success`, `ask_love`, `ask_funny`
- `emotion_stress`, `emotion_anxiety`, `emotion_sadness`, `emotion_lonely`, `emotion_failure`
- `ask_another`, `affirm`, `deny`, `thanks`, `bot_challenge`, `out_of_scope`, `nlu_fallback`

Regex patterns are also included for category/emotion keyword support.

## 8. Domain and Response Strategy
`domain.yml` defines:

- full intent list.
- response templates (`utter_*`) for quote categories and emotional support.
- fallback/out-of-scope responses.
- session behavior (`session_expiration_time: 60`).

Response strategy implemented:

- category-specific quote delivery.
- emotion-aware support lines.
- follow-up prompt (`utter_followup`) for continued engagement.
- positive/negative feedback branching using `affirm` and `deny`.

## 9. Conversation Control

### Stories (`data/stories.yml`)
Stories train multi-turn behavior, such as:

- stress support followed by motivation request.
- sadness support followed by humor and thanks.
- requesting another quote category.

### Rules (`data/rules.yml`)
Rules enforce deterministic behavior for:

- greeting, goodbye, and bot challenge.
- each quote category response.
- each emotion support response.
- fallback and out-of-scope handling.

## 10. NLU Pipeline and Policies
Configured in `config.yml`:

Pipeline components:

- `WhitespaceTokenizer`
- `RegexFeaturizer`
- `LexicalSyntacticFeaturizer`
- `CountVectorsFeaturizer` (word + character n-grams)
- `DIETClassifier` (intent classification)
- `EntitySynonymMapper`
- `ResponseSelector`
- `FallbackClassifier`

Policies:

- `MemoizationPolicy`
- `RulePolicy`
- `TEDPolicy`

This combination provides balanced deterministic behavior and learned dialogue generalization.

## 11. Training and Model Storage
Training command:

```bash
python -m rasa train
```

Training artifacts are stored in `models/` as timestamped archives (`.tar.gz`) and reused for runtime loading.

## 12. Testing and Validation

### Manual Testing

- performed via `python -m rasa shell` and via web UI.
- tested variations in wording for all major intents.
- validated response relevance and flow continuity.

### Automated Testing

- test stories in `tests/test_stories.yml`.
- includes stress support, motivation, and Hindi inspiration test paths.

### Web Health Validation

- Flask exposes `/health` endpoint.
- health response confirms if Rasa backend is online.

## 13. Deployment
The chatbot is deployed locally through:

1. Rasa API server (port `5005`)
2. Flask web app (port `8010` by default)

Key implementation points:

- `app.py` handles chat API requests and error states.
- `start_project.sh` auto-detects Python environments and starts both services.
- `stop_project.sh` terminates services and clears occupied ports.

## 14. Results and Observations
Observed outcomes:

- chatbot correctly handles quote and emotion intents in supported patterns.
- multilingual example inputs improve practical recognition coverage.
- web deployment gives better usability than CLI-only interaction.
- rule + story setup provides stable, predictable conversation behavior.

## 15. Social Impact
The system contributes to positive digital well-being by:

- providing 24/7 motivational and emotional support content.
- reducing effort required to find suitable uplifting messages.
- encouraging constructive thought patterns and emotional reflection.

## 16. Business Impact
The project demonstrates a practical conversational AI use case:

- personalized content recommendation via NLP.
- scalable architecture adaptable to wellness, education, support, and engagement scenarios.
- reduced manual effort in content discovery and user interaction.

## 17. Limitations
Current limitations include:

- responses are predefined (not dynamically fetched from external quote APIs).
- no user profile/history-based personalization yet.
- limited long-context memory beyond configured dialogue behavior.

## 18. Future Enhancements
Planned extensions:

- advanced sentiment/emotion detection models.
- ML-based personalized recommendations from user history.
- multilingual expansion beyond current examples.
- voice input/output integration.
- deployment on messaging platforms (WhatsApp/Telegram/etc.).
- dynamic quote retrieval using APIs/databases.
- feedback rating loop and analytics dashboard.
- cloud deployment for higher concurrency.

## 19. Conclusion
The Quotes Recommendation Chatbot successfully addresses the identified need for quick, interactive, and relevant motivational/emotional quote support. By combining Rasa NLU, structured dialogue design, and a Flask web interface, the project delivers a practical conversational system suitable for real-world extension and deployment.

## 20. References

- Rasa Documentation: https://rasa.com/docs/
- Flask Documentation: https://flask.palletsprojects.com/
- Python Documentation: https://docs.python.org/3/
