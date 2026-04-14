# Phase 4: Applied AI & Generative AI

> **Duration:** 8–10 weeks  
> **Prerequisite:** Phase 3 complete  
> **Goal:** Build real-world AI applications using LLMs, RAG, agents, and multimodal AI

---

## The GenAI Landscape (2025+)

```
Foundation Models (trained by OpenAI, Anthropic, Google, Meta)
          ↓
APIs / SDKs (OpenAI API, Anthropic API, Hugging Face)
          ↓
Orchestration Frameworks (LangChain, LlamaIndex, DSPy)
          ↓
Your Application Layer
          ↓
Users
```

As an Applied AI Solution Architect, your job is in the **application layer** — knowing which foundation model to use, how to orchestrate it, and how to build reliable systems on top of unpredictable AI outputs.

---

## Module 4.1 — Large Language Models: What They Are

### The Mental Model

An LLM is a text-in, text-out function. It was trained to predict the next token on trillions of tokens of text. As a side effect of doing this extremely well, it learned to reason, code, summarize, translate, and more.

```python
from openai import OpenAI

client = OpenAI()  # Requires OPENAI_API_KEY environment variable

# Basic completion
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a mobile app expert."},
        {"role": "user", "content": "What are the top 5 causes of iOS app crashes?"}
    ],
    temperature=0.7,    # 0=deterministic, 1=creative
    max_tokens=500
)

print(response.choices[0].message.content)
print(f"Tokens used: {response.usage.total_tokens}")
```

### Prompt Engineering (Critical Skill)

**Zero-shot prompting:**
```python
prompt = "Classify this app review as POSITIVE, NEGATIVE, or NEUTRAL: 'The app crashes every time I try to upload a photo'"
```

**Few-shot prompting — give examples:**
```python
prompt = """
Classify app reviews:

Review: "Works perfectly every time!" → POSITIVE
Review: "Crashes constantly, terrible." → NEGATIVE
Review: "It's okay, nothing special." → NEUTRAL

Review: "The new update broke everything, very disappointed." → 
"""
```

**Chain-of-thought prompting — force reasoning:**
```python
prompt = """
A mobile app has:
- Daily Active Users: 100,000
- Average session duration: 8 minutes
- Current churn rate: 5% per month
- Estimated LTV: $50 per user

If we reduce churn by 2% using an AI-powered re-engagement system that costs $20,000 to build and $5,000/month to operate, calculate the ROI over 12 months.

Think step by step:
"""
```

**Structured output — JSON mode:**
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": """
        Analyze this crash log and return JSON:
        {
            "error_type": string,
            "likely_cause": string,
            "severity": "low"|"medium"|"high"|"critical",
            "suggested_fix": string,
            "similar_known_issues": [string]
        }
        
        Crash log: NullPointerException at MainActivity.java:47 in onResume()
    """}],
    response_format={"type": "json_object"}
)

import json
result = json.loads(response.choices[0].message.content)
print(result['severity'])       # "high"
print(result['suggested_fix'])  # "Check for null before accessing..."
```

### LLM Parameters You Must Understand

| Parameter | Effect | Guidance |
|-----------|--------|----------|
| `temperature` | Randomness (0=deterministic, 2=very random) | 0 for code/JSON, 0.7 for creative writing |
| `max_tokens` | Max output length | Set per use case to control cost |
| `top_p` | Nucleus sampling width | Use temperature OR top_p, not both |
| `frequency_penalty` | Reduces repetition | 0.1-0.5 for long outputs |
| `presence_penalty` | Encourages topic diversity | 0.1-0.3 for brainstorming |
| `seed` | Reproducibility | Set for deterministic testing |

---

## Module 4.2 — Embeddings & Vector Search

**The most important concept in Applied AI after prompting.**

Embeddings turn text (or images, audio) into numerical vectors such that semantically similar content has similar vectors.

```
"The app crashed" → [0.12, -0.45, 0.87, ..., 0.33]  (1536 dimensions)
"Application error occurred" → [0.11, -0.43, 0.85, ..., 0.31]  (similar!)
"I love this app!" → [-0.72, 0.33, -0.11, ..., 0.67]  (very different)
```

This enables **semantic search** — finding relevant content by meaning, not just keyword match.

```python
from openai import OpenAI
import numpy as np

client = OpenAI()

def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Store embeddings
docs = [
    "The app crashes when uploading images larger than 10MB",
    "Login fails with OAuth when behind corporate proxy",
    "Push notifications not received on Android 14",
    "Dark mode toggle causes white flash on navigation"
]

doc_embeddings = [get_embedding(doc) for doc in docs]

# Search by meaning
query = "photos can't be uploaded"
query_embedding = get_embedding(query)

similarities = [cosine_similarity(query_embedding, doc_emb) for doc_emb in doc_embeddings]
best_match_idx = np.argmax(similarities)

print(f"Query: {query}")
print(f"Best match: {docs[best_match_idx]}")
print(f"Similarity: {similarities[best_match_idx]:.4f}")
# → "The app crashes when uploading images larger than 10MB" (0.89)
```

---

## Module 4.3 — RAG: Retrieval-Augmented Generation

**RAG is the most important architectural pattern in Applied AI.** It solves the core LLM limitation: LLMs don't know your private data.

### The RAG Architecture

```
User Query
    ↓
Query Embedding
    ↓
Vector DB Similarity Search → Retrieve Top-K Relevant Chunks
    ↓
Augment Prompt: [System Prompt + Retrieved Context + User Query]
    ↓
LLM Generates Answer Grounded in Your Data
    ↓
Response to User
```

### RAG with LlamaIndex (Production-Ready)

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

# Step 1: Configure models
Settings.llm = OpenAI(model="gpt-4o", temperature=0.1)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large")

# Step 2: Load and index documents
documents = SimpleDirectoryReader('docs/').load_data()  # Load PDF, TXT, MD files
index = VectorStoreIndex.from_documents(documents)

# Persist index (don't re-embed every run)
index.storage_context.persist(persist_dir="./index_storage")

# Step 3: Query
query_engine = index.as_query_engine(similarity_top_k=5)

response = query_engine.query(
    "How do I configure deep linking in our iOS SDK?"
)
print(response.response)

# Show source documents
for node in response.source_nodes:
    print(f"Source: {node.node.metadata.get('file_name', 'Unknown')}")
    print(f"Score: {node.score:.3f}")
    print(f"Text: {node.node.text[:200]}...")
    print()
```

### Building a RAG System from Scratch (Educational)

```python
import chromadb
from openai import OpenAI
import textwrap

client = OpenAI()

# 1. Vector Database Setup
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(
    name="mobile_sdk_docs",
    metadata={"hnsw:space": "cosine"}
)

# 2. Chunking Strategy (Critical for RAG Quality)
def chunk_document(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split document into overlapping chunks for better context preservation"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# 3. Index Documents
def index_documents(docs: list[dict]):
    for doc in docs:
        chunks = chunk_document(doc['content'])
        embeddings = [
            client.embeddings.create(model="text-embedding-3-large", input=chunk).data[0].embedding
            for chunk in chunks
        ]
        collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=[{"source": doc['source'], "chunk_idx": i} for i in range(len(chunks))],
            ids=[f"{doc['source']}_{i}" for i in range(len(chunks))]
        )

# 4. RAG Query Function
def rag_query(question: str, top_k: int = 5) -> str:
    # Embed the question
    q_embedding = client.embeddings.create(
        model="text-embedding-3-large", input=question
    ).data[0].embedding
    
    # Retrieve relevant chunks
    results = collection.query(query_embeddings=[q_embedding], n_results=top_k)
    context = "\n\n---\n\n".join(results['documents'][0])
    
    # Generate answer grounded in retrieved context
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """You are a helpful technical assistant.
            Answer based ONLY on the provided context. 
            If the answer is not in the context, say "I don't have information about that."
            Always cite which part of the context you used."""},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content

# 5. Evaluate RAG quality
def evaluate_rag(question: str, expected_answer: str) -> dict:
    actual_answer = rag_query(question)
    
    # Use LLM as judge
    eval_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"""
            Question: {question}
            Expected Answer: {expected_answer}
            Actual Answer: {actual_answer}
            
            Rate the actual answer on:
            - Correctness (0-10): Is the information accurate?
            - Completeness (0-10): Does it cover the key points?
            - Groundedness (0-10): Is it based on facts, not hallucinations?
            
            Return JSON: {{"correctness": int, "completeness": int, "groundedness": int, "explanation": str}}
        """}],
        response_format={"type": "json_object"}
    )
    return json.loads(eval_response.choices[0].message.content)
```

### RAG Quality Levers (For Architecture Decisions)

| Problem | Solution |
|---------|---------|
| Retrieved chunks miss context | Increase chunk overlap; use sentence-aware splitting |
| Wrong chunks retrieved | Better embedding model; metadata filtering; hybrid search |
| LLM ignores retrieved context | Stronger system prompt; reranking with cross-encoder |
| Slow retrieval | HNSW index tuning; caching frequent queries |
| Outdated information | Incremental re-indexing; document versioning |
| Hallucination in answers | Stricter system prompt; answer verification step; guardrails |

---

## Module 4.4 — AI Agents

**Agents = LLM + Tools + Memory + Planning Loop**

An agent can take actions (search the web, run code, call APIs, query databases) and iterate based on results.

```python
from openai import OpenAI
import json

client = OpenAI()

# Define tools the agent can use
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_crash_reports",
            "description": "Get crash reports for a specific app version from the analytics database",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_version": {"type": "string", "description": "The app version to query"},
                    "days": {"type": "integer", "description": "Number of days to look back"}
                },
                "required": ["app_version", "days"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_jira_ticket",
            "description": "Create a JIRA ticket for a bug",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "priority": {"type": "string", "enum": ["Low", "Medium", "High", "Critical"]}
                },
                "required": ["title", "description", "priority"]
            }
        }
    }
]

# Tool implementations
def get_crash_reports(app_version: str, days: int) -> dict:
    # In reality: query your analytics DB
    return {
        "version": app_version,
        "crash_count": 1247,
        "affected_devices": 892,
        "top_crash": "NullPointerException in UserProfileActivity.java:234",
        "crash_rate": "8.2%"
    }

def create_jira_ticket(title: str, description: str, priority: str) -> dict:
    # In reality: call JIRA API
    return {"ticket_id": "MOB-4829", "url": "https://jira.company.com/MOB-4829", "status": "Created"}

# Agent loop
def run_agent(user_request: str) -> str:
    messages = [
        {"role": "system", "content": "You are a mobile app engineering assistant. Analyze crash reports and create tickets as needed."},
        {"role": "user", "content": user_request}
    ]
    
    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        msg = response.choices[0].message
        
        # If no tool call, we're done
        if not msg.tool_calls:
            return msg.content
        
        # Execute tool calls
        messages.append(msg)
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            print(f"Agent calling: {func_name}({args})")
            
            if func_name == "get_crash_reports":
                result = get_crash_reports(**args)
            elif func_name == "create_jira_ticket":
                result = create_jira_ticket(**args)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

# Run it
response = run_agent(
    "Check crash reports for version 2.3.0 from the last 7 days. "
    "If the crash rate is above 5%, create a critical JIRA ticket."
)
print(response)
```

### LangChain Agents (Framework Approach)

```python
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain import hub

llm = ChatOpenAI(model="gpt-4o", temperature=0)

@tool
def search_app_reviews(query: str) -> str:
    """Search app store reviews for user feedback matching a query"""
    # Implementation
    return f"Found 47 reviews mentioning: {query}"

@tool
def analyze_crash_stack_trace(stack_trace: str) -> str:
    """Analyze a crash stack trace and identify the root cause"""
    # Could call another LLM or rules engine
    return "Root cause: Memory leak in image cache not releasing on low memory signal"

tools = [search_app_reviews, analyze_crash_stack_trace]

# Use a pre-built prompt or define your own
prompt = hub.pull("hwchase17/openai-tools-agent")

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10)

result = agent_executor.invoke({
    "input": "Find what users are complaining about and check if there are related crash reports"
})
print(result['output'])
```

---

## Module 4.5 — Multimodal AI

Modern AI systems process images, audio, text, and video together.

```python
# GPT-4V: Image + Text
import base64

def analyze_screenshot(image_path: str, question: str) -> str:
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
            ]
        }]
    )
    return response.choices[0].message.content

# Use cases for mobile:
# - Analyze UI screenshots for accessibility issues
# - Extract text from screenshots (receipts, business cards)
# - Describe what a user is seeing for support agents
# - Automated visual regression testing with AI

result = analyze_screenshot(
    "app_screenshot.png",
    "Describe any UX issues you see in this mobile app screen. Be specific about accessibility, visual hierarchy, and usability problems."
)
```

---

## Module 4.6 — AI Application Patterns

### Pattern 1: Summarization Pipeline

```python
def summarize_support_tickets(tickets: list[str]) -> dict:
    """Summarize a batch of support tickets and extract action items"""
    combined = "\n---\n".join(tickets[:50])  # Limit for context window
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": f"""Analyze these {len(tickets)} support tickets and return JSON:
            {{
                "top_issues": [string],  # Top 5 most common issues
                "severity_distribution": {{"critical": int, "high": int, "medium": int, "low": int}},
                "recommended_actions": [string],  # Prioritized action list
                "sentiment_trend": "improving"|"stable"|"degrading"
            }}
            
            Tickets:
            {combined}"""
        }],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
```

### Pattern 2: AI-Powered Code Review

```python
def review_mobile_code(code: str, language: str = "Swift") -> dict:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "system",
            "content": f"You are an expert {language} mobile developer and security engineer."
        }, {
            "role": "user",
            "content": f"""Review this code for:
            1. Memory leaks and retain cycles
            2. Thread safety issues
            3. Battery optimization problems
            4. Security vulnerabilities
            5. Performance bottlenecks
            
            Return JSON with issues array, each having: line_number, severity, type, description, fix.
            
            Code:
            ```{language}
            {code}
            ```"""
        }],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)
```

### Pattern 3: Guardrails & Safety

```python
# Always validate AI outputs in production
def safe_llm_call(prompt: str, max_retries: int = 3) -> str:
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                timeout=30
            )
            result = response.choices[0].message.content
            
            # Validate output (customize per use case)
            if len(result) < 10:
                raise ValueError("Response too short — likely an error")
            
            return result
            
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff

# Input validation — prevent prompt injection
def validate_user_input(user_input: str) -> str:
    forbidden_patterns = [
        "ignore previous instructions",
        "system prompt",
        "jailbreak",
        "you are now"
    ]
    lower_input = user_input.lower()
    for pattern in forbidden_patterns:
        if pattern in lower_input:
            return "[Input blocked: potential prompt injection detected]"
    return user_input
```

---

## Module 4.7 — LLM Cost Optimization

Critical skill for Solution Architects — AI costs can spiral quickly.

| Strategy | Savings | Trade-off |
|---------|---------|----------|
| Use smaller model (GPT-4o-mini vs GPT-4o) | 95% | Lower capability |
| Prompt compression | 20-40% | Engineering effort |
| Response caching | 50-80% for repeated queries | Stale responses |
| Batch processing | 50% | Latency |
| Streaming | Better UX, same cost | Implementation complexity |
| Fine-tuning small model | 90%+ at scale | Training cost upfront |

```python
# Semantic caching — cache by meaning, not exact string
from functools import lru_cache
import hashlib

embedding_cache = {}
response_cache = {}

def cached_llm_call(prompt: str, similarity_threshold: float = 0.95) -> str:
    # Get embedding for the prompt
    prompt_embedding = get_embedding(prompt)
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    
    # Check if similar query was answered before
    for cached_prompt, cached_embedding in embedding_cache.items():
        similarity = cosine_similarity(prompt_embedding, cached_embedding)
        if similarity > similarity_threshold:
            print(f"Cache hit! Similarity: {similarity:.3f}")
            return response_cache[cached_prompt]
    
    # Cache miss — call LLM
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content
    
    embedding_cache[prompt_hash] = prompt_embedding
    response_cache[prompt_hash] = response
    return response
```

---

## Phase 4 Capstone Project

**Project: RAG Chatbot over Mobile SDK Documentation**

Build a production-quality RAG chatbot that answers questions about your company's mobile SDK documentation (or use a public SDK like Firebase, React Native, or Flutter docs).

**Requirements:**
1. Scrape/download and chunk the documentation (>100 pages)
2. Embed and store in ChromaDB with metadata
3. Build RAG pipeline with LlamaIndex
4. Add a reranking step with a cross-encoder model
5. Implement conversation memory (multi-turn chat)
6. Build a FastAPI backend with these endpoints:
   - `POST /chat` — Send message, get response
   - `GET /sources` — Get source documents for last response
   - `POST /feedback` — Thumbs up/down on responses
7. Build a simple Streamlit or Gradio UI
8. Evaluate: Run 20 test questions, measure answer quality (LLM-as-judge)
9. Deploy to Hugging Face Spaces (free) or Railway

**Why this project:** RAG chatbots are the #1 GenAI enterprise use case. Every company wants one. This project proves you can architect and build one end-to-end.

---

## Phase 4 Completion Checklist

- [ ] Understand LLMs, prompting, and how to get reliable structured outputs
- [ ] Understand embeddings and cosine similarity
- [ ] Built a semantic search system from scratch
- [ ] Built a full RAG pipeline with chunking, embedding, retrieval, and generation
- [ ] Know the quality levers for RAG (chunking strategy, embedding model, reranking)
- [ ] Built an LLM agent with tool use
- [ ] Used multimodal AI (image + text)
- [ ] Applied AI cost optimization strategies
- [ ] Implemented guardrails and input validation
- [ ] Completed the RAG chatbot capstone project

**When all boxes are checked → move to [Phase 5](../phase-5-mlops-ai-engineering/README.md)**
