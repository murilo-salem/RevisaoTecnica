"""
Configurações do Agente de Web Scraping de Patentes.
"""

# --- Ollama ---
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "gemma3:4b"
OLLAMA_TIMEOUT = 600  # segundos

# --- Scraper ---
MAX_RESULTS = 10
REQUEST_TIMEOUT = 30  # segundos
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # segundos (backoff exponencial)

# --- User Agents rotativos ---
USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

# --- Google Patents ---
GOOGLE_PATENTS_BASE_URL = "https://patents.google.com"
GOOGLE_PATENTS_SEARCH_URL = f"{GOOGLE_PATENTS_BASE_URL}/xhr/query"

# --- Output ---
OUTPUT_DIR = "output"
