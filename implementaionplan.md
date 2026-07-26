# Implementation Details — Smart-trade Multi-Agent LLM Financial Trading System

Overview
Smart-trade is implemented as a modular, CLI-driven multi-agent system in Python 3.10+. The runtime is a Typer + Rich CLI (cli/main.py) that builds and runs a trading graph (tradingagents/graph/trading_graph.py). Agents are small, focused components that exchange messages and signals; data ingestion and preprocessing are handled separately by dataflows under tradingagents/dataflows. Outputs are written to results/<symbol>/<date>/reports for audit and analysis.

Core components and responsibilities
- CLI (cli/main.py, cli/utils.py, cli/models.py)
  - User entry point. Builds configuration, starts runs, and displays a live dashboard with agent status and messages.
- Trading graph (tradingagents/graph/trading_graph.py)
  - Constructs nodes (agents) and edges (signal routing). Orchestration uses the graph to propagate signals and aggregate results.
  - Key modules: propagation.py (signal passing), conditional_logic.py (routing conditions), reflection.py (deliberation/feedback loops), signal_processing.py (transforms).
- Agents (tradingagents/agents/*)
  - Analysts: market, sentiment, news, fundamentals — fetch and summarize inputs from dataflows.
  - Researchers: bull/bear — synthesize analyst outputs and propose hypotheses.
  - Trader: constructs trade plans from researcher outputs.
  - Risk agents: evaluate sizing, constraints, and propose mitigations.
  - Portfolio manager: consolidates and finalizes decisions and writes reports.
- Dataflows (tradingagents/dataflows/*)
  - Interface (interface.py) provides unified adapters to data sources: yfinance, Finnhub, Tushare/Akshare, Reddit, news feeds, and stockstats.
  - Utilities implement scraping, rate-limit handling, parsing, and basic feature engineering (moving averages, indicators).
- Storage / caching / retrieval
  - Chroma vector store is used for retrieval-augmented generation and fast similarity lookups.
  - Optional Redis caching for persistence across runs and to avoid repeated expensive fetches.
  - Local cache under tradingagents/dataflows/data_cache for temporary artifacts.

LLM usage, local-first design, and GPU optimization
- Local-first: design supports running smaller or quantized LLMs locally to avoid API latency and cost for iterative workflows.
- Mixed precision (FP16): where supported by the model/runtime, use FP16 to reduce memory usage and increase throughput.
- Model offloading / CPU-GPU staging: configure the runtime to move parts of the model to CPU when GPU memory is limited. This allows larger models to run on constrained GPUs.
- Quantization and smaller models: use 4-bit/8-bit quantized models where accuracy trade-offs are acceptable for large-scale experimentation.
- Batching and streaming: group requests for similar prompts or stream long responses to reduce per-call overhead and perceived latency.
- Caching: cache LLM outputs for repeated prompts (prompt/result caching) and reuse vector retrievals rather than reconstructing full context each time.
- Async and parallel execution: agents are designed to run in parallel where possible (non-blocking I/O) so GPU and I/O overlap and pipeline utilization improves.
- Profiling hooks: integrate simple profiling (timing, GPU memory snapshots) at key points (graph start/end, LLM calls) to find bottlenecks and tune batch sizes, model precision, and offload thresholds.

Memory and latency reduction strategies
- Retrieval-augmented generation (Chroma): store and fetch concise contexts rather than including long histories in each prompt.
- Staged processing: load only necessary datasets per symbol and free memory as stages complete.
- Prompt trimming & summarization: keep prompts minimal using short summaries and stored embeddings.
- Worker sharding: divide symbol lists into shards to limit concurrent working set size.
- Redis-backed intermediate state: offload intermediate results to Redis when memory use would spike.
- Limit parallelism to hardware: set worker counts to match CPU/GPU resources to prevent thrashing.

Practical implementation pointers (files to inspect)
- cli/main.py — entry and command definitions.
- tradingagents/graph/trading_graph.py — graph construction and runner.
- tradingagents/graph/propagation.py — how signals are sent between agents.
- tradingagents/graph/reflection.py — agent deliberation and iterative feedback.
- tradingagents/dataflows/interface.py — adapters to yfinance, Finnhub, Reddit, and news.
- tradingagents/default_config.py — default runtime toggles and profiling hook points.

How to configure for local GPU runs
1. Install dependencies and a local model runtime that supports mixed precision and offloading.
2. Choose a quantized or small model for local experiments to reduce VRAM needs.
3. Set environment variables for provider keys only if needed; prefer local LLM endpoints for heavy runs.
4. Tune default_config.py:
   - set model precision to fp16 when available
   - enable model offloading thresholds
   - set batch sizes for LLM calls
   - configure Redis URL only if persistence across runs is required
5. Use the profiling hooks to measure end-to-end latency and per-call GPU memory and adjust config.

Outputs and observability
- Reports: results/<symbol>/<date>/reports/ — per-symbol, per-run structured outputs (market, sentiment, news, plans, decisions).
- Logs: CLI dashboard shows live agent messages; persistent logs are written to results/ for auditing.
- Metrics: basic timing and memory measurements available via profiling hooks; add more detailed telemetry (Prometheus/Grafana) if operating at scale.

Extensibility
- Add new agents by creating a focused module in tradingagents/agents and connecting it in trading_graph.py.
- Add a new data source by implementing an adapter in tradingagents/dataflows and wiring it into interface.py.
- Replace or add vector stores / LLM backends with minimal changes to the agent logic; keep model-specific code isolated.

Notes and recommended next steps
- Add unit tests for dataflows and agent logic to increase reliability.
- Add a small example run in the repo that produces a single-symbol report (helps hackathon judges reproduce results quickly).
- Include an example config for a local quantized model and a short guide to measure GPU usage during a run.
