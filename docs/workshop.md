# Workshop: KNOW.md Impact on AI Agent Code Quality

## Overview

This workshop demonstrates how pre-extracted code metadata (KNOW.md) impacts AI agent response speed, quality, and accuracy compared to agents that explore codebases at runtime.

**Duration:** ~45 min in-session + home assignment
**Prerequisites:** Kiro CLI installed, Python 3.12+, `skill-sdk-aila` installed

---

## Part 1: Hands-On with Knowledge Agents (In-Session)

### Setup (5 min)

Clone the pre-documented repository:

```bash
cd ~/aila/z_practice_repos
git clone <workspace-repo-url> full-stack-fastapi-template
cd full-stack-fastapi-template
```

Verify workspace:
```bash
python3 workspace.py validate
```

You should see two agents available:
- `backend-py` — FastAPI backend expert (Python KNOW.md loaded)
- `frontend-ts` — React frontend expert (TypeScript KNOW.md loaded)

### Exercise 1: Ask Questions (15 min)

Open Kiro in the repo and try these prompts. Observe how fast and detailed the responses are:

**Architecture questions:**
- "What authentication flow does this app use? Trace from login form to JWT token."
- "How does the User model relate to Items? Show the full schema chain."
- "What dependencies does the items route use and how are they injected?"

**Implementation questions:**
- "Add a new 'projects' resource following the items pattern with fields: status, start_date, end_date, budget."
- "Add a 'tags' field to items — what files need to change?"
- "How would I add email notification when a new user registers?"

**Debugging questions:**
- "If a user gets 403 on DELETE /items/{id}, what are the possible causes?"
- "What happens if the database is down when the app starts?"

Notice:
- ⚡ Responses come in seconds, not minutes
- 📋 Code examples match actual project patterns
- 🔗 Agents reference specific files, functions, and relationships

### Exercise 2: Observe Subagent Delegation (10 min)

Ask a cross-domain question to the default agent:
- "Add a 'projects' resource — cover both backend and frontend."

Watch how it delegates to `backend-py` and `frontend-ts` subagents in parallel.

### Part 1 Debrief (15 min)

Review the pre-generated comparison report: `docs/know-md-impact-analysis.md`

Key findings:
| | No KNOW.md | With KNOW.md (focused) | With KNOW.md (comprehensive) |
|---|---|---|---|
| Time | 57s | 10s | 93s |
| Code examples | None | CRUD + router | Full BE + FE (500 lines) |
| File reads | 15+ | 0 | 0 |
| Accuracy | Variable | Pattern-accurate | Pattern-accurate |

The "without KNOW.md" response (`docs/session-report.md`) spent most of its time exploring the codebase and produced a broad report with no code. The "with KNOW.md" responses produced actionable implementation guides with working code — generated entirely from metadata.

---

## Part 2: Home Assignment — Verify It Yourself

### Objective

Clone the ORIGINAL (undocumented) repo, set up Kiro, and ask the same questions. Compare your results with the workshop results to verify the difference.

### Step 1: Clone Original Repo

```bash
cd ~/aila/z_practice_repos
git clone https://github.com/fastapi/full-stack-fastapi-template.git full-stack-fastapi-original
cd full-stack-fastapi-original
```

### Step 2: Set Up Kiro (No KNOW.md)

```bash
kiro
# Initialize code intelligence
/code init
```

No workspace, no KNOW.md, no steering — just raw Kiro with code tools.

### Step 3: Ask the Same Questions

Try the exact same prompts from Exercise 1:

1. "What authentication flow does this app use? Trace from login form to JWT token."
2. "Add a new 'projects' resource following the items pattern with fields: status, start_date, end_date, budget."
3. "How does the User model relate to Items? Show the full schema chain."

**Record for each question:**
- ⏱ Response time
- 📄 Response length
- 💻 Did it include code examples?
- 🔍 How many files did the agent read?
- ✅ Was the code accurate to the actual patterns?

### Step 4: Generate KNOW.md and Compare

Now add KNOW.md to the original repo:

```bash
# Install SDK if needed
pip install skill-sdk-aila

# Create config
mkdir -p .aila
cat > .aila/documentation.json << 'EOF'
{
  "output_dir": "document-meta",
  "providers": [
    {"type": "python", "enabled": true, "roots": ["."], "output": "python"},
    {"type": "typescript", "enabled": true, "roots": ["."], "output": "typescript"}
  ]
}
EOF

# Create docignore
cat > .aila/.docignore << 'EOF'
**/node_modules/**
**/__pycache__/**
**/test_*.py
**/*.spec.ts
frontend/src/client/**
frontend/src/components/ui/**
backend/app/alembic/versions/**
EOF

# Generate
python -m skill_sdk_aila.metadata --document
```

Add KNOW.md to Kiro steering:
```bash
mkdir -p .kiro/steering
ln -s ../../document-meta/python/KNOW.md .kiro/steering/KNOW-python.md
ln -s ../../document-meta/typescript/KNOW.md .kiro/steering/KNOW-typescript.md
```

### Step 5: Ask Again and Compare

Ask the same questions again with KNOW.md loaded. Compare:

| Question | Without KNOW.md | With KNOW.md |
|---|---|---|
| Auth flow | Time: ___ | Time: ___ |
| | Code examples: Y/N | Code examples: Y/N |
| | Files read: ___ | Files read: ___ |
| Add projects | Time: ___ | Time: ___ |
| | Code examples: Y/N | Code examples: Y/N |
| | Pattern-accurate: Y/N | Pattern-accurate: Y/N |
| Model relationships | Time: ___ | Time: ___ |
| | Complete: Y/N | Complete: Y/N |

### Deliverable

Write a short summary (3-5 sentences) of your findings. Did you observe the same differences as the workshop demo? What surprised you?

---

## Reference Materials

| File | Description |
|---|---|
| `docs/know-md-impact-analysis.md` | Full comparison report with metrics |
| `docs/adding-projects-resource.md` | Knowledge agent output (focused, 10s) |
| `docs/session-report.md` | Code-only agent output (no KNOW.md, 57s) |
| `docs/adding-projects-resource-with-know-detailed.md` | Knowledge agent output (comprehensive, 93s) |
| `document-meta/python/KNOW.md` | Auto-generated Python metadata |
| `document-meta/typescript/KNOW.md` | Auto-generated TypeScript metadata |
| `workspace.py` | Workspace definition with two agents |
