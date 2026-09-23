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

# Day 10

## Learned

-Agent Loop / Tool Execution Orchestration

# Day 11

## Learned

- 使用 LangChain create_agent()
- 给 Agent 注册多个 Tool
- 理解 Agent 的输入输出
- 理解 Agent 如何自动调用 Tool
- 理解 Agent Loop 与 create_agent 的关系
- 使用 system prompt
- 使用 Agent State 的基础能力
- 使用 streaming
- 使用 LangSmith 观察 Agent
- 对比“手写 Agent”和“LangChain Agent”

# Day 12

## Learned

## 1. What is a Tool?

A Tool is a function that an Agent can call.

## 2. Tool Calling Flow

User
↓
LLM
↓
Tool Call
↓
Tool Execution
↓
Tool Result
↓
LLM
↓
Final Answer

## 3. Tool Structure

A Tool contains:

- name
- description
- input schema
- function
- output

## 4. Important Insight

The LLM does not directly execute Python code.

The LLM decides:

- which tool to call
- what arguments to provide

The application executes the tool.

## 5. Tool Design Principles

- Clear tool name
- Clear description
- Strong type hints
- Small responsibilities
- Predictable output

# Day 13

## Learned

## 1. Agent Loop

Agent repeatedly performs:

LLM
↓
Decision
↓
Tool Call
↓
Tool Result
↓
LLM
↓
Decision
↓
...

## 2. ReAct

ReAct can be understood as:

Reasoning
+
Acting

The important engineering concept is:

Decision
↓
Action
↓
Observation
↓
Decision

## 3. Workflow vs Agent

Workflow:

A → B → C → D

The developer defines the execution path.

Agent:

LLM → Tool A
    → Tool B
    → Tool C

The LLM dynamically decides the next action.

## 4. Message Flow

HumanMessage
↓
AIMessage
↓
ToolMessage
↓
AIMessage
↓
ToolMessage
↓
AIMessage

## 5. Key Insight

The core of an Agent is not simply having tools.

The core is:

LLM-driven dynamic decision making
+
Tool execution
+
Iteration

# Day 14

## Learned Agent State & Memory

## 1. Message History

Message History stores previous conversation messages.

## 2. State

State contains the data required by an Agent during execution.

Example:

State
├── messages
├── current_task
├── tool_results
└── other runtime data

## 3. Memory

Memory allows an Agent to retain and reuse information from previous interactions.

## 4. Thread

A thread represents an independent conversation/execution context.

## 5. Checkpointer

A checkpointer stores Agent state so it can be restored later.

## 6. thread_id

thread_id identifies a conversation/thread.

Different thread_ids should have independent state.

## 7. Important Difference

State:
Current runtime data.

Message History:
Conversation messages.

Memory:
Mechanism for retaining/reusing past information.

## 8. Key Insight

Agent
+
State
+
Persistence
=
Stateful Agent