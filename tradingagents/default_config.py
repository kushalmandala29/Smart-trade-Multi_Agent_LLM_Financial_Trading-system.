import os
from dotenv import load_dotenv
load_dotenv()

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    # Data directories: prefer repository `dataflows/data_cache` so offline tools find expected CSVs
    "data_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings
    "llm_provider": "Gemini",
    "deep_think_llm": "gemini-2.0-flash",
    "quick_think_llm": "gemini-2.0-flash",
    "backend_url": "https://generativelanguage.googleapis.com/v1beta",
    "google_api_key": os.getenv("GOOGLE_API_KEY"),
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # Tool settings
    "online_tools": True,
}
