# Agent Assignment: Time Tracking Feature

## Epic

AWSP-114 — Time Tracking Feature for Full-Stack FastAPI Template

## Your Task

Read the epic and all linked stories from JIRA (AWSP-114 through AWSP-121). Plan and orchestrate implementation by delegating to specialist subagents.

## How to Work

You are the orchestrator. You do NOT implement code directly. You delegate to specialist subagents:

- **backend-py** — implements all Python/FastAPI code (models, routes, CRUD, tests)
- **frontend-ts** — implements all React/TypeScript code (components, routes, hooks)

For each story:
1. Read the JIRA acceptance criteria
2. Delegate to the appropriate subagent with clear instructions
3. Include the acceptance criteria in your delegation prompt
4. After subagent completes, verify the output (check files exist, run tests)
5. Move to next story

## Principles for Subagents

Include these in every delegation prompt:
- Follow existing codebase patterns exactly — KNOW.md is loaded, use it
- Do not invent new patterns — reuse what's already in the codebase
- Write unit tests for backend endpoints following existing test patterns
- Run tests after implementation to verify

## Implementation Order

1. Read all stories from JIRA epic AWSP-114
2. Create implementation plan
3. Delegate AWSP-115 to **backend-py** (models + migration)
4. Delegate AWSP-116 to **backend-py** (project routes + tests)
5. Delegate AWSP-117 to **backend-py** (time entry routes + tests)
6. Verify: run all backend tests
7. Delegate AWSP-121 to **frontend-ts** (sidebar navigation)
8. Delegate AWSP-118 to **frontend-ts** (projects page)
9. Delegate AWSP-119 to **frontend-ts** (time entry page)
10. Delegate AWSP-120 to **frontend-ts** (dashboard)

Backend stories (3-5) can be delegated sequentially — each depends on the previous.
Frontend stories (7-10) can be delegated in parallel after backend is complete.

## What Subagents Already Know

The subagents have KNOW.md loaded with complete codebase metadata. They know all patterns, file conventions, and import styles. You do not need to explain the codebase to them — just give them the acceptance criteria and tell them to implement.

## Start

Read JIRA epic AWSP-114 and begin.
