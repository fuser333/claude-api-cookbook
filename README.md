# Claude API Cookbook

Working code examples and patterns from **Anthropic Academy · "Building with the Claude API"** course, plus real-world production patterns from running Claude at scale in Latin America.

**Built by [Héctor Velasco](https://www.linkedin.com/in/hectorvelasco)** · CEO [H3L Consulting](https://diagnostico.h3l.ai) · Quito, Ecuador
**Course:** https://anthropic.skilljar.com/building-with-the-claude-api
**Certificate:** Anthropic Academy · Building with the Claude API · May 2026

---

## 🎯 What's inside

14 standalone examples. Each runs in under 30 seconds with `uv`. No build steps. No magic.

| Folder | What it teaches | Run it with |
|--------|-----------------|-------------|
| `app_starter` | Minimal Claude API setup with `uv` + dotenv | `uv run python app.py` |
| `system_prompts` | Top-level `system` parameter for persistent role | `uv run python exercise.py` |
| `chatbot` | Multi-turn conversation with stateless API + history array | `uv run python chatbot.py` |
| `structured_output` | Prefilling + `stop_sequences` for clean JSON | `uv run python exercise.py` |
| `tool_use` | Function calling, agentic loops, `stop_reason` handling | `uv run python exercise.py` |
| `built_in_tools` | Web search, text editor, code execution from Anthropic | `uv run python exercise.py` |
| `multimodal_images` | Image input via base64 + URL + asset_id | `uv run python exercise.py` |
| `pdf_processing` | Native PDF input (no preprocessing needed) | `uv run python exercise.py` |
| `prompt_caching` | `cache_control` for 90% cost reduction on repeated context | `uv run python exercise.py` |
| `citations` | Auditable `char_location` + `page_location` citations | `uv run python exercise.py` |
| `chunking_rag` | Document chunking + hybrid BM25 + vector retrieval | `uv run python exercise.py` |
| `prompt_evals` | Dataset generation with Haiku + model grader pattern | `uv run python exercise.py` |
| `prompting_with_evaluator` | Iterative prompt refinement via automated grading | `uv run python exercise.py` |
| `cli_capstone_project` | Final project: CLI app with all patterns combined | See folder README |

---

## 🚀 Quick start

```bash
# 1. Clone
git clone https://github.com/fuser333/claude-api-cookbook.git
cd claude-api-cookbook

# 2. Get your Anthropic API key
# → https://console.anthropic.com/settings/keys

# 3. Pick any folder and run
cd chatbot
export ANTHROPIC_API_KEY="sk-ant-..."
uv run python chatbot.py
```

> **Note:** `.env` files were stripped before publishing. Each example expects `ANTHROPIC_API_KEY` exported in your shell or in a local `.env` you create yourself.

---

## 💡 Key concepts (cheat sheet)

```python
# Minimum required API call
client.messages.create(
    model="claude-sonnet-4-5",   # OBLIGATORY
    max_tokens=1024,              # OBLIGATORY (unlike OpenAI)
    messages=[{"role": "user", "content": "..."}],
)
```

| Pattern | Use case | Temperature |
|---------|----------|-------------|
| Factual Q&A, classification | Deterministic output | **0.0 - 0.2** |
| Technical analysis, code | Stable + creative | 0.0 - 0.3 |
| Natural conversation | Friendly tone | 0.5 - 0.7 |
| Brainstorming, creative writing | Diverse output | 0.7 - 1.0 |

```python
# Stateless multi-turn (you must send ALL history every request)
messages = [
    {"role": "user", "content": "What's 2+2?"},
    {"role": "assistant", "content": "4"},
    {"role": "user", "content": "Now multiply by 3"},  # Claude sees the full history
]
```

```python
# Clean JSON output via prefill + stop_sequences
add_assistant_message(messages, "{")
text = chat(messages, stop_sequences=["}"])
raw_json = "{" + text + "}"
```

```python
# Streaming for better perceived latency (time-to-first-token drops ~95%)
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

---

## 🏗️ Real production usage at H3L Consulting

These patterns power live SaaS products in Latin America:

| Pattern from this cookbook | Where it runs in production |
|---------------------------|----------------------------|
| `system_prompts` | Auditor role at `diagnostico.h3l.ai` |
| `chatbot` multi-turn | 15-minute deep audit at `profundiza.h3l.ai` |
| Streaming | `profundiza.h3l.ai` for live token rendering |
| `structured_output` | JSON report generation for SRI tax declarations |
| Temperature 0.0 | Classification of 28 operational waste types |
| Haiku for volume | Bulk classification of 332,460 Ecuadorian companies |
| `prompt_evals` | Frozen golden dataset for the auditor agent (in progress) |
| API key security | All keys server-side in `.env` + `.gitignore` |

---

## 🌎 Why this matters for LATAM builders

Most Claude tutorials assume English-speaking users with US infrastructure. This cookbook was written from Quito, deployed to cPanel servers in Latin America, and tested with Spanish-language audit reports running on Anthropic models.

If you're building with Claude from anywhere in Latin America and want to talk shop, find me on LinkedIn.

---

## 📜 License

MIT — use, fork, modify, ship.

Course material referenced here belongs to Anthropic Academy. The code examples in each folder were written following the course exercises and are shared here as study notes + working snippets.

---

## 🔗 Links

- **Anthropic Academy:** https://anthropic.skilljar.com/
- **Anthropic Console:** https://console.anthropic.com/
- **Claude API docs:** https://docs.anthropic.com/
- **H3L Consulting:** https://diagnostico.h3l.ai
- **My MCP cookbook:** https://github.com/fuser333/mcp-advanced-demos

---

*Published as part of my Anthropic Academy certification path. 4 of 18 courses completed · the journey continues.*
