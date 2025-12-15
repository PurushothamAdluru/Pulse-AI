# Pulse AI

Pulse AI is a lightweight AI agent experiment focused on understanding customer conversations at scale.

Customer messages often carry implicit signals — intent, urgency, sentiment — but time constraints make it difficult to analyze each interaction carefully. Pulse AI explores how an AI agent can quietly extract those signals and make them visible through a simple, clean dashboard.

## What it does

- Listens to customer messages
- Identifies intent (pricing, support, demo requests, etc.)
- Analyzes sentiment
- Scores lead readiness
- Suggests a recommended next action
- Logs insights to structured data
- Visualizes trends and patterns in a dashboard

The goal is not heavy automation, but clarity — helping teams quickly understand what kind of conversations are happening and where attention is needed.

## How it works

- Conversations happen through an AI agent powered by Ollama
- Each customer message is analyzed in real time
- Insights are stored locally in a structured JSON file
- A Streamlit dashboard reads this data and displays live analytics

Chat and analytics are intentionally separated to keep the system fast, simple, and easy to reason about.

## Tech Stack

- Python
- Ollama (local LLM runtime)
- Streamlit
- JSON (lightweight data storage)

## Why this project

As communication volume increases and systems become more dynamic, teams need faster ways to understand conversations without reading everything manually. Pulse AI is a small experiment exploring how AI agents and well-designed insight layers can support quicker, more informed decision-making.

## Status

Early-stage experimental project. Built for learning, exploration, and demonstration.
