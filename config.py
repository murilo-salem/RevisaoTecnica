"""
Configurações do Agente de Web Scraping de Patentes.
"""

import os

# --- Ollama ---
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:27b")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "600"))  # segundos
OLLAMA_MAX_FAILURES_BEFORE_DEGRADE = 3
OLLAMA_HEALTHCHECK_PROMPT = 'Responda apenas com {"status":"ok"}'
SCREEN_INCLUDE_THRESHOLD = 7.0
SCREEN_REVIEW_THRESHOLD = 4.5
SCREEN_RERANK_MIN_SCORE = 5.5
SCREEN_RERANK_MAX_SCORE = 8.0
SCREEN_MAX_ITEMS_FOR_REVIEW = 20
WHITESPACE_MAX_ADJACENT = 3
REVIEW_PROTOCOL_VERSION = "1.0"
MEMORY_SLOT_MAX_ITEMS = 5
ENABLE_LLM_CACHE = True
ROUTER_PRIORITY_CLUSTERS = [
    "CO2 Cycle Configurations",
    "Cryogenic Energy Systems",
    "Phase Change Materials",
    "Thermal Transfer Mechanisms",
    "Economic Optimization",
]

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

# --- EPO Open Patent Services ---
EPO_CONSUMER_KEY = os.getenv("EPO_CONSUMER_KEY", "")
EPO_CONSUMER_SECRET = os.getenv("EPO_CONSUMER_SECRET", "")

# --- Pipeline de Análise de Artigo ---
OLLAMA_EXTRACTION_MODEL = os.getenv("OLLAMA_EXTRACTION_MODEL", "gemma3:12b")
ARTICLE_MAX_SEARCH_QUERIES = int(os.getenv("ARTICLE_MAX_SEARCH_QUERIES", "4"))
ARTICLE_MAX_RESULTS_PER_QUERY = int(os.getenv("ARTICLE_MAX_RESULTS_PER_QUERY", "5"))
ARTICLE_TEXT_MAX_CHARS = 15000

# --- Output ---
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
LLM_CACHE_DIR = os.path.join(OUTPUT_DIR, "cache")

# --- PatentScope ---
PATENTSCOPE_BASE_URL = "https://patentscope.wipo.int/search/en"
PATENTSCOPE_PAGE_SIZE = 50
PATENTSCOPE_DETAIL_DELAY = (3.0, 6.0)
PATENTSCOPE_SEARCH_DELAY = (1.5, 3.0)
