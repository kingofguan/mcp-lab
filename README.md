# MCP Lab – AI Agent Integration Experiments

**Overview**  
This repository is my sandbox for learning **AI-native product engineering**. I explored how to connect large language models (Claude, OpenAI, and local models) to external services using **Model Context Protocol (MCP)**, then tested multiple frameworks and deployment strategies. As a proof-of-concept, I built a crypto assistant that queries Binance data and generates summaries.

---

## Strategies Explored

- **MCP Integrations**
  - Local MCP server setup  
  - Cursor IDE integration for rapid iteration  
  - Claude API + OpenAI API configurations  
  - Custom tools, resources, and prompts (e.g., Binance price fetch + executive summary)  

- **Agent Orchestration**
  - **LangChain** – classic agent/tool abstraction  
  - **LangGraph** – stateful, graph-based workflows  

- **Deployment Approaches**
  - **Docker** containerization for reproducibility  
  - **Render.com** deployment for cloud access  
  - Local + remote testing with inspector and MCP clients  

- **Ecosystem & Tooling**
  - TypeScript + npm for MCP inspector and client tooling  
  - Python backend for server and API connectors  
  - Modular project design to support future extensions  

