# Multi-Agent Maritime Supply Chain Monitoring and Rerouting System

This system is a modular, multi-agent solution designed to monitor vessel positions, identify route anomalies or hazards, calculate optimized alternative paths, and analyze downstream supply chain and port impacts. It is built using the CrewAI framework and orchestrates local LLM processing via Ollama.

## System Architecture

The system uses three specialized agents executing sequentially:

1. Maritime Operations Monitor: Uses fleet telemetry data to track positions and capture coordinates, destinations, and active disruptions.
2. Dynamic Rerouting Strategist: Analyzes active disruptions to calculate alternative maritime paths, specific waypoint adjustments, and updated ETA offsets.
3. Supply Chain Impact Analyst: Evaluates the route changes against destination port backlogs, demurrage fees, and warehouse safety margins to produce a risk mitigation brief.

### Tools

* get_fleet_telemetry: Retrieves live mock telemetry data for a given ship ID.
* get_port_metrics: Retrieves active backlog and demurrage details for a specified destination port.

## Directory Structure

```text
maritime-rerouter/
├── config/
│   ├── agents.yaml
│   └── tasks.yaml
├── tools/
│   └── api_tools.py
├── main.py
├── requirements.txt
└── README.md
```

## Prerequisites

1. Install Ollama from the official website.
2. Download the Llama 3 model:
   ```bash
   ollama run llama3
   ```
3. Ensure the Ollama server is running locally at http://localhost:11434.

## Setup and Usage

1. Activate the Python virtual environment:
   * On Windows:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   * On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the orchestration script:
   ```bash
   python main.py
   ```
