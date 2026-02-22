# AI Testcase Agent (LLM + RAG + Agent + Playwright)

AI-powered system that generates, validates, and executes software test cases using Large Language Models and Retrieval-Augmented Generation.

This project demonstrates production-grade AI engineering architecture.

---

## Features

- LLM-powered testcase generation
- RAG-based requirement retrieval
- Agent orchestration
- FastAPI interface
- Playwright automated execution
- Vector search with FAISS

---

## Architecture

See docs/architecture.md

---

## Project Structure

---

## Installation
git clone https://github.com/maheshdesu12-bot/ai-testcase-agent.git

cd ai-testcase-agent

python -m venv ai-env
source ai-env/bin/activate

pip install -r requirements.txt

---

## Setup Environment

Create `.env`
OPENAI_API_KEY=your_api_key_here

---

## Run API
uvicorn src.api.api:app --reload

---

## Run Tests
pytest

---

## Example Use Case

Input:
Login feature with email/password

Output:
Generated test cases with validation and execution

---

## Technologies Used

- Python
- OpenAI GPT
- FastAPI
- FAISS
- Playwright
- Pytest

---

## Author

Mahesh Desu
AI Engineer Portfolio Project