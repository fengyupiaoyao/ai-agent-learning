# Research & Knowledge Agent

## 1. 项目目标

构建一个支持文档知识库检索、
自主研究、工具调用和报告生成的 AI Agent。

## 2. 核心功能

- 文档上传与解析
- 文档切分与向量索引
- 知识库语义检索
- 研究任务自动规划
- Agent 工具调用
- 证据汇总与引用溯源
- 研究报告生成
- SSE 流式响应
- 任务状态持久化

## 3. 技术栈

- Python
- LangChain
- LangGraph
- FastAPI
- Pydantic
- MCP
- PostgreSQL / pgvector
- Redis
- Docker
- pytest

## 4. 质量要求

- 模块化设计
- 可测试
- 可观测
- 支持异常恢复
- 支持权限控制
- 控制 Token 成本