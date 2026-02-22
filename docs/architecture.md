# AI Testcase Agent Architecture

## Overview

This project is an AI-powered Test Case Generator using:

- LLM (OpenAI GPT)
- RAG (FAISS vector search)
- FastAPI (API layer)
- Playwright (test execution)
- Agent orchestration layer

---

## Architecture Flow

User → FastAPI → Agent → RAG → LLM → Response → Testcases

---

## Components

### 1. API Layer (`src/api/api.py`)
Handles incoming requests and routes to agent.

### 2. Agent Layer (`src/rag/agent.py`)
Orchestrates:

- RAG retrieval
- LLM prompt construction
- response generation

### 3. RAG Layer (`src/rag/`)
Uses:

- FAISS vector DB
- embedding search
- requirement retrieval

### 4. LLM Client (`src/llm/client.py`)
Handles communication with OpenAI.

### 5. Demo App (`demo_app/`)
Login app used for testing.

### 6. Tests (`tests/`)
Playwright automated tests.

---

## Tech Stack

- Python
- OpenAI API
- FastAPI
- FAISS
- Playwright
- Pytest