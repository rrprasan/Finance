# 🧠 Snowflake Cortex AI_COMPLETE Masterclass: The Practice Notebook
## Overview
This repository contains a comprehensive Snowflake Notebook designed to bridge the gap between basic prompt engineering and production-grade AI pipelines. It focuses exclusively on AI_COMPLETE—the "Swiss Army Knife" of Snowflake Cortex AI functions.

While specialized functions like AI_CLASSIFY or AI_SENTIMENT are powerful, AI_COMPLETE offers the control Data Engineers and Data Scientists need for complex, custom logic. This notebook is a hands-on guide to mastering those controls.

## 🚀 What You Will Learn
By running through this notebook, you will explore:

### 1. 🎛️ Hyper-parameter Tuning
Learn how to fine-tune model behavior using the model_parameters object:

- Temperature: Control deterministic vs. creative outputs (0.0 - 1.0).

- Max Tokens: Manage response length and compute costs.

- Top_P (Nucleus Sampling): Adjust the diversity of the token selection pool.

- Guardrails: Enable or disable safety filters.

### 2. 🏗️ Structured Outputs (JSON)
Move beyond unstructured text. Learn to use response_format to force the LLM to output valid, schema-compliant JSON objects—essential for reliable Data Engineering pipelines.

### 3. ⚡ The "Chameleon" Technique
See how AI_COMPLETE can mimic and extend other Cortex functions:

- Custom Classification: Add confidence scores and reasoning to classification tasks.

- Enhanced Sentiment: Perform aspect-based sentiment analysis (e.g., quality vs. price).

- Complex Extraction: Extract multi-layered entities from documents and tickets.

- Similarity Analysis: Get similarity scores plus semantic explanations.

### 4. 🎭 Advanced Prompt Engineering
Role-Based Prompting: Simulate personas (e.g., "Senior Equity Analyst") using System, User, and Assistant roles.

Multi-Turn Simulation: Create conversational context within a single SQL call.

Few-Shot Prompting: Teach the model complex output formats using examples.

## 📂 Real-World Use Cases Included
The notebook includes setup scripts for demo tables (CUSTOMER_REVIEWS, SUPPORT_TICKETS, DOCUMENTS) to practice:

Automated Support Ticket Triage

Equity Research Summarization

Executive Document Summarization

Multi-language Translation Pipelines

## 🛠️ Prerequisites
- A Snowflake Account with Cortex AI enabled.

- SNOWFLAKE.CORTEX_USER database role.

- A warehouse for compute.
