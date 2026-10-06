# Web Reader

Web Reader is a local FastAPI service and Chrome extension that lets you ask
grounded questions about the active web page.

## Run locally

```powershell
cd server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r ..\requirements.txt
$env:OPENAI_API_KEY = "your-api-key"
# Optional: $env:OPENAI_MODEL = "gpt-4o-mini"
python main.py
```

The API listens on `http://127.0.0.1:8000`. Confirm it is running at
`http://127.0.0.1:8000/health`.

## Install the extension

1. Open `chrome://extensions` and enable **Developer mode**.
2. Select **Load unpacked**.
3. Choose the `extension` folder.
4. Open an `http` or `https` page, click the extension, and ask a question.

The extension calls only the local API. The API fetches the active page,
extracts readable HTML text, and asks the configured model to answer from that
text. It reports a clear error if the server is unavailable, the page is not
HTML, or `OPENAI_API_KEY` is missing.

## Security

Never put API keys in source files or the extension. Set `OPENAI_API_KEY` in
your local environment or a secret manager, and rotate any key that was ever
committed to Git history.
