# CivicSathi AI

**Government schemes made simple.** CivicSathi AI is a Streamlit MVP that helps people explore Indian government scheme information in plain English, review common documents, and find official portals.

> CivicSathi is an independent informational tool, not a government website or application submission service. Rules change; always verify details with the linked authority.

## Problem and solution
Citizens can find scheme rules hard to navigate. CivicSathi brings six starter guides into one searchable dashboard and offers a cautious Q&A experience grounded in those guides.

## Features
- Searchable scheme cards for PM-KISAN, Ayushman Bharat PM-JAY, National Scholarship Portal, Karnataka SSP, PMUY and MGNREGA.
- Eligibility checker with preliminary-only language and official next steps.
- Common document guide.
- Chat assistant powered by Gemini when configured, otherwise local knowledge-base fallback.
- Responsive custom-styled Streamlit interface; no account or personal data storage.

## Stack and architecture
Python 3, Streamlit, Google Gen AI SDK, JSON, optional environment configuration.

- `app.py`: navigation and UI
- `data/schemes.json`: editable starter knowledge base
- `utils/scheme_manager.py`: data loading and search
- `utils/eligibility.py`: cautious preliminary rules
- `utils/ai_assistant.py`: Gemini integration and local fallback
- `assets/style.css`: interface styling

## Run locally
Use Python 3.10 or newer.

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app works without an API key. To enable Gemini, copy `.env.example` to `.env`, set `GEMINI_API_KEY`, then load it in your shell or configure it as a Streamlit secret. For example, PowerShell: `$env:GEMINI_API_KEY="your-key"`. Never commit secrets.

For Streamlit secrets, create `.streamlit/secrets.toml` locally with `GEMINI_API_KEY = "your-key"`; add the same key under the app's Secrets settings after deployment. `.gitignore` excludes the local secrets file.

## Deploy to Streamlit Community Cloud
1. Push this folder to a GitHub repository (see commands below).
2. In Streamlit Community Cloud, choose **Create app**, select the repository, branch, and `app.py`.
3. Deploy. Add `GEMINI_API_KEY` under **App settings → Secrets** if Gemini is desired; otherwise the local fallback runs.

## Upload to GitHub
Create an empty repository named `CivicSathi-AI` in [your GitHub account](https://github.com/shri-Nxtdev), then run these commands in this project folder:

```bash
git init
git add .
git commit -m "Build CivicSathi AI MVP"
git branch -M main
git remote add origin https://github.com/shri-Nxtdev/CivicSathi-AI.git
git push -u origin main
```

## Limitations
The dataset is a concise demonstration guide, not an exhaustive or live government database. Some scheme criteria, benefits and application routes are state- and year-specific. The eligibility checker does not make official decisions. Gemini output is constrained by supplied context but should still be verified. The app does not submit applications or collect/store personal information.

## Future improvements
Add source review dates and citations per field, multilingual answers, official data refresh workflows, fuller state scheme coverage, and a more comprehensive rules-based eligibility engine.
