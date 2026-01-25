🧠 Demand Signals AI Agent

An AI-powered orchestration system that understands user intent and intelligently triggers different stages of a retail demand data pipeline.
This project combines Azure AI Foundry Agents + Intent Classification + Data Pipeline Simulation to create a smart assistant that can:
Understand what the user wants (sales history, insights, cleanup, demand signals)
Execute the correct pipeline step
Return structured execution results
Ask controlled follow-up questions for deeper insights

🚀 Project Architecture
User Query
   ↓
Intent Classifier (LLM)
   ↓
Execution Controller
   ↓
Pipeline Step (Data Generation / Processing)
   ↓
ExecutionResult (Structured Output)
   ↓
Follow-up Intelligence (Step 1.2)


📂 Project Structure
src/
│
├── chatbot/
│   ├── intent_classifier.py      # LLM-based intent detection
│   ├── execution_controller.py   # Routes intent → pipeline step
│   ├── execution_result.py       # Standard result schema
│   └── intents.py                # Enum of supported intents
│
├── data_generation/
│   ├── run_all.py                # Generates POS, Inventory, Finance data
│   ├── consolidation.py          # Merges datasets
│   ├── cleanup.py                # Data validation & cleaning
│   ├── gold_signal.py            # Demand signal logic
│   └── base_sku.py               # SKU generator using Faker
│
└── tests/
    └── test_step_2.py            # End-to-end orchestration test

    --added comments for feature branch


--changes did for master branch
--feature data

create table emp(id,name)