# AI Testcase Agent using LLM, RAG, and Agentic AI

## Overview

This project implements an autonomous AI agent that generates software test cases and automation scripts using Large Language Models, Retrieval-Augmented Generation (RAG), and Playwright.

It demonstrates a real-world AI engineering workflow from requirements → test cases → automation → execution.

---

## Features

- LLM-powered test case generation
- Multi-agent architecture (Planner, Generator, Reviewer)
- Retrieval-Augmented Generation using requirement PDFs
- Automated Playwright test generation
- Fully executable automation framework
- FastAPI integration
- Config-driven design

---

## Architecture

Input Feature / Requirements
        ↓
Planner Agent
        ↓
RAG Pipeline (PDF Context)
        ↓
Generator Agent
        ↓
Reviewer Agent
        ↓
Automation Agent
        ↓
Playwright Execution

---

## Tech Stack

Python  
OpenAI API  
FastAPI  
Playwright  
Pytest  
FAISS (vector search)  
Agentic AI  

---

## Run locally

Start demo app:

uvicorn demo_app.app:app --reload

Run agent:

python run.py

Run automation tests:

python -m pytest -q

---

## Example Result

4/4 automation tests passed using AI-generated test cases and scripts.

---

## Author

Mahesh Desu  
AI Engineer Portfolio Project