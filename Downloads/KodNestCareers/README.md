KodNestCareers Monorepo
=======================

This repository is a local-first, modular monolith with worker processes for background jobs.

Prerequisites
-------------
- Node.js and pnpm
- Docker and Docker Compose

Getting started
---------------
1. Install dependencies:
   - pnpm install

2. Start local infrastructure:
   - ./infra/scripts/up-local.sh

3. Run applications (once implemented):
   - pnpm dev:web
   - pnpm dev:worker

Repository layout
-----------------
- apps/web           Web application (Next.js app directory layout)
- apps/worker        Background worker and schedulers
- packages/db        Database client and repositories
- packages/modules   Domain modules (auth profile, job tracker, readiness, resume, notifications, analytics)
- packages/ai-gateway  AI provider routing and prompt management
- packages/events    Event and outbox abstractions
- packages/shared    Shared types, utilities, and validation
- packages/config    Configuration and feature flags
- infra              Local infrastructure and scripts
- docs               Product, architecture, runbooks, and testing docs

Note
----
This is scaffold only. Business logic and concrete implementations will be added later.

