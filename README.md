# AI Test Case Generator with Agentic AI and RAG

## Overview

This project uses Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and Agentic AI to automatically:

- Generate test cases from feature descriptions
- Refine test cases using QA best practices
- Generate Playwright automation code
- Execute automation tests against a real application

## Architecture

Feature Description
       ↓
Planner Agent
       ↓
RAG Pipeline (PDF context)
       ↓
Generator Agent
       ↓
Reviewer Agent
       ↓
Automation Generator Agent
       ↓
Playwright Test Execution

## Tech Stack

- Python
- OpenAI API
- FastAPI
- Playwright
- pytest
- RAG
- Agentic AI

## Example Result

- Generated test cases automatically
- Generated automation code automatically
- Executed tests successfully (4 passed)

## How to Run

Start demo app:

uvicorn demo_app.app:app --reload

Run agent:

python agent.py

Run tests:

python -m pytest -q