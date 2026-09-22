# ai-agent-learning
ai-agent-learning

                    AI Agent Developer
                           │
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
       LLM能力          Agent能力        工程能力
          │                │                │
     Prompt/Model      Tool Calling      API
     Structured       Agent Loop        FastAPI
     Output           Memory            Async
     Streaming        RAG               DB
     Context          Workflow          Docker
          │                │                │
          └────────────────┼────────────────┘
                           ↓
                    LangGraph
                           ↓
                  Production Agent
                  
# Day 01

## Learned

- Chat Model
- SystemMessage
- HumanMessage
- AIMessage
- invoke()
- stream()

## Project

CLI Streaming Chatbot

# Day 02

## Learned

- PromptTemplate
- ChatPromptTemplate
- System / Human Message
- prompt.invoke()
- prompt | model
- chain.invoke()
- 理解 Runnable / LCEL
- 完成 Python Tutor

# Day 03

## Learned

- Pydantic BaseModel
- Field
- with_structured_output()
- Structured Output
- ChatPromptTemplate + Structured Output
- prompt | structured_model
- 能拿 result.xxx
- 完成 Python Question Classifier

# Day 04

## Learned

- runnable_basic.py
- parallel.py
- tutor_chain.py
- interview_bot.py

# Day 05

## Learned

- stream_basic.py
- prompt_stream.py
- async_stream.py
- api.py

# Day 06

## Learned

- 知道 Trace 是什么
- 知道 Run 是什么
- 能配置 LangSmith
- 能看到一次 LLM 调用
- 能看到 Chain
- 能看到 Error
- 理解 Token Usage
- 理解 Latency
- 理解 Streaming vs Tracing
- 完成 Python Tutor

# Day 07

## Learned

- LLM Application Development

# Day 08

## Learned

Tool Calling 

- LLM → Tool Call
- Tool → Result
- Agent Loop

# Day 09

## Learned

- 独立设计一个 Agent Tool
- 使用 @tool
- 使用 Pydantic 定义参数
- 理解 Tool Schema
- 设计清晰的 Tool Description
- 处理 Tool 参数错误
- 处理 Tool 执行异常
- 编写多个 Tool
- 让 LLM 正确选择 Tool
- 理解什么样的函数不适合直接暴露给 Agent