# Deep Research

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![Anthropic](https://img.shields.io/badge/AI-Anthropic_|_OpenAI_|_DeepSeek-8A2BE2?logo=openai&logoColor=white)](#)
[![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)

AI-powered research assistant that searches multiple platforms, synthesizes findings with Claude, and generates comprehensive research reports.

[中文文档](./README_CN.md)

## Features

- **Multi-source search**: arXiv, Semantic Scholar, Reddit, Twitter/X, Xiaohongshu, and web search
- **AI synthesis**: Claude API with extended thinking analyzes results and produces structured reports
- **Real-time progress**: Watch search → dedup → analyze → generate phases live via SSE
- **Multiple output formats**: Markdown, LaTeX, and PDF
- **Plugin architecture**: Add new search sources without modifying core code

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- [pandoc](https://pandoc.org/installing.html) (for PDF output)
- An Anthropic API key

### Setup

```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Set your Anthropic API key
cp .env.example .env
# Edit .env and fill in ANTHROPIC_API_KEY

# Install frontend dependencies
cd ../frontend
npm install
```

### Run

```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8765 --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

Open http://localhost:5173 in your browser.

## How It Works

1. **Enter a research topic** (e.g., "diffusion models for protein design")
2. **Select search sources** — toggle which platforms to query
3. **Watch progress** — real-time SSE stream shows each phase
4. **Read the report** — structured results with summary, hotspots, timeline, innovations, debates, and more
5. **Download** — export as Markdown, LaTeX, or PDF

## Architecture

```
frontend (React + Vite + Tailwind CSS)
    ↕ REST + SSE
backend (FastAPI + aiohttp + asyncio)
    ├── plugins/        ← Search sources (plug-and-play)
    ├── services/       ← Search, dedup, analyze, generate
    ├── output/         ← Markdown/LaTeX/PDF rendering
    └── api/            ← HTTP routes
database (aiosqlite)
```

### Search Sources

| Source | Category | Reliability | Auth Required |
|--------|----------|-------------|---------------|
| arXiv | Academic | High | No |
| Semantic Scholar | Academic | High | No |
| Reddit | Social | Medium | No |
| Web Search | Web | Medium | No |
| Twitter / X | Social | Low (experimental) | No |
| Xiaohongshu | Social | Low (experimental) | No |

### Adding a New Source

Create a file in `backend/app/plugins/` that extends `SearchPlugin`:

```python
from app.plugins.base import SearchPlugin, SearchResult, PluginInfo

class MyPlugin(SearchPlugin):
    @property
    def info(self) -> PluginInfo:
        return PluginInfo(name="my_source", display_name="My Source",
                          description="...", category="academic")

    async def search(self, query: str, limit: int = 20) -> list[SearchResult]:
        results = []
        # Your search logic here
        return results
```

The plugin is auto-discovered on startup. No other changes needed.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/research` | Start a research task |
| GET | `/api/research/{id}` | Get task status and results |
| GET | `/api/research/{id}/stream` | SSE progress stream |
| GET | `/api/research/history` | List past tasks |
| DELETE | `/api/research/{id}` | Delete a task |
| GET | `/api/research/{id}/output.{md,tex,pdf}` | Download output |
| GET | `/api/plugins` | List available plugins |
| PUT | `/api/plugins/{name}/config` | Configure a plugin |
| GET | `/api/health` | Health check |

## Configuration

All settings via environment variables or `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | — | **Required** — Your Anthropic API key |
| `ANTHROPIC_MODEL` | `claude-sonnet-4-6-20250514` | Claude model to use |
| `ANTHROPIC_MAX_TOKENS` | `64000` | Max output tokens |
| `ANTHROPIC_THINKING_BUDGET` | `16000` | Extended thinking budget |
| `SEARCH_LIMIT_PER_SOURCE` | `20` | Max results per source |
| `SEARCH_TIMEOUT_SECONDS` | `60` | Per-source timeout |
| `REDDIT_CLIENT_ID` | — | Reddit API client ID (optional) |
| `REDDIT_CLIENT_SECRET` | — | Reddit API secret (optional) |

## Project Structure

```
deep-research/
├── backend/
│   ├── app/
│   │   ├── api/          # HTTP routes
│   │   ├── core/         # Cache, exceptions
│   │   ├── models/       # Pydantic schemas
│   │   ├── output/       # MD/TeX/PDF renderers + templates
│   │   ├── plugins/      # Search source plugins
│   │   └── services/     # Business logic
│   └── tests/
├── frontend/
│   └── src/
│       ├── components/   # Reusable UI components
│       ├── hooks/        # Custom React hooks
│       ├── lib/          # API client, types
│       └── pages/        # Route pages
└── Makefile
```
