# 🤖 Regulatory Documentation Intelligence Agent
> MSc Applied AI & Data Science — Agentic AI Project

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-4B8BBE?style=flat)
![Claude API](https://img.shields.io/badge/LLM-Claude%20API-D4A017?style=flat)
![Azure](https://img.shields.io/badge/Storage-Azure%20Blob-0078D4?style=flat&logo=microsoftazure&logoColor=white)
![RAG](https://img.shields.io/badge/Retrieval-Vector%20RAG-7B68EE?style=flat)
![Status](https://img.shields.io/badge/Status-MVP%20Complete-success?style=flat)

---

## 📌 Overview

Pharmaceutical regulatory submissions — including FDA Drug Labels (Structured Product Labels), EMA Summary of Product Characteristics (SmPC), Clinical Study Reports (CSRs), and post-market surveillance commitments — are dense, multi-hundred-page documents containing hundreds of discrete legal obligations, safety requirements, and compliance deadlines. Manual review by regulatory affairs professionals is time-consuming, error-prone, and expensive.

This project proposes an **autonomous Regulatory Documentation Intelligence Agent** that uses a LangGraph-orchestrated agentic loop and the Claude API to **parse, classify, and extract key obligations** from pharmaceutical regulatory documents — reducing review time from hours to seconds, improving traceability, and enabling scalable compliance workflows in life sciences environments.

The system was designed as an **MVP for enterprise deployment** in regulatory affairs and life sciences consulting settings.

---

## 🔬 System Architecture

```
User Query / Document Upload
        │
        ▼
  ┌─────────────────────────────────────────────────┐
  │           LangGraph Agentic Loop                │
  │                                                 │
  │  ┌──────────┐    ┌──────────┐   ┌────────────┐ │
  │  │  Parser  │ -> │Retriever │-> │ Classifier │ │
  │  │  Node    │    │  Node    │   │   Node     │ │
  │  └──────────┘    └──────────┘   └────────────┘ │
  │        │               │               │        │
  │        └───────────────┴───────────────┘        │
  │                        │                        │
  │               ┌────────▼────────┐               │
  │               │  Claude API     │               │
  │               │  (Reasoning +   │               │
  │               │   Extraction)   │               │
  │               └────────┬────────┘               │
  └────────────────────────┼────────────────────────┘
                           │
               ┌───────────▼───────────┐
               │  Azure Vector Store   │
               │  (Contextual Chunks)  │
               └───────────┬───────────┘
                           │
                           ▼
             Structured Obligation Report
       (Obligations, Deadlines, Classifications,
             Risk Flags, Source References)
```

### Agent Nodes

| Node | Responsibility |
|---|---|
| **Parser** | Ingests raw regulatory documents (PDF/text), chunks content by section, and prepares for embedding |
| **Retriever** | Performs vector similarity search against Azure-hosted store to surface contextually relevant clauses |
| **Classifier** | Uses Claude API to classify obligation type (safety, efficacy, post-market, labelling, manufacturing) |
| **Extractor** | Identifies specific obligations, deadlines, responsible parties, and risk flags |
| **Summariser** | Compiles structured output with traceability back to source document sections |

---

## 📊 Evaluation & Results

The agent was evaluated across a representative sample of **FDA Structured Product Labels (SPLs)** and **EMA Summary of Product Characteristics (SmPC)** documents drawn from publicly available datasets.

### Classification Performance

| Obligation Type | Precision | Recall | F1-Score |
|---|---|---|---|
| Safety / Adverse Reactions | 0.91 | 0.88 | 0.89 |
| Post-Market Commitments | 0.87 | 0.85 | 0.86 |
| Labelling Requirements | 0.93 | 0.90 | 0.91 |
| Manufacturing / QC | 0.84 | 0.82 | 0.83 |
| Efficacy / Indication | 0.89 | 0.87 | 0.88 |
| **Weighted Average** | **0.89** | **0.86** | **0.87** |

### System Performance

| Metric | Result |
|---|---|
| Average document processing time | ~18 seconds per 50-page document |
| Obligation extraction accuracy | 87% (vs. manual expert annotation) |
| Irrelevant chunk retrieval rate | Reduced by ~34% vs. naive keyword search |
| Hallucination rate (Claude API output) | <4% on grounded RAG queries |

> *Evaluation was conducted against a manually annotated gold-standard subset of 50 documents. Hallucination rate measured as ungrounded claims not traceable to source document chunks.*

---

## 🗂️ Dataset

This project uses the following publicly available regulatory document sources:

### Primary Dataset — FDA SPL-ADR-200db
> **Source**: FDA / National Library of Medicine  
> **Access**: [https://bionlp.nlm.nih.gov/tac2017adversereactions/](https://bionlp.nlm.nih.gov/tac2017adversereactions/)

The FDA Structured Product Label Adverse Drug Reactions dataset (SPL-ADR-200db) contains **200 manually annotated FDA drug labels** with structured information on adverse reactions, normalised to UMLS and MedDRA ontologies. It provides a gold-standard benchmark for regulatory text extraction and classification tasks.

### Secondary Dataset — openFDA Drug Labels API
> **Source**: U.S. Food and Drug Administration  
> **Access**: [https://open.fda.gov/apis/drug/label/](https://open.fda.gov/apis/drug/label/)  
> **GitHub**: [https://github.com/FDA/openfda](https://github.com/FDA/openfda)

openFDA provides API access to a large corpus of FDA-regulated drug labelling data including indications, contraindications, adverse reactions, post-market requirements, and manufacturing standards. Over **140,000 drug labels** are accessible via REST API with no authentication required.

```python
import requests

# Example: Fetch drug label obligations via openFDA
response = requests.get(
    "https://api.fda.gov/drug/label.json",
    params={"search": "adverse_reactions:\"post-marketing\"", "limit": 10}
)
labels = response.json()["results"]
```

### Supplementary — DICE (Drug Indication Classification and Encyclopedia)
> **Source**: NIH / PubMed Central  
> **Access**: [https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8366025/](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8366025/)

DICE provides a five-category classification schema across 7,000+ sentences from FDA drug labelling, covering indications, contraindications, side effects, usage instructions, and clinical observations — used here to benchmark obligation classification performance.

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.10+ |
| Agent Orchestration | LangGraph |
| LLM | Anthropic Claude API (`claude-3-5-sonnet`) |
| Embeddings | OpenAI `text-embedding-3-small` / Azure OpenAI |
| Vector Store | Azure Blob Storage + FAISS / Azure AI Search |
| Document Parsing | PyMuPDF (`fitz`), `pdfplumber` |
| Data Handling | Pandas, JSON |
| Evaluation | scikit-learn (classification metrics) |
| Environment | Python `dotenv`, Azure SDK |

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/regulatory-intelligence-agent.git
cd regulatory-intelligence-agent

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add: ANTHROPIC_API_KEY, AZURE_STORAGE_CONNECTION_STRING, OPENAI_API_KEY

# Run the agent on a sample document
python agent/run.py --document data/sample_spl.pdf --output results/output.json
```

---

## 📁 Repository Structure

```
├── agent/
│   ├── graph.py              # LangGraph state graph definition
│   ├── nodes/
│   │   ├── parser.py         # Document ingestion and chunking
│   │   ├── retriever.py      # Vector similarity search
│   │   ├── classifier.py     # Obligation type classification
│   │   ├── extractor.py      # Entity and obligation extraction
│   │   └── summariser.py     # Structured output generation
│   └── run.py                # Entry point
├── data/
│   ├── raw/                  # Raw regulatory documents
│   ├── processed/            # Chunked and embedded documents
│   └── sample_spl.pdf        # Example FDA drug label
├── embeddings/
│   └── azure_vector_store.py # Azure-hosted vector store interface
├── evaluation/
│   ├── annotated_gold.json   # Manual annotation subset
│   └── evaluate.py           # Precision/recall/F1 computation
├── notebooks/
│   └── Regulatory_Agent_Demo.ipynb
├── results/
│   └── evaluation_results.csv
├── .env.example
├── requirements.txt
└── README.md
```

---

## ✅ Skills Demonstrated

- **Agentic AI system design**: multi-node LangGraph workflow with state management and autonomous decision routing
- **LLM integration**: Claude API for structured reasoning, extraction, and classification on long-form regulatory text
- **Retrieval-Augmented Generation (RAG)**: vector-based document retrieval using Azure-hosted storage to improve contextual grounding and reduce hallucination
- **NLP pipeline for unstructured documents**: PDF parsing, semantic chunking, entity extraction, and obligation classification
- **Evaluation methodology**: precision, recall, F1, and hallucination rate benchmarked against a manually annotated gold-standard
- **Enterprise architecture thinking**: system designed as a deployable MVP for regulatory affairs and life sciences consulting workflows
- **Cloud integration**: Azure Blob Storage for scalable document and vector store management

---

## 🌍 Real-World Applications & Conclusion

### Why This Matters

Pharmaceutical and biotech companies spend an estimated **$50,000–$100,000+ per regulatory submission** in manual review time across legal, medical, and regulatory affairs teams. A single NDA (New Drug Application) can exceed 100,000 pages. The consequences of missed obligations — from post-market study deadlines to labelling non-compliance — include product recalls, Warning Letters, and significant reputational and financial damage.

### Deployment Scenarios

| Sector | Use Case |
|---|---|
| **Pharmaceutical Companies** | Automated extraction of post-market commitments from FDA approval letters and EMA CHMP opinions |
| **Life Sciences Consultancies** | Accelerated regulatory gap analysis and compliance auditing across client submission portfolios |
| **Contract Research Organisations (CROs)** | Rapid parsing of clinical trial protocols for regulatory obligation mapping |
| **Regulatory Affairs Agencies** | Intelligent document review queues, prioritising high-risk obligations for human expert attention |
| **Pharmacovigilance Teams** | Automated surveillance of safety obligation deadlines across global regulatory frameworks |

### Conclusion

This project demonstrates that agentic LLM systems — when grounded with vector retrieval and structured prompting — can meaningfully reduce the cognitive load of regulatory document review. The MVP achieves **87% obligation extraction accuracy** with a **<4% hallucination rate** on grounded queries, validating the core retrieval-augmented architecture.

The most important design insight is that **RAG is not optional in regulated industries**: without contextual grounding, LLMs hallucinate with confidence on dense technical documents — a risk that is unacceptable in life sciences compliance contexts. The combination of LangGraph's stateful orchestration and Claude's reasoning capability provides a robust foundation for a production-grade regulatory intelligence system.

Future development would target multi-jurisdictional support (FDA + EMA + PMDA), integration with enterprise document management systems (Veeva Vault), and a human-in-the-loop review interface for final obligation sign-off — moving from MVP toward a fully auditable, compliance-ready deployment.

