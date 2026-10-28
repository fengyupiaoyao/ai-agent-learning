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

# Day 15

## Learned Structured Output

## 1. Structured Output

Structured Output makes LLM responses conform to a predefined schema.

## 2. Pydantic

Pydantic provides:

- Data validation
- Type definitions
- Schema generation
- Structured Python objects

## 3. Schema

A schema defines:

- Field names
- Field types
- Field descriptions
- Allowed values

## 4. Structured Output vs Tool Calling

Structured Output:

LLM
↓
Structured Data

Tool Calling:

LLM
↓
Tool
↓
Tool Result

## 5. LLM Router

LLM
↓
Structured Output
↓
Intent
↓
Python Router
↓
Tool

## 6. Key Engineering Principle

Use LLM for language understanding.

Use deterministic code for business logic.

# Day 16

## Learned 实战

AI Agent
│
├── Model
│
├── Prompt
│
├── Tool
│
├── Tool Calling
│
├── Agent Loop
│
├── State
│
├── Conversation History
│
├── Memory
│
└── Structured Output
      │
      └── Pydantic

最终形成：

                 ┌──────────────┐
                 │     User     │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │    Agent     │
                 └──────┬───────┘
                        ↓
               ┌─────────────────┐
               │       LLM       │
               └────────┬────────┘
                        ↓
                 Need a Tool?
                   /       \
                 Yes        No
                  ↓          ↓
                Tool       Answer
                  ↓
             Tool Result
                  ↓
                 LLM
                  ↓
        Structured Output
                  ↓
          ResearchResult

# Day 17

## Learned RAG

基础
 创建 Document
 理解 page_content
 理解 metadata
Loader
 TextLoader
 Markdown Loader
 PyPDFLoader
 DirectoryLoader
实战
 加载 TXT
 加载 Markdown
 加载 PDF
 批量加载 Markdown
 打印 metadata
 统计 Document 数量
理解
 Loader 是干什么的？
 Loader 和 Splitter 有什么区别？
 为什么 PDF 通常会产生多个 Document？
 metadata 为什么对 RAG 很重要？

# Day 18

## Learned RAG Split

理论
 为什么需要 Chunking
 什么是 Chunk
 什么是 chunk_size
 什么是 chunk_overlap
 为什么需要 overlap
 Loader 和 Splitter 的区别
 split_text() 和 split_documents() 的区别
Coding
 RecursiveCharacterTextSplitter
 split_text()
 split_documents()
 TXT → Document → Chunk
 Markdown → Document → Chunk
 保留 metadata
 对比不同 chunk_size
 对比不同 overlap

# Day 19

## Learned RAG

Embedding Model
├── 语义质量
├── 向量维度
├── 语言支持
├── 延迟
├── 成本
├── 上下文长度
└── 部署方式

理论
 什么是 Embedding
 什么是 Vector
 什么是 Vector Dimension
 什么是 Similarity
 什么是 Cosine Similarity
 Query Embedding
 Document Embedding
Coding
 调用 Embedding API
 获取 Vector
 查看 Vector Dimension
 自己实现 Cosine Similarity
 比较两个文本的相似度
 使用 LangChain embed_query()
 使用 LangChain embed_documents()
 Document → Chunk → Vector
工程
 理解 Embedding Model 不能随便混用
 理解中文/日文/英文多语言支持
 理解 Embedding 的成本和延迟
 理解 Vector Search 不等于完整搜索系统

# Day 20

## Learned RAG

一定要把这个架构记住：

             Document
                 │
                 ▼
          Text Splitter
                 │
                 ▼
              Chunks
                 │
                 ▼
          Embedding Model
                 │
                 ▼
              Vectors
                 │
                 ▼
          ┌──────────────┐
          │ Vector Store │
          └──────────────┘
                 ▲
                 │
              Query
                 │
                 ▼
          Query Embedding
                 │
                 ▼
        Similarity Search
                 │
                 ▼
          Relevant Chunks

这是后面 RAG 的核心。

# Day 21

## Learned RAG

                 Knowledge Base
                       │
                 ┌─────┴─────┐
                 ↓           ↓
             Documents     Metadata
                 │
                 ↓
              Chunking
                 │
                 ↓
             Embedding
                 │
                 ↓
            Vector Store
                 │
                 ↓
             Retriever
                 │
        ┌────────┴────────┐
        ↓                 ↓
   Similarity            MMR
        │                 │
        └────────┬────────┘
                 ↓
          Relevant Docs
                 │
                 ↓
              RAG
                 │
                 ↓
                LLM

# Day 22

## Learned RAG

        AI Agent Knowledge RAG
                  │
                  ↓
             User Query
                  │
                  ↓
              Retriever
                  │
                  ↓
          Relevant Documents
                  │
                  ↓
                Context
                  │
                  ↓
               Prompt
                  │
                  ↓
                 LLM
                  │
                  ↓
                Answer
                  │
                  ↓
               Sources

# Day 23

## Learned RAG

                 RAG
                  │
          ┌───────┴────────┐
          ↓                ↓
       Indexing         Retrieval
          │                │
          ↓                ↓
      Documents          Query
          │                │
          ↓                ↓
      Chunking         Embedding
          │                │
          ↓                ↓
      Embedding       Vector Search
          │                │
          ↓          ┌─────┴──────┐
     Vector Store     ↓            ↓
                  Metadata       Top-K
                     │            │
                     └─────┬──────┘
                           ↓
                    Relevant Docs
                           │
                           ↓
                        Context
                           │
                           ↓
                         Prompt
                           │
                           ↓
                          LLM
                           │
                           ↓
                         Answer

# Day 24

## Learned RAG

                    Evaluation
                        │
          ┌─────────────┴─────────────┐
          ↓                           ↓
   Retrieval Eval              Answer Eval
          │                           │
          ↓                           ↓
     Recall@K                      Correctness
     MRR                            Relevance
     Hit@K

# Day 25

## Learned RAG

                    ┌── Rewrite ────────┐
                    │                   │
Question ───────────┼── Multi-Query ────┼── Retriever
                    │                   │
                    └── HyDE ───────────┘
                                            ↓
                                        Documents
                                            ↓
                                           LLM
                                            ↓
                                         Answer
                                            ↓
                                       Evaluation

# Day 26

## Learned RAG

# Day 27

## Learned RAG

# Day 28

## Learned Agent

                    Agent
                      │
             ┌────────┴────────┐
             │                 │
            LLM              Tools
             │                 │
             │            ┌────┼────┐
             │            │    │    │
             │          Search RAG  API
             │
             ▼
          Decision
             │
             ▼
        Tool Calling
             │
             ▼
        Tool Execution
             │
             ▼
         Observation
             │
             ▼
           State
             │
             ▼
            LLM
             │
             └──────────→ Loop

# Day 29

## Learned Agent

09:00
  ↓
Tool Schema
  ↓
Pydantic 参数校验
  ↓
bind_tools
  ↓
strict
  ↓
Tool Execution Error
  ↓
ToolMessage(status="error")
  ↓
Structured Output
  ↓
Tool Routing
  ↓
完整 Agent
  ↓
测试

# Day 30

## Learned Agent

State = Agent 当前运行过程中需要携带的信息。

                     User
                          │
                          ↓
                 ┌────────────────┐
                 │     Agent      │
                 └───────┬────────┘
                         │
          ┌──────────────┴──────────────┐
          ↓                             ↓
   Short-term Memory              Long-term Memory
          │                             │
     Checkpointer                     Store
          │                             │
     thread_id                       user_id
          │                             │
          └──────────────┬──────────────┘
                         ↓
                 Context Engineering
                         ↓
                        LLM
RAG VS Memory
|      | RAG       | Memory      |
| ---- | --------- | ----------- |
| 数据来源 | 外部知识库     | Agent/用户历史  |
| 典型对象 | Documents | User facts  |
| 查询   | Query     | User/Thread |
| 目的   | 知识增强      | 个性化/连续性     |
| 更新   | 知识库更新     | Agent 交互产生  |
| 例子   | 公司技术文档    | 用户喜欢 Python |

# Day 31

## Learned Langgraph Agent Loop

                              USER
                               │
                               ↓
                        ┌─────────────┐
                        │   THREAD    │
                        └──────┬──────┘
                               ↓
                        ┌─────────────┐
                        │    STATE    │
                        └──────┬──────┘
                               ↓
                        ┌─────────────┐
                        │    AGENT    │
                        │     LLM     │
                        └──────┬──────┘
                               ↓
                       Conditional Edge
                         /           \
                        /             \
                  Tool Call          Final
                     ↓                ↓
               ┌──────────┐          END
               │ ToolNode │
               └────┬─────┘
                    ↓
                Tool Result
                    ↓
                  State
                    ↓
                  Agent
                    ↑
                    │
                    └──── Loop


Memory:
State
 ↓
Checkpointer
 ↓
thread_id

Long-term:
User
 ↓
Store
 ↓
Memory Retrieval
 ↓
Context
 ↓
Agent


# Day 32

## Learned Langgraph Agent State

Agent State
    │
    ├── Messages
    │
    ├── Task State
    │
    ├── Tool Results
    │
    ├── Retrieved Documents
    │
    ├── Intermediate Results
    │
    └── Metadata

# Day 33

## Learned Langgraph Agent Interrupt

                    ┌──────────────┐
                    │     User     │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │    Agent     │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │  Tool Call   │
                    └──────┬───────┘
                           ↓
                    High Risk?
                     /           \
                   No             Yes
                   ↓               ↓
                Tool          interrupt()
                                   ↓
                              Checkpoint
                                   ↓
                               Human
                              /      \
                        Approve      Reject
                           ↓            ↓
                         Tool          END
                           ↓
                         Agent
                           ↓
                          END

# Day 34

## Learned Langgraph Agent Persistence Persistence 解决 Agent 状态能不能保存

                         User
                          │
                          ↓
                    ┌───────────┐
                    │ thread_id │
                    └─────┬─────┘
                          ↓
                    ┌───────────┐
                    │ Checkpoint│
                    └─────┬─────┘
                          ↓
                       State
                          ↓
                     ┌────────┐
                     │ Agent  │
                     └───┬────┘
                         ↓
                     Tool Call
                         ↓
                   High Risk?
                    /       \
                  No         Yes
                  ↓           ↓
                Tool      interrupt
                              ↓
                         Checkpoint
                              ↓
                            Human
                              ↓
                       Command(resume)
                              ↓
                           Agent
                              ↓
                         Checkpoint
                              ↓
                            END

RAG → Tool Calling → Agent → State → Memory → LangGraph → HITL → Persistence

# Day 35

## Learned Langgraph Agent Stream Streaming 解决 Agent 执行过程能不能实时看到

                       LangGraph
                           │
                           ▼
                      graph.stream
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
     updates            messages            custom
        │                  │                  │
        │                  │                  │
        ▼                  ▼                  ▼
    Node状态             Token             自定义事件
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                      Backend Stream
                           │
                           ▼
                      SSE / WebSocket
                           │
                           ▼
                        React UI


# Day 36

## Learned LangGraph Streaming + FastAPI + SSE

- 理解 LangGraph 的 astream() 和 stream_mode
- 理解 messages 与 custom 两种流式模式
- 成功启动 FastAPI 服务
- 通过 POST /chat/stream 获取 SSE 响应
- 使用 httpx 客户端实时打印模型输出
- 能够解释 StreamingResponse 和 SSE 的区别

# Day 37

## Learned LangGraph Streaming + FastAPI + SSE + Persistence

- 能够解释 MessagesState 的作用
- 能够解释 Checkpointer 与 thread_id 的关系
- 同一 thread_id 的第二轮能够引用上一轮信息
- 不同 thread_id 的会话相互隔离
- FastAPI 接口可以持续返回 SSE token
- 能够说明 MemorySaver 重启后为什么会丢失数据
- 能够区分短期记忆与长期记忆

# Day 38

## Learned LangGraph Streaming + FastAPI + SSE + Persistence(sqlite)

- 理解 Checkpoint、Thread 和 Store 的区别
- 安装并使用 AsyncSqliteSaver
- 将 FastAPI Agent 接入 SQLite
- 同一 thread_id 可以恢复历史消息
- 重启服务后仍能恢复之前的会话
- 使用 aget_state_history 查看 checkpoint
- 理解 SQLite 与 PostgreSQL 的适用场景

# Day 39

## Learned LangGraph Streaming + FastAPI + SSE + Persistence + Store

- 理解 Checkpointer 与 Store 的区别
- 独立完成 Store 的 put/get/search/delete 操作
- 能够解释 namespace、key 和 value
- 将 Store 接入 LangGraph 节点
- 通过 user_id 读取对应的长期记忆
- 验证同一用户的不同 thread_id 能共享资料
- 验证不同用户的资料相互隔离
- 理解 InMemoryStore 不能提供重启后的持久化

# Day 40

## Learned LangGraph 语义检索、Embedding 与自动提取

用户输入
   ↓
LLM 提取记忆
   ↓
Embedding
   ↓
Store 保存
   ↓
语义检索
   ↓
注入 Agent Context

# Day 41

## Learned LangGraph Agent Memory Engineering：记忆去重、更新、遗忘机制与质量评估

- 实现 Memory Importance 判断
- 实现结构化 Memory Schema
- 实现 Embedding 相似度检测
- 实现 Memory Merge
- 实现 Memory Update
- 理解 TTL 和 Confidence
- 完成 MemoryManager

# Day 42

## MCP 核心概念与架构

- 能够解释 Host、Client、Server 的区别
- 能够区分 Tools、Resources、Prompts
- 理解 JSON-RPC 与传输层的区别
- 能够说明 stdio 与 Streamable HTTP 的使用场景
- 完成本地能力注册表代码
- 完成至少 3 个测试
- 画出 LangGraph + MCP Client + MCP Server 架构图

# Day 43

## MCP Server

- 安装并记录 MCP Python SDK 版本
- 使用 MCPServer 创建真实 MCP Server
- 成功注册并调用 search_notes Tool
- 成功读取 research://topics Resource
- 成功获取 create_research_prompt Prompt
- 通过 MCP Inspector 验证三类能力
- pytest 正常与错误场景测试通过
- 能解释 Server、Client 与 Host 的职责边界

# Day 44

## MCP Client：发现工具与调用工具

- 成功使用 stdio 连接 Day 43 的 Server
- 读取服务端身份、协议版本与能力信息
- 动态发现 Tools，并打印参数 Schema
- 成功调用 search_notes 并检查 is_error
- 读取 research://topics Resource
- 获取 create_research_prompt Prompt
- 封装可复用的 ResearchMCPClient
- 能够解释 MCP Client 的连接生命周期

# Day 45

## MCP 与 LangGraph Agent 集成

- 成功通过 Streamable HTTP 连接 MCP Server
- 通过 MCPAdapter 动态发现工具
- 成功创建 LangChain Agent
- Agent 能根据用户问题选择 MCP 工具
- 工具结果能够返回模型并生成最终答案
- 测试正常结果与空搜索结果
- 理解工具发现、模型决策、执行和结果反馈的完整循环
- 为潜在危险的工具设计权限或审批机制

# Day 46

## AI Agent 工程化：模块化与分层架构

- 模块拆分: 确认 API、Service、Agent、配置分别位于独立模块。
- 依赖注入: 让测试通过 FakeResearchService 运行，不依赖真实 API Key。
- 错误处理: 为 Agent 执行失败增加日志，并避免向客户端暴露内部异常。
- 扩展工具: 把 Day 45 的 MCP 工具接入 Agent 层，而不是塞进 API 路由。
- 回归测试: 执行 pytest -q，确认修改没有破坏现有接口。

# Day 47

## 配置管理、环境隔离与密钥安全

- 配置集中在 Settings 中，不再散落在业务代码里
- API Key 使用 SecretStr，并且没有真实默认值
- 错误环境名称和非法超时参数会触发校验错误
- .env 已被 Git 忽略，.env.example 不含真实密钥
- 测试可以不读取本地 .env 文件
- 测试请求不依赖真实模型 API
- 理解 get_settings 的缓存行为

# Day 48

## 日志、异常处理与可观测性

- 项目使用统一的 logging 配置
- 每个 HTTP 请求都能关联 request_id
- 响应头返回 X-Request-ID
- 日志记录请求状态码和耗时
- Agent 执行成功或失败时有对应日志
- 异常响应不包含内部堆栈和敏感信息
- 日志不输出 API Key、完整 Authorization 头或敏感用户内容
- pytest 全部通过

# Day 49

## Agent 超时、重试、限流与熔断

超时 Timeout
限制一次操作最多等待多久。防止请求无限等待，但不保证远端操作一定停止。

重试 Retry
对暂时性错误再次尝试，例如短暂网络中断或服务端返回 503。

限流与并发限制
控制单位时间内允许多少请求，以及同时允许多少任务执行，防止服务过载。

熔断 Circuit Breaker
当依赖服务持续失败时，暂时拒绝新的调用，避免把资源继续浪费在故障服务上。

- Agent 整体执行具有超时限制
- 理解指数退避与随机抖动
- 只对明确的暂时性异常进行重试
- 设置单进程并发限制
- 实现并测试速率限制
- 修正熔断器的失败阈值与半开逻辑
- 理解超时后远端操作仍可能继续
- pytest 全部通过

# Day 50

## Agent 评测与自动化回归测试

Agent 评测至少要覆盖四个维度：
1. 答案质量
答案是否正确、完整、相关，有没有编造事实？
2. 工具行为
是否调用了正确的工具？参数是否合理？有没有不必要的重复调用？
3. 可靠性
空结果、工具报错、超时或无效输入时，系统能否按预期处理？
4. 性能与成本
任务耗时多少？调用了多少次模型和工具？Token 成本是否超出预算？

- 建立固定的 Agent 评测数据集
- 实现规则评测器并理解关键词匹配的局限
- 运行真实 Agent 评测并保存 JSON 结果
- 使用 pytest 测试评测逻辑
- 能检查 Agent 是否调用了指定工具
- 理解单元测试、集成测试和模型评测的区别
- 能比较修改前后的通过率、耗时和工具调用表现
- 理解 LLM-as-a-Judge 的风险与适用范围