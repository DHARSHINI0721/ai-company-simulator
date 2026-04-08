# AI Company Simulator 🏢

**Autonomous Enterprise Agent Benchmark** | OpenEnv Compliant

This environment evaluates AI agents as autonomous compliance officers
in realistic enterprise workflows.

## Motivation
No existing benchmark tests AI agents on multi-domain enterprise decisions.
This environment fills that gap across HR, security, and policy domains.

## Tasks

| ID | Type | Difficulty | Description |
|---|---|---|---|
| email_001 | Email | Easy | Admin access request triage |
| email_002 | Email | Easy | HR policy bypass handling |
| security_001 | Security | Medium | Credential exposure response |
| security_002 | Security | Medium | API abuse detection |
| fix_001 | Fix | Hard | Database exposure remediation |
| fix_002 | Fix | Hard | Leaked API key remediation |

## Observation Space
- `input_text`: The enterprise situation to evaluate
- `task_type`: email / security / fix
- `step_number`: Current step in episode
- `context`: Task metadata (difficulty, task_id)

## Action Space
- `output`: Agent's decision as natural language text

## Reward Function
Scored 0.0–1.0 with breakdown:
- `keyword_match` (0.0–0.6): Correct decision keywords
- `response_quality` (0.0–0.2): Response completeness
- `task_bonus` (0.0–0.2): Policy/urgency references
- `penalty`: Deducted for wrong decisions or too many steps

## Baseline Scores (Mistral-7B)

| Task Type | Avg Reward |
|---|---|
| Email | 0.82 |
| Security | 0.88 |
| Fix | 0.79 |
| **Overall** | **0.83** |

## Setup

```bash
pip install -r requirements.txt
set HF_TOKEN=your_huggingface_token   # Windows
python inference.py
```

## Docker
```bash
docker build -t ai-company-sim .
docker run -e HF_TOKEN=your_token ai-company-sim
```