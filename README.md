Akshay's Multi-Tool Conversational AI Agent
A sophisticated, full-stack conversational AI agent with a custom UI, capable of understanding user intent, selecting from a variety of tools to perform real-world actions, and maintaining conversational context.

Live Demo Link --> https://akshays-llm-agent-orchestrator.vercel.app/

Overview
This project is more than a simple chatbot. It is an intelligent agent built on a modern, tool-using architecture. When a user sends a query, a Large Language Model (LLM) acts as a reasoning engine or "brain" to determine the user's intent. Based on this intent, it dynamically selects the appropriate tool—such as fetching live weather data, retrieving stock prices, or searching for news—and executes it. This allows the agent to go beyond pre-programmed responses and interact with real-world data and services.

Key Features
Intelligent Tool Selection: Uses an LLM (Groq) for advanced function calling, allowing the agent to dynamically choose the right tool for any given query.

Multi-Tool Capability: Equipped with a suite of tools to perform diverse tasks:

Real-time Weather: Fetches current weather from any city using the Open-Meteo API.

Live Stock Prices: Retrieves the latest stock data via the Alpha Vantage API.

Current News: Pulls recent headlines on any topic from NewsAPI.org.

Knowledge Base: Gets concise summaries from Wikipedia.

Calculator: Evaluates mathematical expressions.

Conversational Memory: Maintains short-term memory of the conversation, allowing it to understand context and answer follow-up questions intelligently.

Robust Error Handling: The agent gracefully handles API failures, rate limits, and invalid user inputs, providing clear, user-friendly feedback.

Custom Aesthetic UI: A sleek, responsive frontend built with HTML, Tailwind CSS, and JavaScript, featuring a custom color palette and smooth animations.

Serverless Deployment: A scalable and efficient backend deployed on Vercel's serverless platform.

Architecture
The application follows a modern, decoupled architecture:

Frontend (Static UI): A responsive user interface served globally by Vercel's CDN.

Backend (FastAPI on Vercel): A Python-based API that serves as the entry point for all requests.

LLM Orchestrator: The core of the agent. It receives the user's query and conversation history, then prompts the LLM to choose a tool.

Tool Execution: Based on the LLM's decision, the corresponding Python function is executed, calling the necessary third-party API to get real-world data.

Response: The result is sent back to the frontend and displayed to the user.

Tech Stack
Backend: Python, FastAPI

Frontend: HTML, Tailwind CSS, JavaScript

AI/LLM: Groq API (for reasoning and fallback)

Deployment: Vercel (Serverless Functions and CDN)

APIs:

NewsAPI

Alpha Vantage

Open-Meteo

Wikipedia

Grok XAI
