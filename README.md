# CYP Induction Inhibition Tdi

> **Domain:** Computational Biology & AI Drug Discovery
> **Reference Guidelines & Standards:** `wwPDB, IUPAC & CLSI Computational Guidelines`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**CYP Induction Inhibition Tdi** is an advanced analytical and computational platform implementing Mechanism-based CYP time-dependent inhibition (Kinact/KI) pharmacokinetic agent.

---

## ⚙️ Key Capabilities & Algorithmic Modules

- **Deterministic Calculation Engine**: Strict compliance with standard reference formulations and thresholds.
- **Risk & Urgency Classification**: Multi-tier categorization with automated clinical/operational action recommendations.
- **Validation & Guardrails**: Rigorous input bounds checking and anomaly detection.

---

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/cyp-induction-inhibition-tdi.git
cd cyp-induction-inhibition-tdi

# Install dependencies
pip install -e .

# Optional: Install with FastAPI support
pip install fastapi uvicorn
```

---

## 💻 CLI Quickstart & Usage

### 1. Run Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --status DISCORDANT
```

### 2. Interactive Chat Query
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch Process CSV Records
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Launch REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `--task-id` | str | TASK-2026-001 | Unique task/case identifier |
| `--target` | str | KEY-TARGET-01 | Entity, patient key, or target |
| `--primary` | float | 28.5 | Primary domain measurement |
| `--secondary` | float | 14.2 | Secondary kinetic/confidence score |
| `--critical` | flag | False | Emergency escalation trigger |
| `--status` | str | DISCORDANT | Status code or phenotype descriptor |
| `-i, --input` | str | (required) | Input CSV file path for batch |
| `-o, --output` | str | results.csv | Output CSV file path for batch |

### Input Data Schema (CSV Batch)

| Field | Type | Description | Requirement |
|:------|:-----|:------------|:------------|
| `task_id` | str | Unique task identifier | Required |
| `target_identifier` | str | Target entity/key | Required |
| `primary_metric` | float | Primary measurement | Required |
| `secondary_metric` | float | Secondary score | Required |
| `is_critical_flag` | bool | Escalation flag | Required |
| `status_descriptor` | str | Status code | Required |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

### Security Configuration

Set the `AUDIT_SECRET_KEY` environment variable for persistent audit integrity across restarts:

```bash
# Linux/macOS
export AUDIT_SECRET_KEY="your-secure-random-key"

# Windows
set AUDIT_SECRET_KEY=your-secure-random-key
```

If not set, a random ephemeral key is generated at startup (audit trail will not persist across restarts).

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 100
```

---

## 🐳 Container Deployment

```bash
docker build -t cyp-induction-inhibition-tdi .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secure-key cyp-induction-inhibition-tdi
```

### Docker Compose

```bash
docker-compose up -d
```

---

## 📁 Project Structure

```
cyp-induction-inhibition-tdi/
├── agents/                  # Core agent system with PHI guard & HMAC audit
│   ├── api.py              # FastAPI REST endpoints
│   ├── base.py             # Security, PHI guard, audit trail
│   ├── models.py           # Pydantic data models
│   ├── supervisor.py       # Multi-agent orchestrator
│   ├── workers.py          # Specialized domain workers
│   ├── llm_factory.py      # LLM client factory
│   ├── learning.py         # Bayesian calibration engine
│   ├── metrics.py          # Prometheus metrics exporter
│   └── streamer.py         # WebSocket telemetry broadcaster
├── cyp_kinetics/           # Alternative CYP-Kin calculation engine
│   ├── agents.py           # Sub-agent coordination
│   ├── cli.py              # CLI for CYP-Kin engine
│   ├── engine.py           # Core algorithmic engine
│   ├── models.py           # Data models
│   └── server.py           # FastAPI server factory
├── tests/                  # Test suite
├── web/                    # Static web assets
├── cli.py                  # Main CLI entry point
├── cyp_kinetics_app.py    # CYP-Kin CLI entry point
├── enrichment.py           # Enrichment feature engines
├── simulator.py            # High-throughput testing simulator
├── sample.csv              # Sample batch input
├── pyproject.toml          # Project configuration
├── Dockerfile              # Container build
└── docker-compose.yml      # Multi-container orchestration
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.
