# Smart-trade Multi-Agent LLM Financial Trading System

Smart-trade is a Python CLI application that provides a multi-agent research and trading platform. Specialized agents (market, sentiment, news, and fundamentals analysts) ingest and summarize data; researcher agents (bull/bear) synthesize viewpoints; trader agents propose trade plans; risk agents debate position sizing and limits; and a portfolio manager consolidates decisions into final trades and structured reports. The system is designed for researchers, algorithmic traders, and hackathon teams who want to experiment with LLM-driven workflows and rapid iteration.

Key strengths
- Multi-agent orchestration: clearly separated responsibilities for data ingestion, analysis, research, trading, risk, and portfolio management. The trading graph routes signals and outputs between components so each agent can focus on a small set of tasks.
- Local-first LLM usage and GPU optimizations: supports running smaller or quantized models locally, mixed precision (FP16), model offloading, and batch/streaming modes to maximize GPU utilization and reduce latency and cost when compared to repeated remote API calls.
- Performance and cost controls: prompt/result caching, vector storage (Chroma) for retrieval-augmented generation, asynchronous agent execution, staged processing to limit in-memory data, and optional Redis caching for persistence.
- Extensible dataflows: built-in integrations for yfinance, Finnhub, Tushare/Akshare, Reddit (praw), feedparser/news, and stockstats. Backtrader scaffolding is included for strategy testing.

Quick start
```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
./venv/Scripts/Activate.ps1

pip install -r requirements.txt
```

Run the CLI
```bash
cd cli
python main.py          # launches Typer + Rich CLI dashboard
python main.py --help   # see available commands and flags
```

Environment variables
Set keys and services you plan to use before running. Examples:
```bash
export GOOGLE_API_KEY="..."
export FINNHUB_API_KEY="..."
export OPENAI_API_KEY="..."     # if using OpenAI
export ANTHROPIC_API_KEY="..."  # if using Anthropic
# optional Redis
export REDIS_URL="redis://localhost:6379"
```

Project layout (top-level)
```
cli/                    Typer + Rich CLI and helpers
tradingagents/          core agent framework: graph, agents, dataflows
results/                generated reports and logs (results/<symbol>/<date>/reports)
assets/                 diagrams and CLI screenshots
README.md               quick start and overview
IMPLEMENTATION.md       (new) architecture and implementation details
```

How it runs (runtime shape)
- The CLI (cli/main.py) constructs and starts a trading graph defined in tradingagents/graph/trading_graph.py.
- Dataflows in tradingagents/dataflows/* fetch and pre-process market, news, and social data. Analysts consume this data and produce concise messages or signals.
- Signals are vectorized and cached (Chroma) and then routed across researchers, trader, and risk agents for deliberation. The portfolio manager consolidates final decisions and writes reports under results/.

Performance recommendations for local/GPU usage
- Prefer local or quantized models when doing many iterative runs to reduce API costs and latency.
- Use mixed precision (FP16) where supported and enable model offloading to move parts of the model between GPU and CPU to avoid GPU memory exhaustion.
- Batch or stream requests to the LLM where possible to increase throughput and reduce per-call overhead.
- Cache prompt results and reuse vector retrieval (Chroma) rather than reconstructing full contexts for repeated queries.
- Run agents asynchronously to overlap I/O and computation and use staged processing so only necessary datasets are loaded in memory.
- Add profiling hooks (see tradingagents/default_config.py and graph/setup.py) to measure GPU/CPU usage and tune model size, batch size, and offload configuration.

Outputs
- Reports and logs are written under `results/<symbol>/<date>/reports/` (market, sentiment, news, fundamentals, plans, and final decisions). Use these outputs for audit and post-analysis.

Development notes
- Python 3.10+ is required. The project is ready for local experimentation but does not include unit tests; adding tests for dataflows and agent logic is recommended.
- The CLI app is implemented with Typer and Rich for interactive dashboards. Agent orchestration uses a custom trading graph and leverages LangChain / LangGraph for LLM orchestration.

License
See `LICENSE` for details.
