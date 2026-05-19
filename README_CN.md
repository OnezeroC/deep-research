# Deep Research

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![AI](https://img.shields.io/badge/AI-Anthropic_|_OpenAI_|_DeepSeek-8A2BE2?logo=openai&logoColor=white)](#)
[![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)

AI 驱动的科研助手，输入研究方向后自动检索多个平台，综合分析和总结研究热点、创新点及历史发展，生成结构化科研报告。

[English](./README.md)

## 功能特点

- **多源检索**：arXiv、Semantic Scholar、Reddit、Twitter/X、小红书、网页搜索
- **AI 综合分析**：支持 Anthropic / OpenAI / DeepSeek / 本地模型，生成深度结构化报告
- **实时进度**：SSE 流式推送，实时展示搜索 → 去重 → 分析 → 生成全流程
- **多格式输出**：Markdown、LaTeX、PDF
- **插件架构**：新增搜索源无需修改核心代码

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- [pandoc](https://pandoc.org/installing.html)（PDF 输出需要）
- 至少一个 AI 服务的 API Key

### 安装

```bash
cd deep-research
make install
```

### 运行

```bash
# 终端 1：启动后端（端口 8765）
make dev-backend

# 终端 2：启动前端（端口 5173）
make dev-frontend
```

打开浏览器访问 `http://localhost:5173`。

## 使用流程

1. **输入研究方向**（如 `"transformer attention mechanism survey"` 或 `"大语言模型推理能力"`）
2. **选择搜索来源** — 勾选需要的平台
3. **点击 Analyze** — 实时进度展示
4. **查看报告** — 包含摘要、热点、时间线、创新点、争议、趋势、研究缺口等
5. **下载导出** — Markdown / LaTeX / PDF

## AI 提供商配置

在 `backend/.env` 中配置：

```bash
# 方案一：Anthropic Claude
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-你的密钥

# 方案二：OpenAI
AI_PROVIDER=openai
OPENAI_API_KEY=sk-你的密钥

# 方案三：DeepSeek
AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-你的密钥

# 方案四：本地模型（Ollama / vLLM / LM Studio）
AI_PROVIDER=openai_compatible
OPENAI_COMPATIBLE_BASE_URL=http://localhost:11434/v1
OPENAI_COMPATIBLE_MODEL=llama3
```

## 项目结构

```
deep-research/
├── backend/                  # Python FastAPI 后端
│   └── app/
│       ├── api/              # HTTP 路由
│       ├── plugins/          # 搜索源插件（自动发现）
│       ├── providers/        # AI 提供商后端
│       ├── services/         # 业务逻辑
│       ├── output/           # MD/TeX/PDF 渲染器
│       └── models/           # 数据模型
├── frontend/                 # React 前端
│   └── src/
│       ├── components/       # UI 组件
│       ├── pages/            # 页面
│       ├── hooks/            # 自定义 Hooks
│       └── lib/              # API 客户端、类型
└── README.md
```

## 搜索源

| 来源 | 类型 | 可靠性 | 需要认证 |
|------|------|--------|----------|
| arXiv | 学术 | 高 | 否 |
| Semantic Scholar | 学术 | 高 | 否 |
| Reddit | 社交 | 中 | 否 |
| Web Search | 网页 | 中 | 否 |
| Twitter / X | 社交 | 低（实验性） | 否 |
| 小红书 | 社交 | 低（实验性） | 否 |

## 新增搜索源

在 `backend/app/plugins/` 下创建文件，继承 `SearchPlugin`：

```python
from app.plugins.base import SearchPlugin, SearchResult, PluginInfo

class MyPlugin(SearchPlugin):
    @property
    def info(self):
        return PluginInfo(name="my_source", display_name="我的来源",
                          description="...", category="academic")

    async def search(self, query: str, limit: int = 20):
        results = []
        # 在此实现搜索逻辑
        return results
```

插件会自动发现和加载，无需修改其他代码。

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/research` | 创建研究任务 |
| GET | `/api/research/{id}` | 获取任务状态和结果 |
| GET | `/api/research/{id}/stream` | SSE 实时进度 |
| GET | `/api/research/history` | 历史任务列表 |
| DELETE | `/api/research/{id}` | 删除任务 |
| GET | `/api/research/{id}/output.{md,tex,pdf}` | 下载导出文件 |
| GET | `/api/plugins` | 列出搜索源 |
| PUT | `/api/plugins/{name}/config` | 配置搜索源 |
| GET | `/api/health` | 健康检查 |

## 配置项

全部通过 `backend/.env` 环境变量配置：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `AI_PROVIDER` | `anthropic` | AI 提供商 |
| `ANTHROPIC_API_KEY` | — | Anthropic API Key |
| `OPENAI_API_KEY` | — | OpenAI API Key |
| `DEEPSEEK_API_KEY` | — | DeepSeek API Key |
| `ANTHROPIC_MODEL` | `claude-sonnet-4-6-20250514` | Claude 模型 |
| `OPENAI_MODEL` | `gpt-4.1` | OpenAI 模型 |
| `DEEPSEEK_MODEL` | `deepseek-chat` | DeepSeek 模型 |
| `SEARCH_LIMIT_PER_SOURCE` | `20` | 每个来源最大结果数 |
| `SEARCH_TIMEOUT_SECONDS` | `60` | 单来源搜索超时 |

## 许可证

MIT
