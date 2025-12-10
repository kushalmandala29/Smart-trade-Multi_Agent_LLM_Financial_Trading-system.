Smart-trade Multi-Agent LLM Financial Trading System
===================================================

A multi-agent, LLM-driven research and trading framework that coordinates analyst, research, trading, risk, and portfolio teams to generate market analysis, trade plans, and final portfolio decisions. The CLI provides an interactive, Rich-powered terminal experience to monitor agent progress and view generated reports.

Features
--------
- Multi-agent pipeline: market, sentiment, news, and fundamentals analysts feed bull/bear researchers, trader, risk debators, and portfolio manager.
- Rich CLI dashboard: live progress, agent statuses, messages, and rendered report sections.
- Data integrations: yfinance, Finnhub, Akshare/Tushare, Reddit (praw), feedparser/news, stockstats, backtrader scaffolding.
- LLM tooling: LangChain (OpenAI, Anthropic, Google GenAI), LangGraph orchestration, Chroma vector storage.
- Caching and storage: Redis support for persistence, local data cache under `tradingagents/dataflows/data_cache`.

Requirements
------------
- Python 3.10+
- Recommended: virtual environment
- Optional services: Redis (if you enable caching), API keys for OpenAI/Anthropic/Google GenAI/Finnhub/Tushare/Akshare as needed

Setup
-----
```powershell
# from repo root
python -m venv venv
./venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

Environment variables
---------------------
Set what you need before running. Common examples:
```powershell
$env:OPENAI_API_KEY="..."
$env:ANTHROPIC_API_KEY="..."
$env:GOOGLE_API_KEY="..."
$env:FINNHUB_API_KEY="..."
$env:TUSHARE_TOKEN="..."
$env:REDIS_URL="redis://localhost:6379"  # if using Redis
```

Quick start (CLI)
-----------------
```powershell
cd cli
python main.py
```

Command-line options
--------------------
The Typer app is defined in `cli/main.py`. Run `python main.py --help` for available commands/flags (shell completion is enabled by Typer).

Project layout
--------------
- `cli/` – Rich/typer CLI, models, helpers, welcome banner
- `tradingagents/graph/` – agent graph orchestration and signal processing
- `tradingagents/agents/` – analysts, researchers, trader, risk debators, managers
- `tradingagents/dataflows/` – data ingestion (yfinance, Finnhub, news/reddit, stock stats), config, cache
- `results/` – generated reports and logs grouped by symbol/date
- `assets/` – diagrams and CLI screenshots

Outputs
-------
- Reports and logs are written under `results/<symbol>/<date>/reports/` (market, sentiment, news, fundamentals, plans, final decisions).

Architecture (high level)
--------------------------
![Architecture diagram](assets/WhatsApp%20Image%202025-11-26%20at%2012.23.54.jpeg)

The diagram shows the CLI (Typer + Rich) driving the TradingAgents graph, which orchestrates analyst teams (market/sentiment/news/fundamentals), bull/bear researchers, trader, risk debators, and portfolio manager, all fed by external data sources (yfinance, Finnhub, Akshare/Tushare, Reddit/news/feeds, stock stats). Outputs flow into reports and final portfolio decisions.

Development
-----------
- Lint/format: not configured; you can add Ruff/Black/Flake8 if desired.
- Tests: none committed; recommended to add unit tests for dataflows and agent logic.

License
-------
See `LICENSE` for details.
