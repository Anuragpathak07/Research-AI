# Agentic AI Implementation

## Overview

This project now implements **true agentic AI** using the ReAct (Reasoning + Acting) pattern with LLM-powered reasoning for each agent.

## Architecture

### Base Agent Class (`base_agent.py`)

All agents inherit from `BaseAgent` which provides:
- **ReAct Pattern**: Reasoning → Action → Observation loop
- **Tool Use**: Agents can use tools to perform actions
- **LLM Reasoning**: Autonomous decision-making using Ollama
- **Fallback Handling**: Graceful degradation when LLM is unavailable

### Agentic Agents

1. **DiscoveryAgent** (`discovery_agent.py`)
   - **Reasoning**: Optimizes search queries, analyzes paper relevance
   - **Tools**: `search_arxiv`, `filter_by_relevance`
   - **Capabilities**: 
     - Reasons about best search strategy
     - Analyzes paper quality and relevance
     - Decides whether to refine queries

2. **ExtractionAgent** (`extraction_agent.py`)
   - **Reasoning**: Chooses extraction strategy (keyword vs LLM)
   - **Tools**: `extract_keywords`, `analyze_paper_content`
   - **Capabilities**:
     - Decides when to use keyword matching vs LLM analysis
     - Validates extracted entities
     - Handles edge cases intelligently

3. **TrajectoryAgent** (`trajectory_agent.py`)
   - **Reasoning**: Analyzes research evolution patterns
   - **Tools**: `calculate_trend`, `classify_trajectory`
   - **Capabilities**:
     - Reasons about trajectory classification
     - Validates ambiguous cases with LLM
     - Considers multiple factors for classification

4. **GapAgent** (`gap_agent.py`)
   - **Reasoning**: Assesses temporal viability of research gaps
   - **Tools**: `analyze_gap_viability`, `generate_gap_hypothesis`
   - **Capabilities**:
     - Classifies gaps as future-viable, time-sensitive, or likely-obsolete
     - Generates gap hypotheses
     - Provides detailed temporal justification

5. **ExperimentAgent** (`experiment_agent.py`)
   - **Reasoning**: Designs future-aligned experiments
   - **Tools**: `design_experiment`, `select_datasets`, `generate_code_structure`
   - **Capabilities**:
     - Designs experiments aligned with gaps
     - Selects appropriate datasets and models
     - Generates code structure
     - Ensures temporal relevance

## ReAct Pattern Implementation

Each agent follows this pattern:

```
Thought: [Agent reasons about what to do]
Action: [Choose a tool or provide final answer]
Action Input: [Input for the action]
Observation: [Result from the action]
[Repeat until final answer]
```

## Usage

Agents are used automatically through the API endpoints:
- `/api/discover/` - Uses DiscoveryAgent
- `/api/clusters/` - Uses ExtractionAgent (via clustering)
- `/api/gaps/` - Uses GapAgent + TrajectoryAgent
- `/api/experiments/` - Uses ExperimentAgent

## Benefits

1. **Autonomous Decision-Making**: Agents reason about best approaches
2. **Adaptive Behavior**: Adjusts strategy based on context
3. **Tool Use**: Can use multiple tools to accomplish tasks
4. **Better Accuracy**: LLM reasoning improves entity extraction and classification
5. **Temporal Awareness**: Agents understand research evolution and temporal relevance

## Fallback Behavior

If LLM is unavailable, agents gracefully fall back to:
- Rule-based logic
- Keyword matching
- Statistical analysis

This ensures the system works even without LLM, but with reduced intelligence.

