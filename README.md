# AI Image Studio — Grok + Groq

A beginner-friendly Streamlit project with two independent AI features:

1. **Text to Image (Grok / xAI):** enter a text prompt and generate an image using Grok Imagine.
2. **Image to Description (Groq):** upload a PNG/JPG/WEBP image and ask a Groq vision model to describe it.

## Project structure

```text
ai_image_studio/
├── app.py
├── services/
│   ├── __init__.py
│   ├── image_generator.py
│   └── image_describer.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 1. Get the API keys

- Create an xAI API key: https://console.x.ai/
- Create a Groq API key: https://console.groq.com/keys

The two keys are separate. Image generation through xAI may be paid; check current pricing and account access before using it. Groq model availability and limits depend on your account.

## 2. Open the project in VS Code

Extract the ZIP file, open the `ai_image_studio` folder in VS Code, then open its terminal.

## 3. Create and activate a virtual environment (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 4. Install packages

```powershell
pip install -r requirements.txt
```

## 5. Add API keys

Copy `.env.example` and rename the copy to `.env`.

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace the placeholder values with your real API keys. Never share this file or upload it to GitHub.

## 6. Run the application

```powershell
streamlit run app.py
```

Streamlit will open the app in your browser.

## How the code is organized

- `app.py`: creates the Streamlit interface, tabs, upload control, and buttons.
- `services/image_generator.py`: sends the user's text prompt to the xAI image-generation API.
- `services/image_describer.py`: converts the uploaded image into Base64 and sends it to Groq's vision model.
- `.env`: stores secret API keys locally (not included in this ZIP).
- `requirements.txt`: lists the Python packages needed by the project.

## Important notes

- The xAI image API returns a temporary image URL. Open or save the generated image soon if you need to keep it.
- API calls require internet access and valid API keys. They are not simulated in this project.
- API pricing, model availability, rate limits, and access can change. Check the providers' current dashboards.
- If Groq reports that the selected model is unavailable for your account, check the current vision model IDs in https://console.groq.com/docs/vision and update `GROQ_VISION_MODEL` in `.env`.
- Do not commit `.env` to GitHub.
