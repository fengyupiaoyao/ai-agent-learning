# System Architecture

## 1. Architecture

Client
  |
FastAPI
  |
ResearchService
  |
Research Agent (LangGraph)
  |
  +-- Planner
  +-- Retriever
  +-- Researcher
  +-- Writer
  |
  +-- LLM
  +-- Knowledge Base
  +-- MCP Tools
  +-- External APIs

## 2. Layer Responsibilities

### API Layer
处理 HTTP 请求和 SSE 响应。

### Service Layer
负责任务编排和业务逻辑。

### Agent Layer
负责规划、决策和工具调用。

### Knowledge Layer
负责文档处理和知识检索。

### Tools Layer
提供 MCP 和外部工具。

### Infrastructure Layer
负责配置、日志、数据库和测试。

## 3. Data Flow

User Request
  -> Planner
  -> Retriever
  -> Researcher
  -> Evidence Aggregation
  -> Writer
  -> Final Report

## 4. Reliability

- Timeout
- Retry
- Checkpoint
- Logging
- Token Budget
- Permission Control